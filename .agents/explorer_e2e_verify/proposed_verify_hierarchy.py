#!/usr/bin/env python3
import sys
import os
import re
from html.parser import HTMLParser

# --- HTML CSS Extractor ---
class StyleExtractor(HTMLParser):
    """Extracts all text content from <style> tags in an HTML file."""
    def __init__(self):
        super().__init__()
        self.style_blocks = []
        self.in_style = False
        self.current_style = []
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'style':
            self.in_style = True
            self.current_style = []
            
    def handle_data(self, data):
        if self.in_style:
            self.current_style.append(data)
            
    def handle_endtag(self, tag):
        if tag.lower() == 'style':
            self.in_style = False
            self.style_blocks.append("".join(self.current_style))

# --- HTML Class Verifier ---
class ClassVerifier(HTMLParser):
    """Tracks all CSS class names present in elements inside the HTML <body>."""
    def __init__(self):
        super().__init__()
        self.found_classes = set()
        self.in_body = False
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'body':
            self.in_body = True
        if self.in_body:
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict:
                for c in attrs_dict['class'].split():
                    self.found_classes.add(c)
                    
    def handle_endtag(self, tag):
        if tag.lower() == 'body':
            self.in_body = False

# --- CSS Selector Helpers ---
def extract_classes_from_selector(selector):
    """Extracts CSS class names (without the leading dot) from a single selector string."""
    return set(re.findall(r'\.([a-zA-Z0-9_-]+)', selector))

def parse_css_text(css_text):
    """
    Parses CSS stylesheet text into structured rules.
    Correctly handles comments, nested @media blocks, and groups of selectors.
    """
    # Remove CSS comments
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    # Clean whitespace
    css_text = re.sub(r'\s+', ' ', css_text)
    
    def extract_blocks(text):
        blocks = []
        depth = 0
        block_header_start = 0
        block_content_start = 0
        
        for idx, char in enumerate(text):
            if char == '{':
                if depth == 0:
                    header = text[block_header_start:idx].strip()
                    block_content_start = idx + 1
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    content = text[block_content_start:idx].strip()
                    blocks.append((header, content))
                    block_header_start = idx + 1
        return blocks

    all_rules = []
    
    def process_blocks(blocks, media_query=None):
        for header, content in blocks:
            if header.startswith('@media'):
                sub_blocks = extract_blocks(content)
                process_blocks(sub_blocks, media_query=header)
            elif header.startswith('@keyframes'):
                # Keyframes contain sub-blocks which we skip for property parsing
                pass
            else:
                props = {}
                for decl in content.split(';'):
                    if not decl.strip():
                        continue
                    if ':' in decl:
                        name, val = decl.split(':', 1)
                        props[name.strip().lower()] = val.strip()
                
                selectors = [s.strip() for s in header.split(',')]
                for sel in selectors:
                    all_rules.append({
                        'selector': sel,
                        'properties': props,
                        'media': media_query
                    })
                    
    blocks = extract_blocks(css_text)
    process_blocks(blocks)
    return all_rules

def resolve_variables(val, variables):
    """Resolves CSS var(--var-name) values recursively using a variables dictionary."""
    for _ in range(5):  # Max nesting resolution depth
        matches = re.findall(r'var\((--[a-zA-Z0-9_-]+)\)', val)
        if not matches:
            break
        for var_name in matches:
            if var_name in variables:
                val = val.replace(f'var({var_name})', variables[var_name])
            else:
                break
    return val

def convert_unit(num, unit):
    """Converts standard CSS length units to an approximate pixel value."""
    if unit in ('rem', 'em'):
        return num * 16.0
    elif unit == '%':
        return (num / 100.0) * 16.0
    elif unit == 'pt':
        return num * 1.333
    return num

def parse_font_size(val):
    """Parses and normalizes a CSS font-size property value to pixels."""
    val = val.strip().lower().replace('!important', '').strip()
    
    # 1. Try exact match: 24px, 1.5rem, etc.
    match = re.match(r'^([\d.]+)\s*(px|rem|em|%|pt)?$', val)
    if match:
        num = float(match.group(1))
        unit = match.group(2)
        return convert_unit(num, unit)
        
    # 2. Try fallback for complex expressions like calc(), clamp()
    matches = re.findall(r'([\d.]+)\s*(px|rem|em|%|pt)?', val)
    if matches:
        num = float(matches[0][0])
        unit = matches[0][1]
        return convert_unit(num, unit)
        
    raise ValueError(f"Could not parse font-size: '{val}'")

def parse_font_weight(val):
    """Parses and normalizes CSS font-weight property value to an integer weight representation."""
    val = val.strip().lower().replace('!important', '').strip()
    if val.isdigit():
        return int(val)
    weight_map = {
        'normal': 400,
        'bold': 700,
        'bolder': 800,
        'lighter': 300,
        'initial': 400,
        'inherit': 400
    }
    if val in weight_map:
        return weight_map[val]
    raise ValueError(f"Could not parse font-weight: '{val}'")

def main():
    game_path = 'game.html'
    if not os.path.exists(game_path):
        print(f"Error: {game_path} not found.")
        sys.exit(1)
        
    with open(game_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # 1. Extract CSS from <style> blocks
    extractor = StyleExtractor()
    extractor.feed(html_content)
    style_blocks = extractor.style_blocks
    
    if not style_blocks:
        print("Error: No <style> blocks found in game.html.")
        sys.exit(1)
        
    combined_css = "\n".join(style_blocks)
    rules = parse_css_text(combined_css)
    
    # 2. Extract CSS Custom Properties (Variables)
    css_variables = {}
    for rule in rules:
        for prop, val in rule['properties'].items():
            if prop.startswith('--'):
                css_variables[prop] = val
                
    # 3. Verify target classes exist in the HTML body
    verifier = ClassVerifier()
    verifier.feed(html_content)
    body_classes = verifier.found_classes
    
    required_classes = ['hero-metric-val', 'secondary-metric-val']
    missing_req = [c for c in required_classes if c not in body_classes]
    if missing_req:
        print(f"Error: Missing required metric classes in HTML body: {missing_req}")
        sys.exit(1)
        
    tertiary_classes_in_body = [c for c in ['card-note', 'tertiary-metric-val'] if c in body_classes]
    if not tertiary_classes_in_body:
        print("Error: Neither 'card-note' nor 'tertiary-metric-val' classes found in HTML body.")
        sys.exit(1)
        
    print(f"Verified body classes present: {list(body_classes.intersection({'hero-metric-val', 'secondary-metric-val', 'tertiary-metric-val', 'card-note'}))}")
    
    # 4. Resolve styles for target classes in base CSS rules (media query is None)
    target_classes = ['hero-metric-val', 'secondary-metric-val', 'tertiary-metric-val', 'card-note']
    class_styles = {c: {} for c in target_classes}
    
    for rule in rules:
        if rule['media'] is not None:
            continue
        classes_in_sel = extract_classes_from_selector(rule['selector'])
        for tc in target_classes:
            if tc in classes_in_sel:
                for prop, val in rule['properties'].items():
                    resolved_val = resolve_variables(val, css_variables)
                    class_styles[tc][prop] = resolved_val
                    
    # 5. Parse and validate font properties
    classes_to_check = ['hero-metric-val', 'secondary-metric-val'] + tertiary_classes_in_body
    resolved_metrics = {}
    
    for tc in classes_to_check:
        styles = class_styles[tc]
        if 'font-size' not in styles:
            print(f"Error: 'font-size' not declared in base CSS for '.{tc}'.")
            sys.exit(1)
        if 'font-weight' not in styles:
            print(f"Error: 'font-weight' not declared in base CSS for '.{tc}'.")
            sys.exit(1)
            
        try:
            sz_val = parse_font_size(styles['font-size'])
        except ValueError as e:
            print(f"Error parsing font-size for '.{tc}': {e}")
            sys.exit(1)
            
        try:
            wt_val = parse_font_weight(styles['font-weight'])
        except ValueError as e:
            print(f"Error parsing font-weight for '.{tc}': {e}")
            sys.exit(1)
            
        resolved_metrics[tc] = {
            'font-size': sz_val,
            'font-weight': wt_val,
            'raw_font-size': styles['font-size'],
            'raw_font-weight': styles['font-weight']
        }
        
    print("\nParsed CSS Metrics:")
    for tc, metrics in resolved_metrics.items():
        print(f"  .{tc:22} => font-size: {metrics['raw_font-size']:8} ({metrics['font-size']:.1f}px normalized), font-weight: {metrics['raw_font-weight']:8} ({metrics['font-weight']} normalized)")
        
    # Check 1: font size of hero-metric-val > secondary-metric-val
    hero = resolved_metrics['hero-metric-val']
    secondary = resolved_metrics['secondary-metric-val']
    if not (hero['font-size'] > secondary['font-size']):
        print(f"Error: Font size hierarchy violated! Hero ({hero['font-size']:.1f}px) is not strictly greater than Secondary ({secondary['font-size']:.1f}px).")
        sys.exit(1)
        
    # Check 2: font size of secondary-metric-val > tertiary elements
    for tc in tertiary_classes_in_body:
        tert = resolved_metrics[tc]
        if not (secondary['font-size'] > tert['font-size']):
            print(f"Error: Font size hierarchy violated! Secondary ({secondary['font-size']:.1f}px) is not strictly greater than Tertiary .{tc} ({tert['font-size']:.1f}px).")
            sys.exit(1)
            
    # Check 3: font weight of hero-metric-val >= secondary-metric-val
    if not (hero['font-weight'] >= secondary['font-weight']):
        print(f"Error: Font weight hierarchy violated! Hero weight ({hero['font-weight']}) is less than Secondary weight ({secondary['font-weight']}).")
        sys.exit(1)
        
    print("\nVisual hierarchy verification PASSED!")
    
    # Check 6: Check for CSS animation/transition property
    has_keyframes = any(re.search(r'@keyframes\b', block) for block in style_blocks)
    has_transition = any(re.search(r'\btransition\s*:', block) for block in style_blocks) or any(re.search(r'\btransition-\w+\s*:', block) for block in style_blocks)
    
    print("\nAnimation/Transition check:")
    print(f"  @keyframes rule found: {has_keyframes}")
    print(f"  transition property found: {has_transition}")
    
    if not (has_keyframes or has_transition):
        print("Error: CSS does not contain any @keyframes rule or transition property.")
        sys.exit(1)
        
    print("Modernization animation/transition check PASSED!")
    
    print("\nAll hierarchy and style checks passed successfully!")
    sys.exit(0)

if __name__ == '__main__':
    main()

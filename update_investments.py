with open('game.html', 'r') as f:
    content = f.read()

css_old = """        .input-group input {
            background: #0f172a;"""
css_new = """        .input-group input, .input-group select {
            background: #0f172a;
            border: 1px solid #475569;
            border-radius: 6px;
            color: #f8fafc;
            padding: 7px 10px;
            font-size: 13px;
            font-family: 'Inter', sans-serif;
            transition: border-color 0.15s;
            width: 100%;
            box-sizing: border-box;
        }
        .input-group input:focus, .input-group select:focus {
            outline: none;
            border-color: #38bdf8;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);
        }
        .input-group select {
            appearance: none;
            padding-right: 24px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 8px center;
        }
        /* Hide the old input block to avoid duplicate matching */
        .old_input_ignore {"""
content = content.replace("""        .input-group input {
            background: #0f172a;
            border: 1px solid #475569;
            border-radius: 6px;
            color: #f8fafc;
            padding: 7px 10px;
            font-size: 13px;
            font-family: 'Inter', sans-serif;
            transition: border-color 0.15s;
            width: 100%;
            box-sizing: border-box;
        }
        .input-group input:focus {""", css_new)


html_old = """                <div class="input-group">
                    <label>Reinvestment Yield (%)</label>
                    <input type="number" id="inp_hysa" value="4.0" step="0.25" min="0" max="25">
                </div>"""

html_new = """                <div class="input-group">
                    <label>Reinvestment</label>
                    <div style="display: flex; gap: 4px;">
                        <select id="inp_invType" style="flex: 2;" onchange="
                            if(this.value !== 'custom') {
                                document.getElementById('inp_hysa').value = this.value;
                            }
                        ">
                            <option value="4.0">Savings (4%)</option>
                            <option value="5.0">T-Bills (5%)</option>
                            <option value="10.0">S&P 500 (10%)</option>
                            <option value="15.0">Real Estate (15%)</option>
                            <option value="custom">Custom</option>
                        </select>
                        <input type="number" id="inp_hysa" value="4.0" step="0.25" min="0" max="50" style="flex: 1;" onchange="document.getElementById('inp_invType').value = 'custom';">
                    </div>
                </div>"""

content = content.replace(html_old, html_new)

with open('game.html', 'w') as f:
    f.write(content)

print("Updated investment options UI.")

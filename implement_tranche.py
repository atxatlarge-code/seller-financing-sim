import re

with open('game.html', 'r') as f:
    content = f.read()

# 1. Update UI Inputs
html_old_dropdown = """                        <select id="inp_invType" style="flex: 2;" onchange="
                            if(this.value !== 'custom') {
                                document.getElementById('inp_hysa').value = this.value;
                            }
                        ">"""
html_new_dropdown = """                        <select id="inp_invType" style="flex: 2;" onchange="
                            if(this.value !== 'custom') {
                                document.getElementById('inp_hysa').value = this.value;
                                document.getElementById('inp_deploymentMin').value = (this.value === '15.0') ? 50000 : 0;
                            }
                        ">"""
content = content.replace(html_old_dropdown, html_new_dropdown)

# Add Min Deployment input
html_old_appr = """                <div class="input-group">
                    <label>Appreciation (%/yr)</label>"""
html_new_appr = """                <div class="input-group">
                    <label>Min Deployment ($)</label>
                    <input type="number" id="inp_deploymentMin" value="0" step="5000">
                </div>
                <div class="input-group">
                    <label>Appreciation (%/yr)</label>"""
content = content.replace(html_old_appr, html_new_appr)

# 2. Update readInputs
old_read = """                hysa: parseFloat(document.getElementById('inp_hysa').value) / 100,"""
new_read = """                hysa: parseFloat(document.getElementById('inp_hysa').value) / 100,
                deploymentMin: parseFloat(document.getElementById('inp_deploymentMin').value),"""
content = content.replace(old_read, new_read)

# 3. Global states
old_globals = """        let sf_loanBalance, sf_studentCash, sf_arthurCash, sf_accruedTax;
        let bk_loanBalance, bk_studentCash, bk_arthurCash, bk_accruedTax;"""
new_globals = """        let sf_loanBalance, sf_st_checking, sf_st_invested, sf_arthurCash, sf_accruedTax;
        let bk_loanBalance, bk_st_checking, bk_st_invested, bk_arthurCash, bk_accruedTax;
        
        function get_sf_studentCash() { return sf_st_checking + sf_st_invested; }
        function get_bk_studentCash() { return bk_st_checking + bk_st_invested; }"""
content = content.replace(old_globals, new_globals)

# 4. initState updates
old_init = """            // Scenario 1: Seller Financed
            sf_loanBalance = loanAmount;
            sf_studentCash = CONFIG.buyerCash - CONFIG.downPayment;
            sf_accruedTax = CONFIG.downPayment * gainRatio * capGainsTaxRate;"""
new_init = """            // Scenario 1: Seller Financed
            sf_loanBalance = loanAmount;
            sf_st_checking = CONFIG.buyerCash - CONFIG.downPayment;
            sf_st_invested = 0;
            sf_accruedTax = CONFIG.downPayment * gainRatio * capGainsTaxRate;"""
content = content.replace(old_init, new_init)

old_init_bk = """            // Scenario 2: Traditional Bank
            bk_loanBalance = loanAmount;
            bk_studentCash = CONFIG.buyerCash - CONFIG.downPayment - CONFIG.closingCosts;
            bk_accruedTax = CONFIG.downPayment * gainRatio * capGainsTaxRate;"""
new_init_bk = """            // Scenario 2: Traditional Bank
            bk_loanBalance = loanAmount;
            bk_st_checking = CONFIG.buyerCash - CONFIG.downPayment - CONFIG.closingCosts;
            bk_st_invested = 0;
            bk_accruedTax = CONFIG.downPayment * gainRatio * capGainsTaxRate;"""
content = content.replace(old_init_bk, new_init_bk)

# Fix variables everywhere in HTML logic
# We need to replace sf_studentCash with get_sf_studentCash() when reading, and when writing we add to sf_st_checking
content = content.replace('sf_studentCash =', 'sf_st_checking =')
content = content.replace('bk_studentCash =', 'bk_st_checking =')

content = content.replace('sf_studentCash +=', 'sf_st_checking +=')
content = content.replace('bk_studentCash +=', 'bk_st_checking +=')

content = content.replace('sf_studentCash -=', 'sf_st_checking -=')
content = content.replace('bk_studentCash -=', 'bk_st_checking -=')

content = content.replace('sf_studentCash', 'get_sf_studentCash()')
content = content.replace('bk_studentCash', 'get_bk_studentCash()')

# But wait, my find/replace just made `get_sf_studentCash() +=` which is invalid. 
# Let me roll back and do it carefully.

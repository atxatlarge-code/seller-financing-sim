with open('game.html', 'r') as f:
    content = f.read()

content = content.replace('let sf_studentCash;\n', '')
content = content.replace('let bk_studentCash;\n', '')
content = content.replace('sf_studentCash = CONFIG.buyerCash - CONFIG.downPayment;\n', '')
content = content.replace('bk_studentCash = CONFIG.buyerCash - CONFIG.downPayment - CONFIG.closingCosts;\n', '')

content = content.replace('sf_studentCash', 'get_sf_studentCash()')
content = content.replace('bk_studentCash', 'get_bk_studentCash()')

# But we need to fix any `get_sf_studentCash()()` instances if they existed.
content = content.replace('get_sf_studentCash()()', 'get_sf_studentCash()')
content = content.replace('get_bk_studentCash()()', 'get_bk_studentCash()')

# Write back
with open('game.html', 'w') as f:
    f.write(content)
print("done")

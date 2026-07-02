with open('game.html', 'r') as f:
    content = f.read()

content = content.replace('get_get_sf_studentCash()', 'get_sf_studentCash()')
content = content.replace('get_get_bk_studentCash()', 'get_bk_studentCash()')

with open('game.html', 'w') as f:
    f.write(content)
print("done")

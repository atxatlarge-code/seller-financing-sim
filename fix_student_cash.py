with open('game.html', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    line = lines[i]
    if "sf_studentCash" in line or "bk_studentCash" in line:
        if "function get_sf_studentCash" in line or "function get_bk_studentCash" in line:
            continue
        if "+=" in line or "-=" in line:
            line = line.replace('sf_studentCash', 'sf_st_checking')
            line = line.replace('bk_studentCash', 'bk_st_checking')
        elif "=" in line and not ("==" in line or "===" in line) and "sf_studentCash +" not in line and "bk_studentCash +" not in line and "sf_studentCash -" not in line and "bk_studentCash -" not in line and "sf_studentCash =" in line:
            # this handles `let sf_studentStart = sf_studentCash + ...` No, wait!
            pass
        
        # General reads
        line = line.replace('sf_studentCash', 'get_sf_studentCash()')
        line = line.replace('bk_studentCash', 'get_bk_studentCash()')
        
        # Fix the case where my simple logic turned `sf_st_checking +=` into `get_sf_studentCash() +=`
        line = line.replace('get_sf_studentCash() +=', 'sf_st_checking +=')
        line = line.replace('get_bk_studentCash() +=', 'bk_st_checking +=')
        line = line.replace('get_sf_studentCash() -=', 'sf_st_checking -=')
        line = line.replace('get_bk_studentCash() -=', 'bk_st_checking -=')
        
    lines[i] = line

with open('game.html', 'w') as f:
    f.writelines(lines)
print("done")

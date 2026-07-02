import re

with open('game.html', 'r') as f:
    content = f.read()

# 1. Update Inputs in HTML
old_inputs = """                <div class="input-group">
                    <label>HYSA APY (%)</label>
                    <input type="number" id="inp_hysa" value="4.0" step="0.25" min="0" max="10">
                </div>"""
new_inputs = """                <div class="input-group">
                    <label>Reinvestment Yield (%)</label>
                    <input type="number" id="inp_hysa" value="4.0" step="0.25" min="0" max="25">
                </div>
                <div class="input-group">
                    <label>Simulation Years</label>
                    <input type="number" id="inp_simulationYears" value="10" step="5" min="5" max="50">
                </div>"""
content = content.replace(old_inputs, new_inputs)

# 2. Update readInputs()
old_read = """                hysa: parseFloat(document.getElementById('inp_hysa').value) / 100,
                appreciation: parseFloat(document.getElementById('inp_appreciation').value) / 100,
                sellerFees: parseFloat(document.getElementById('inp_sellerFees').value),"""
new_read = """                hysa: parseFloat(document.getElementById('inp_hysa').value) / 100,
                appreciation: parseFloat(document.getElementById('inp_appreciation').value) / 100,
                sellerFees: parseFloat(document.getElementById('inp_sellerFees').value),
                simulationYears: parseInt(document.getElementById('inp_simulationYears').value, 10),"""
content = content.replace(old_read, new_read)

# 3. Update 10 years to dynamic in strings
content = content.replace('10-year simulation complete!', '${CONFIG.simulationYears}-year simulation complete!')
content = content.replace('over 10 years.', 'over " + CONFIG.simulationYears + " years.')
content = content.replace('over 10 years.`', 'over ${CONFIG.simulationYears} years.`')
content = content.replace('10-YEAR STUDY COMPLETE', '<span id="studyCompleteYear">10</span>-YEAR STUDY COMPLETE')
content = content.replace('10-Year Verdict: Who Wins?', '<span id="verdictYear">10</span>-Year Verdict: Who Wins?')
content = content.replace('Comparing Net Wealth totals at Year 0, Year 5 (Balloon), and Year 10 (End)', 'Comparing Net Wealth totals at Year 0, Year 5 (Balloon), and Year <span id="tblMaxYear">10</span> (End)')
content = content.replace('Visualizing the 10-year wealth trajectories', 'Visualizing the <span id="chartSubMaxYear">10</span>-year wealth trajectories')
content = content.replace('Year 10<br><span', 'Year <span id="tblRowMaxYear">10</span><br><span')

# 4. Month max display
content = content.replace('0</span> / 120</div>', '0</span> / <span id="monthMaxDisplay">120</span></div>')

# 5. Timeline step
content = content.replace('id="tStep_120"', 'id="tStep_End"')
content = content.replace('Month 120: Study Complete', 'Year <span id="tStep_max_txt">10</span>: Study Complete')

# 6. HTML IDs for m120
content = content.replace('id="m120_', 'id="mEnd_')
content = content.replace("m120_data", "mEnd_data")
content = content.replace("renderMilestone('m120'", "renderMilestone('mEnd'")

# 7. JS updates
content = content.replace('let step120 = document.getElementById(\'tStep_120\');', 'let stepEnd = document.getElementById(\'tStep_End\');')
content = content.replace('[step0, step24, step60, step120].forEach', '[step0, step24, step60, stepEnd].forEach')
content = content.replace('step120.classList.add(\'active\');', 'stepEnd.classList.add(\'active\');')
content = content.replace('Month 120', 'Month ${CONFIG.simulationYears * 12}')

content = content.replace('month / 120 * 100', 'month / (CONFIG.simulationYears * 12) * 100')
content = content.replace('month >= 120', 'month >= (CONFIG.simulationYears * 12)')
content = content.replace('month === 120', 'month === (CONFIG.simulationYears * 12)')
content = content.replace('month < 120', 'month < (CONFIG.simulationYears * 12)')
content = content.replace('Math.min(month + 12, 120)', 'Math.min(month + 12, (CONFIG.simulationYears * 12))')

with open('game.html', 'w') as f:
    f.write(content)
print("Refactor applied.")

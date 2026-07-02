def calculate_monthly_payment(p, r, n):
    r_monthly = r / 12
    return p * (r_monthly * (1 + r_monthly)**n) / ((1 + r_monthly)**n - 1)

sale_price = 400000
down_payment = 40000
buyer_cash = 50000
sf_rate = 0.05
bank_rate = 0.075
rent = 3000
appreciation = 0.03
closing_costs = 8000
pmi_rate = 0.0075
hysa = 0.04

def sim(years):
    months = years * 12
    # Property Value
    prop_val = sale_price * ((1 + appreciation)**years)
    
    # SF Scenario
    # Initial loan
    sf_loan = sale_price - down_payment
    sf_pmt = calculate_monthly_payment(sf_loan, sf_rate, 360)
    sf_cash = buyer_cash - down_payment
    sf_debt = sf_loan
    
    # Run 5 years (60 months)
    for m in range(min(60, months)):
        interest = sf_debt * (sf_rate / 12)
        principal = sf_pmt - interest
        sf_debt -= principal
        sf_cash = sf_cash * (1 + hysa/12) + (rent - sf_pmt)
        
    # Balloon refi at year 5
    if months > 60:
        sf_pmt_new = calculate_monthly_payment(sf_debt, bank_rate, 300)
        # pay refi closing costs? the html says "Student borrows payoff amount from bank at bank rate for remaining 25 years"
        # lets assume no additional closing costs or minimal
        for m in range(60, min(360, months)):
            interest = sf_debt * (bank_rate / 12)
            principal = sf_pmt_new - interest
            sf_debt -= principal
            sf_cash = sf_cash * (1 + hysa/12) + (rent - sf_pmt_new)
            
    if months > 360:
        for m in range(360, months):
            sf_cash = sf_cash * (1 + hysa/12) + rent
            
    sf_nw = sf_cash + max(0, prop_val - sf_debt)

    # Bank Scenario
    bk_loan = sale_price - down_payment
    bk_pmt = calculate_monthly_payment(bk_loan, bank_rate, 360)
    bk_cash = buyer_cash - down_payment - closing_costs
    bk_debt = bk_loan
    
    for m in range(min(360, months)):
        interest = bk_debt * (bank_rate / 12)
        principal = bk_pmt - interest
        bk_debt -= principal
        
        # PMI
        pmi = 0
        if bk_debt > 0.8 * sale_price:
            pmi = (pmi_rate * bk_loan) / 12
            
        bk_cash = bk_cash * (1 + hysa/12) + (rent - bk_pmt - pmi)
        
    if months > 360:
        for m in range(360, months):
            bk_cash = bk_cash * (1 + hysa/12) + rent
            
    bk_nw = bk_cash + max(0, prop_val - bk_debt)
    
    print(f"Year {years}: PropVal: ${prop_val:,.0f}")
    print(f"  SF NW: ${sf_nw:,.0f} (Cash: ${sf_cash:,.0f}, Debt: ${sf_debt:,.0f})")
    print(f"  BK NW: ${bk_nw:,.0f} (Cash: ${bk_cash:,.0f}, Debt: ${bk_debt:,.0f})")
    print(f"  Diff: ${sf_nw - bk_nw:,.0f}")

sim(10)
sim(20)
sim(30)
sim(50)


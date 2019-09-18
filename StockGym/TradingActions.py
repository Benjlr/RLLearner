

def enter_stock(long_short, account_value, atr, price, rsk):
    stop_price = price - (long_short *  2.1 * atr)
    dollar_risk = account_value * rsk    
    amount_shares = dollar_risk / (price - stop_price)
    return amount_shares, stop_price


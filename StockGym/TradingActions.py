
MAX_PORTFOLIO_RISK = 0.025
INITIAL_ATR_DIST_STOP_MAX = 2.5
INITIAL_ATR_DIST_STOP_MIN = 1.2


def enter_stock(long_short, account_value, atr, price):
    stop_price = price - (long_short *  INITIAL_ATR_DIST_STOP * atr)
    dollar_risk = account_value * MAX_PORTFOLIO_RISK    
    amount_shares = dollar_risk / (price - stop_price)
    return amount_shares, stop_price


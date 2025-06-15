
class ZeroCouponBond:
    def __init__(self, principal, maturity, interest_rate):
        # principal amount
        self.principal = principal
        #time to maturity of bond
        self.maturity = maturity
        #market interest rate for discounting
        self.interest_rate = interest_rate / 100

    def calculate_present_value(self, x, n):
        return x/(1+self.interest_rate)**n

    def calculate_price(self):
        return self.calculate_present_value(self.principal, self.maturity)


if __name__ == "__main__":
    bond = ZeroCouponBond(1000, 2, 4)
    print("Price of the bond: %.2f" % bond.calculate_price()) #print in float value upto precision = 2
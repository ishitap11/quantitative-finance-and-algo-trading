
class CouponBond:
    def __init__(self, principal, coupon_rate, maturity, interest_rate):
        self.principal = principal
        self.coupon_rate = coupon_rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100


    ##def calculate_present_value_of_coupon(self, coupon, n):
     ##   return (coupon / self.interest_rate)*(1 - (1+self.interest_rate)**(-n))

    def calculate_present_value(self, x, n):
        return x/(1+self.interest_rate)**n

    def calculate_price(self):
        price = 0

        for i in range(1, self.maturity+1): # increase range by 1 because last value is excluded in python
            price += self.calculate_present_value(self.principal*self.coupon_rate, i)

        price += self.calculate_present_value(self.principal, self.maturity)
        return price


if __name__ == "__main__":
    bond = CouponBond(1000, 10, 3, 4)
    print("Price of the bond: %.2f" % bond.calculate_price()) #print in float value upto precision = 2
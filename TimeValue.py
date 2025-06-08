from math import exp as e

def future_discrete_value(x, r, n):
    return x*(1+r)**n


def present_discrete_value(x, r, n):
    return x*(1+r)**-n


def future_cont_value(x, r, n):
    return x*e(r*n)


def present_cont_value(x, r, n):
    return x*e(-r*n)

if __name__ == "__main__":
    #value of investment
    x = 100
    #interest rate
    r = 0.05
    #time duration in years
    n = 5

    print("Future discrete value: %s" % future_discrete_value(x, r, n))
    print("Present discrete value: %s" % present_discrete_value(x, r, n))
    print("Future cont value: %s" % future_cont_value(x, r, n))
    print("Present cont value: %s" % present_cont_value(x, r, n))
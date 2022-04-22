import math

while(1):
    b = int(input("before: "))
    l = int(input("lv: "))
    n = int(input("Times: "))

    if ((b/2) <= (250+10*(n - 1))):
        condition_3 = True
        b_on_2_factor = b/2
    else:
        condition_3 = False
        b_on_2_factor = 250 + 10*(n - 1)

    a = math.floor( 10 + b* (10*(n-1)+b_on_2_factor+l/2)/1000)

    if (a > 3 * l):
        a = 3 * l

    b_max_reverse = math.ceil(1000 * (3 * l - 10) / (20 * (n-1) + l/2 +250))


    print("bmax: ", b_max_reverse)
    print("a: ", a)
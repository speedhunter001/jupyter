# def prime_factors(n):
#     '''PRIME FACTORS: generates a list of prime factors for the number given
#     RETURNS: number(being factored), list(prime factors), count(how many loops to find factors, for optimization)
#     '''
#     num = n                         #number at the end
#     count = 1                       #optimization (to count iterations)
#     index = 0                       #index (to test)
#     t = [2, 3, 5, 7]                #list (to test)
#     f = []                          #prime factors list
#     while t[index] ** 2 <= n:
#         count += 1                  #increment (how many loops to find factors)
#         if len(t) == (index + 1):
#             t.append(t[-2] + 6)     #extend test list (as much as needed) [2, 3, 5, 7, 11, 13...]
#         if n % t[index]:            #if 0 does else (otherwise increments, or try next t[index])
#             index += 1              #increment index
#         else:
#             n = n // t[index]       #drop max number we are testing... (this should drastically shorten the loops)
#             f.append(t[index])      #append factor to list
#     if n > 1:
#         f.append(n)                 #add last factor...
#     # return num, f, f'count optimization: {count}'
#     return len(f)

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return len(factors)

with open('P3_input.txt') as f:

    for line_number, line in enumerate(f):
        if line_number == 0:
            continue

        j = int(line.strip())
        num = 0
        for i in range(2, 1000):
            if prime_factors(i) == j:
                num = i
                continue
        print("Case #{}: {} {}".format(line_number, j, num))



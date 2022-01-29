def prob(num,l):
    mylis = []
    n = len(l)
    n1 = int(n)
    f = int((sum(l))/2)
    l.sort()
    t1 = 0
    t2 = 0
    for i in l:
        if i >= f:
            y = l.index(i)
            p = l[y]
            l.remove(l[y])
            for j in range(round(num/2)):
                t1 += l[j]
            for k in range(round(num/2),len(l)):
                t2 += l[k] 
            t2 += p
            mylis.append(t1)
            mylis.append(t2)
            return mylis
        
    t1 = f
    t2 = sum(l) - f
    mylis.append(t1)
    mylis.append(t2)
    return mylis

# print(prob(3,[90,200,100]))
# print(prob(10,[2, 3, 10, 5, 8, 9, 7, 3, 5, 2]))
# print(prob(10, [1, 1, 1, 1, 1, 1, 1, 1, 1, 9]))
# print(prob(8, [87, 100, 28, 67, 68, 41, 67, 1]))
with open('P2_input.txt') as f:
    for line_number, line in enumerate(f):
        if line_number == 0:
            continue

        line = line.strip().split(' ')
        line = [int(i) for i in line]

        N = line[0]
        l = line[1:]
        
        res = prob(N, l)
        # res = [str(i) for i in res]
        # res = ' '.join(res)
        print("Case #{}: {} {}".format(line_number, res[0], res[1]))
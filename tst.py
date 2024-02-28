def fibbonaci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibbonaci(n - 1) + fibbonaci(n - 2)
    

for i in range(15, 30):
    print(i, fibbonaci(i))
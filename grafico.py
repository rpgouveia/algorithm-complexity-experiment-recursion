import matplotlib.pyplot as plt
import numpy as np

X = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500,
     2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000]
#X = [2.50, 5.00, 7.50, 10.00, 12.50, 15.00, 17.50, 20.00, 22.50, 25.00,
#     27.50, 30.00, 32.50, 35.00, 37.50, 40.00, 42.50, 45.00, 47.50, 50.00]
MS1	= [6,11,9,11,16,18,24,26,29,33,42,37,48,56,48,60,57,59,75,67]
MS2	= [3,6,6,9,13,14,19,18,20,23,29,31,37,42,36,61,42,45,63,50]
MS3	= [8,9,11,12,20,19,24,29,33,37,45,44,68,61,55,88,65,73,120,83]

x1  = np.polyfit(X,MS1, 2)
x2  = np.polyfit(X,MS2, 2)
x3  = np.polyfit(X,MS3, 2)

f1 = np.poly1d(x1)
f2 = np.poly1d(x2)
f3 = np.poly1d(x3)

# para ver como é a equacão é gerado pelo Python faça:
# print(f1)   # retire o comentário. O Expoente fica em uma linha e o restante da equação na próxima linha
# print(f2)   # retire o comentário. O Expoente fica em uma linha e o restante da equação na próxima linha
# print(f3)   # retire o comentário. O Expoente fica em uma linha e o restante da equação na próxima linha

s1 = 'f1(x) = ' + str(f1).split('\n')[1].replace(' x','x^2',1).replace(' x','x',1)
s2 = 'f2(x) = ' + str(f2).split('\n')[1].replace(' x','x^2',1).replace(' x','x',1)
s3 = 'f3(x) = ' + str(f3).split('\n')[1].replace(' x','x^2',1).replace(' x','x',1)

print(s1)
print(s2)
print(s3)

MS1t = []
MS2t = []
MS3t = []

XX = X.copy()
XX.append(XX[-1]+500)
XX.append(XX[-1]+500)

for x in XX:
    MS1t.append(f1(x))
    MS2t.append(f2(x))
    MS3t.append(f3(x))

plt.scatter(X, MS1)
plt.text(XX[-3]+50,MS1[-1]-3, 'MS1')
plt.scatter(X, MS2)
plt.text(XX[-3]+50,MS2[-1]-3, 'MS2')
plt.scatter(X, MS3)
plt.text(XX[-3]+50,MS3[-1]-3, 'MS3')
plt.scatter(XX, MS1t)
plt.text(XX[-1]-500,MS1t[-1]+3, s1)
plt.scatter(XX, MS2t)
plt.text(XX[-1]-500,MS2t[-1]+3, s2)
plt.scatter(XX, MS3t)
plt.text(XX[-1]-500,MS3t[-1]+3, s3)

plt.title("Desempenho de algoritmos de ordenação")
plt.xlabel("N (em centenas)")
plt.ylabel("t (em milisegundos)")
plt.plot(X, MS1,)
plt.plot(X, MS2,)
plt.plot(X, MS3,)
plt.plot(XX, MS1t,"b--")
plt.plot(XX, MS2t,"b--")
plt.plot(XX, MS3t,"b--")
plt.show()

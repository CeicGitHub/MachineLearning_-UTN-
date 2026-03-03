
#! ****************************DATOS***********************
X = [
    [0, 1],
    [9, 9],
    [1, 0]
]

y = [1, 0, 1]
w = [1.0, 0.0]      # w(0)
alpha = 0.0005       # tasa de aprendizaje
#! ****************************DATOS***********************

y_hat = []

for i in range(3):          # 3 filas
    valor = 0
    for j in range(2):      # 2 columnas
        valor = valor + X[i][j] * w[j]
    y_hat.append(valor)

print("y_hat =", y_hat)

e = []

for i in range(3):
    e.append(y[i] - y_hat[i])

print("error e =", e)

ErrorTotal1 = 0

for i in range(3):
    ErrorTotal1 = ErrorTotal1 + e[i] * e[i]

print("ErrorTotal1 =", ErrorTotal1)

grad = [0.0, 0.0]

for j in range(2):          # columnas
    suma = 0
    for i in range(3):      # filas
        suma = suma + X[i][j] * e[i]
    grad[j] = suma

print("X^T e =", grad)

for j in range(2):
    w[j] = w[j] + alpha * grad[j]

print("nuevos pesos w =", w)


y_hat2 = []

for i in range(3):
    valor = 0
    for j in range(2):
        valor = valor + X[i][j] * w[j]
    y_hat2.append(valor)

print("y_hat2 =", y_hat2)

e2 = []

for i in range(3):
    e2.append(y[i] - y_hat2[i])

ErrorTotal2 = 0
for i in range(3):
    ErrorTotal2 = ErrorTotal2 + e2[i] * e2[i]

print("error nuevo =", e2)
print("ErrorTotal2 =", ErrorTotal2)



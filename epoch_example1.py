
X = [1, 2, 3]
y = [2, 4, 6]   #! Queremos que el modelo aprenda que y = 2x
w = 0           
alpha = 0.1 

for epoch in range(5):   #todo: range(5) = 5 epochs
    print("Epoch:", epoch)
    
    for i in range(len(X)):
        y_hat = w * X[i]           # Predicción
        error = y[i] - y_hat       # Error
        w = w + alpha * error * X[i]  # Ajuste del peso
        
    print("Peso actualizado:", w)
    print("------------------")
    
    
    
    
    
    
#todo: EL USUARIO INGRESARA UN NUMERO Y ESE NUMERO SE ELEVARA A LA 5TA POTENCIA
#! APARTIR DEL NUMERO INGRESADO DEL USUARIO SE OBTENDRA AUTOMATICAMENTE LOS SIGUIENTES 10 NUMEROS
#! Y ESOS MISMOS 10 NUMEROS SE ELEVARAN A LA 5TA POTENCIA Y SE MOSTRARAN EN PANTALLA

#? PARA ELLO UTILIZARAN LA ESTRUCTURA DE CONTROL VISTA EN CLASE QUE ES EL CICLO FOR Y POW DE MATH.H
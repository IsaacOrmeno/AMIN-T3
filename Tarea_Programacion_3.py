import sys #se utilizo para el manejo de excepciones en la validacion de las entradas
import re #se utiliza para el manejo de las expresiones regulares involucradas en la validacion  de las entradas
import os #se utilizo para preguntar si el archivo por el cual se consulta se encuentra en el sistema
from pathlib import Path #se utiliza par aobtener la ruta relativa del archivo
import random  #se utiliza para obtener las numeros aleatorios involucrados tanto en la ruleta como en generacion de numeros enteros par el llenado de listas
import numpy as np #se utiliza para el manejo de arreglos y matrices


random.seed(1) #se utiliza para controlar la secuencia de numeros aleatorios involucrados en el algoritmo y para, en cierta medida, controlar la desviación estandar de los valores con respecto al óptimo de la solucion

def get_Knapsack(name_file):
    relative = Path(name_file) #se obtiene la ruta relativa del archivo
    absPath = relative.absolute() #se obtinene la ruta absoluta del archivo
    with open(absPath,'r') as file:  #se abre el archivo
        lines = file.readlines() #coordenates tiene ahora una lista  en donde cada elemento corresponde a una linea del archivo  
    lines = list(map( lambda f:f.strip(), lines)) #se eliminan los \n
    lines = list( map( lambda f:f.replace( '-','' ), lines ) )
    pattern = '[aA-zZ].*' #se crea un patron que puede ser una secuencia de caracteres
    lines = [re.sub(pattern,'',line) for line in lines] #se reemplaza la descripcion del archivo con espácios vacio
    lines = list(filter( lambda f:f!="", lines)) #se elimina los elementos de la lista que tienen espacios vacios
    string_lines = [ str(lines[i]) for i in range(len(lines)) ] #cada linea se convierte en string
    Elements = [ re.findall(r'\d+', element)   for element in string_lines ] #se buscan todos los numeros en string_lines
    knapsack_elements =  [ [ int(number)  for number in element  ] for element in Elements ]  #se convierten a entero los números presentes en Elements
    file.close() #se cierra el archivo
      
    with open(absPath,'r') as file:  #se abre el archivo
        lines = file.readlines() #coordenates tiene ahora una lista  en donde cada elemento corresponde a una linea del archivo 
    test_features = [ re.findall(r'[aA-zZ]+\s+\d+', line) for line in lines ] 
    test_features= list(filter(None, test_features)) #se elimina los elementos de la lista que tienen espacios vacios
    Knapsack_Features = {} #se crea un diccionario
    Knapsack_Features["amount_items"] = [] #este arreglo dentro del diccionario guardara la cantidad de elementos que hay por cada test
    Knapsack_Features["knapsack_capacity"] = [] #este arreglo dentro del diccionario guardara la capacidad de la mochila en cada test
    Knapsack_Features["best_value"] = [] #este arreglo en el diccionario guardara el mejor valor encontrado para cada test
    Knapsack_Features["test_time"] = [] #ese arreglo guardara el mejor tiempo obtenido en encontrar una solución optima
     
    for i in range(0,len(test_features),4): #for que ira guardando los elementos del archivo csv
        Knapsack_Features["amount_items"].append(test_features[0+i]) #se  guardan la cantidad de elementos por cada test
        Knapsack_Features["knapsack_capacity"].append(test_features[1+i]) #se guara la capacidad de cada mochila
        Knapsack_Features["best_value"].append(test_features[2+i]) #se guarda el mejor valor encontrado para ese test
        Knapsack_Features["test_time"].append(test_features[3+i]) #se guarda el tiempo en encontrar la mejor solucion encontrada
    for i in range(len(Knapsack_Features["amount_items"])): #por cada elemento dentro de amount:items
        Knapsack_Features["amount_items"][i] = [int(s) for s in Knapsack_Features["amount_items"][i][0].split() if s.isdigit()] #rescatamos la cantidad de elementos por test como un valor lista de enteros
        Knapsack_Features["knapsack_capacity"][i] = [int(s) for s in Knapsack_Features["knapsack_capacity"][i][0].split() if s.isdigit()] #rescatamos la capacidad de la mochila s por test como un valor lista de enteros
        Knapsack_Features["best_value"][i] = [int(s) for s in Knapsack_Features["best_value"][i][0].split() if s.isdigit()] #rescatamos el mejor valor encontrado por test como un valor lista de enteros
        Knapsack_Features["test_time"][i] = [int(s) for s in Knapsack_Features["test_time"][i][0].split() if s.isdigit()] #rescatamos el tiempo en encontrar la mejor solucion por test como un valor lista de enteros
        Knapsack_Features["amount_items"][i] = Knapsack_Features["amount_items"][i][0]  #se rescata la cantidad de elementos por test como un valor entero y se guarda en la lista del diccionario
        Knapsack_Features["knapsack_capacity"][i] = Knapsack_Features["knapsack_capacity"][i][0]  #se rescata la capacidad de la mochila por test como un valor entero y se guarda en la lista del diccionario
        Knapsack_Features["best_value"][i] = Knapsack_Features["best_value"][i][0]  #se rescata el mejor valor encontrado por test como un valor entero y se guarda en la lista del diccionario
        Knapsack_Features["test_time"][i] = Knapsack_Features["test_time"][i][0]  #se rescata el tiempo en encontrar la mejor solucion por test como un valor entero y se guarda en la lista del diccionario
        file.close()
             
    knapsack_elements = [knapsack_elements[50*i:50*(i+1)] for i in range(int(len(knapsack_elements)/50))] #se divide la lista conteniendo todos los elementos de los test ['number_item', 'cost', 'weight', 'isInSolution'] en sublistas con los elementos correspondientes a cada test  
    
    Knapsack_Features["knapsack_tests"] = {} #se crea una tabla hash dentro de la tabla hash principal para almacenara los elementos de cada test
    
    Knapsack_Features["knapsack_tests"]["items"] = [] #se crea una lista dentro de la subtabla hash que albergara el numero del item al que hace referencia en cada test
    Knapsack_Features["knapsack_tests"]["costs"] = [] #se crea una sub abla hash que albergara los costos de cada elemento de cada test
    Knapsack_Features["knapsack_tests"]["weights"] = []
    Knapsack_Features["knapsack_tests"]["isInSolution"] = []

    for i in range( len(knapsack_elements) ): #por cada elemento en la lista de elementos
        knapsack_items = [] #se limpia la lista de elementos para que este vacia
        knapsack_costs = []  #se limpia la lista de costos para que este vacia
        knapsack_weights = [] #se limpia la lista de pesos para que este vacia
        knapsack_isInSolution = [] #se limpia la lista de pertenecedores a la solucion  para que este vacia
        for j in range(len(knapsack_elements[i])): #por cada subelmento en los elementos de la lista
            knapsack_items.append( knapsack_elements[i][j][0] )  #añadimos a la lista solo los elementos que hacen referencia al identificados del item
            knapsack_costs.append( knapsack_elements[i][j][1] )  #añadimos a la lista solo los elementos que hacen referencia al icosto del item
            knapsack_weights.append( knapsack_elements[i][j][2] )  #añadimos a la lista solo los elementos que hacen referencia al peso del item
            knapsack_isInSolution.append( knapsack_elements[i][j][3] ) #añadimos a la lista solo los elementos que hacen referencia a la pertenencia a la solucion del item
        Knapsack_Features["knapsack_tests"]["items"].append(knapsack_items) #se añade dicha lista a la sub tabla hash
        Knapsack_Features["knapsack_tests"]["costs"].append(knapsack_costs) #se añade dicha lista a la sub tabla hash
        Knapsack_Features["knapsack_tests"]["weights"].append(knapsack_weights) #se añade dicha lista a la sub tabla hash
        Knapsack_Features["knapsack_tests"]["isInSolution"].append(knapsack_isInSolution) #se añade dicha lista a la sub tabla hash

    return Knapsack_Features

def get_parameters():
    #Entrada del nombre del archivo y manejo de excepciones 
    #name_file = "knapPI_1_50_1000"
    name_file = sys.argv[1] #se obtiene la ruta absoluta del archivo
    if re.findall('([aA-zZ]*[0-9]*)*.\..*', name_file): #se pregunta si el archivo posee extensión
            sys.exit("El nombre del archivo no debe tener extensión Ej: Si el Archivo es 'berlin52.txt', usted debe ingresar 'berlin52'\n Intente Nuevamente")
    else: 
        name_file = name_file + ".csv" #se añade la extension txt al archivo
        if os.path.exists(name_file): #Preguntamos si el archivo existe
            pass #no se hace nada
        else:
            message = '    El Archivo: '+ name_file +'  no se encuentra en ningún directorio. Asegurese de estar escribiendo el nombre correctamente'
            sys.exit(message) #se imprime el mensaje detallado en la linea anterior       
    
    #number_iterations = "1000"
    number_iterations = sys.argv[2] #ingreso de la cantidad de iteraciones
    if re.findall('[aA-zZ]', str(number_iterations)): #preguntamos si la entrada es una secuencia de caracteres
        sys.exit("El Número de iteraciones debe ser un Número, Intentelo Nuevamente")
    else: 
        if re.findall('[0-9]*\.[0-9]*',str(number_iterations)): #preguntamos si la entrada es un decimal
            message = 'El Número de  Iteraciones debe ser un Número Entero'
            sys.exit(message)
        elif int(number_iterations) <= 0:           #preguntamos si el entero ingresado es menor o igual que cero
            message = "\033[4;35m"+'El Número de  Iteraciones debe ser mayor que 0'
            sys.exit(message)
        else:
            number_iterations = int(number_iterations) #cambiamos el tipo de dato de la entrada que era str a int
   
    #tau = "1.8"
    tau = sys.argv[3] #se ingresa heuristic_coefficient
    if re.findall('[aA-zZ]', str(tau)): #pregunta si la entrada no es un numero
        sys.exit("Tau debe ser un Número, Intentelo Nuevamente")
    else: 
        if re.findall('[0-9]*\.[0-9]*',str(tau)): #pregunta si el numero ingresado es decimal
            tau = float(tau)
            if tau<=0: #se pregunta si la entrada  es negativa
                sys.exit("Tau debe ser Positivo")
            else:
                pass
        elif isinstance(int(tau), int): #se pregunta si el numero es un entero
            sys.exit("Tau debe ser un Número Decimal, Intentelo Nuevamente")
            if int(tau)<=0: #se pregunta si el numero entero ingresado es positivo
                sys.exit("Tau debe ser Positivo")
    
    return name_file, number_iterations, tau #se retorna el nombre del archivo solo si es valido

def create_initial_solution(capacity, weights, costs): #se crea una solucion inicial
    cost = 0 #se inicializa la variable que guardara el costo total de la solucion
    weight = 0 #se inicializa la variable que guardara el peso total de la mochila
    weights_costs = list() #se crea una lista que albergará los elementos de la mochila del tipo  (peso, valor)
    pesos = weights.copy() #se crea una copia de la lista  que es copia de la lista que alberga los pesos
    costos = costs.copy() #se crea una lista que es copia de la lista que albrca los calores de los elementos de la mochila
    while pesos:  #mientras pesos no este vacia
        min_value = min(pesos) #encontramos el menor peso 
        min_index = pesos.index(min_value) #se almacena el indice del menor peso encontrado
        if weight+min_value <= capacity:  #si la suma de los pesos mas el menor peso actual es menor que la capacidad de la mochila
            weight += min_value #se suma el minimo peso actual encontrado a la suma general de pesos
            cost += costos[min_index] #se suma el valor del minimo elemento encontrado
            weights_costs.append((pesos[min_index], costos[min_index])) #se añade el elemento en la forma (peso, valor) a la lista de los elementos en la mochila
        pesos.pop(min_index) #se elimina el minimo peso encontrado en esta iteracion de la lista copia de los pesos
        costos.pop(min_index) #se elimina el valor del minimo pesos encontrado en esta iteracion de la lista copia de los valores
    return weights_costs, cost #se retorna la "mochila" con los elementos (peso,valor) en ella y el valor obtenido por esta solucion

def set_probabilities(n, tau): #funcion para calcular las probabilidades según la ecuación 1
    return [ pow(i,-tau)  for i in range(1,n+1) ] #se calculan las probabilidades según la ecuación 1 

def rank_fitness(current_knapsack): # funcion para calcular el fitness de cada elemento de la mochila
    fitness = [] 
    fitness = [ (i, current_knapsack_element, current_knapsack_element[1]/current_knapsack_element[0]) for i, current_knapsack_element in enumerate(current_knapsack) ]
    #se almacena en fitness el indice del elemento, el elemento y el valor del fitness que en este caso es valor/peso
    fitness = sorted(fitness, key=lambda x: x[2]) #se ordena el fitness con respecto al valor de este 
    return fitness

def select_worst_element(fitness, weights, costs): #funcion para encontrar el peor elemento en la mochila
    worst = fitness[0] #debido a que el fitness se ordeno de tal manera que el peor quedara primero, se sabe que el peor elemento es el primero en la lista de fitness
    worst_element = worst[1] #seleccionamos de fitness el elemento de la mochila con formato (peso, valor)
    worst_index = worst[0] #se almacena el indice del peor elemento
    Worst = {} #creamos un diccionario para almacenar las caractersticas del peor elemento
    Worst["element"] = worst_element #en Worst se almacena el peor elemento con formato (peso, valor)
    Worst["index"] = worst_index  #en Worst también se almacena el indice del peor elemento de la mochila
    return Worst

def roulette(probabilities):  #función que crea la Ruleta en base a las probabilidades 
    total = sum(probabilities)     #se suman todas las probabilidades
    roulette = np.cumsum( [ prob/total for prob in probabilities ] ) #se forma la ruleta con la probabilidad acumulada 
    return roulette

def calculate_weight(knapsack): #funcion para calcular el peso de una mochila
    weight =  0 #se inicializa la variable weight
    for i in range(len(knapsack)): #se itera desde 0 hasta la cantidad de elementos de la mochila-1
        weight += knapsack[i][0]  #sumamos todos los pesos de la mochila
    return weight

def calculate_cost(knapsack): #función para calcular el valor maximo alcanzado en una mocchila
    cost =  0 #se inicializa la variable cost
    for i in range(len(knapsack)): #se itera desde 0 hasta la cantidad de elementos en la mochila -1 
        cost += knapsack[i][1] #se suman todos los valores de cada elemento en la mochila
    return cost

def var_knapsack(probabilities, fitness, weights, costs, Worst, current_knapsack, capacity): #funcion para reemplazar el peor elemento de la mochila por uno nuevo
    current_knapsack_copy = current_knapsack.copy() #se crea una copia de la mochila
    roulette_wheel = roulette(probabilities) #se forma la ruleta
    flag = False #setiamos una bandera en falso
    while flag == False: #mientras dicha bandera sea  False
        spin_wheel= random.uniform(roulette_wheel[0], 1) #giramos la ruleta
        for i in range(len(roulette_wheel)): #se itera entre 0 i la cantidad de elementos en la ruleta
            if spin_wheel > roulette_wheel[i] and (weights[i], costs[i]) not in current_knapsack_copy: #si el numero que salio en la ruleta es mayor que a la seccion de la ruleta apropiada y el elemento a añadir no esta ya en la mochila
                added_element = (weights[i],costs[i]) #almacenamos el nuevo elemento que intercambiaremos por el peor de la mochila
                flag=True #setiemos flag en true ya que ya se encontro un elemento nuevo para añadir
    replaced_index = current_knapsack_copy.index(fitness[0][1])  #almacenamos el indicce del elemento en la mochikla que vamos a intercambiar
    current_knapsack_copy[replaced_index] = added_element #intercambiamos el peor elemento por el nuevo elemento pero en una mochila que es copia de la original
    
    weight_copy = calculate_weight(current_knapsack_copy) #almacenamos el peso total de la mochila con el el elemento nuevo añadido

    if weight_copy < capacity : #si el peso total de la mochila con el nuevo elemento es menor que la capacidad de la mochila
        return current_knapsack_copy #se retorna la copia de la mochila como si fuera la verdadera mochila
    else: #si el peso de la mochila con el elemento intercambiado  supera la capacidad de la mochila
        return current_knapsack #deshacemos ese cambio


def search(capacity, weights, costs, n, max_iterations, tau): #función para obtener la meor mochila
    current = {} #se inicializa un diccionario
    current["current_knapsack"], current["current_cost"]  = create_initial_solution(capacity, weights, costs)  #en el diccionario almacenamos la mochila inicial y el valor total de dicha mochila
    best = current #inicialmente la mejor mochila es la actual
    probabilities = set_probabilities(n,tau) #calculamos las probabilidades según la ecuación 1
    
    for i in range(max_iterations): #se itera un maximo de iteraciones definido por el usuario
        fitness = rank_fitness(current["current_knapsack"]) #calculamos el fitness de la mochila actual
        Worst = {} #creamos un diccionario para almacenar las caracteristicas del futuro peor elemento 
        Worst = select_worst_element(fitness, weights, costs) #se almacenan las caracteristicas del peor elemento
        current["current_knapsack"] = var_knapsack(probabilities, fitness, weights, costs, Worst, current["current_knapsack"], capacity) #se asigna la nueva mochila
        if calculate_cost(current["current_knapsack"])>best["current_cost"]: #si el valor de la mochila nueva es mayor que la anterior
            best = { "current_knapsack": current["current_knapsack"], "current_cost": calculate_cost(current["current_knapsack"]) }  #esta nueva mochila es la mejor
    return best 
    
    
name_file, max_iterations, tau = get_parameters() #se obtiene el nombre del archivo valido
Knapsack_Features = get_Knapsack(name_file) #se obtienen todas las caracteristicas asociadas al problema de la mochila y se agrupan en una tabla hash o dictionario  
best = search( Knapsack_Features["knapsack_capacity"][0],Knapsack_Features["knapsack_tests"]["weights"][0],Knapsack_Features["knapsack_tests"]["costs"][0] , Knapsack_Features["amount_items"][0], max_iterations, tau  )   #obtenemos la mejor mochila
print("Elementos en la mochila: (PESO, VALOR)")
print(str(best["current_knapsack"]))
print("Valor Total:  "+str(best["current_cost"]))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
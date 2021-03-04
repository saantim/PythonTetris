import csv
from random import choice

ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZA = 1
SUPERFICIE = 2

RUTA_TECLAS = "teclas.txt"
RUTA_PIEZAS = "piezas.txt"

def importar_piezas(ruta_piezas):
    '''
    Recibe un archivo con las coordenadas de las piezas y sus rotaciones.
    Genera dos listas, una con las piezas y sus rotaciones y otro con las piezas en sus posicion inicial
    ''' 
    rotaciones = []
    piezas = []

    with open(ruta_piezas) as f:
        csv_reader = csv.reader(f, delimiter= " ")
        for linea in csv_reader:
            posiciones = ()
            for posicion in linea:
                pieza = ()
                for coor in posicion.split(";"): 
                    if len(coor.split(",")) == 2:
                        x = int(coor.split(",")[0])
                        y = int(coor.split(",")[1])
                        pieza += (x,y),
                if pieza == ():
                    continue
                posiciones += pieza,
            rotaciones.append(posiciones)    
    for pieza in rotaciones:
        piezas.append(pieza[0])
    
    return piezas, rotaciones

    
#Para el tetris-test.py es necesario habilitar la linea de abajo:
#importar_piezas("piezas.txt")

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    piezas, _ = importar_piezas(RUTA_PIEZAS)
    if pieza == None:
        #generar pieza aleatorea.
        nueva_pieza = choice(piezas)

    else:
        #generar pieza indicada
        nueva_pieza = piezas[pieza]
    
    return tuple(nueva_pieza)




def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    
    #pieza_a_trasladar = PIEZAS[pieza]
    pieza_trasladada = ()
    for coordenada in pieza:
        desplazamiento_en_x = coordenada[0] + dx
        desplazamiento_en_y = coordenada[1] + dy
        coordenada = (desplazamiento_en_x,desplazamiento_en_y) 
        
        pieza_trasladada += (coordenada),
    return pieza_trasladada

def centrar_pieza(pieza):
    '''
    Recibe una pieza y la ubica en el centro del tablero
    '''
    return trasladar_pieza(pieza, ANCHO_JUEGO // 2, 0)

 
def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).

    Coordenadas en grilla: Vacias = 0, Ficha en juego = 1, Superficie consolidada = 2
    """
    tetris_grilla = []
    for fila in range(ALTO_JUEGO):
        tetris_grilla.append([])
        for columna in range(ANCHO_JUEGO):
            tetris_grilla[fila].append(0)

    return [tetris_grilla, centrar_pieza(pieza_inicial)]



def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (len(juego[0][1]),len(juego[0]))


def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[1]


def consolidar_superficie(juego): 
    '''
    Recibe una grilla y una pieza. Coloca 1's en las coordenadas correspondientes a la grilla con pieza en 0,0
    '''
    grilla = juego[0]
    ficha = juego[1]
    for coordenadas in ficha:
        grilla[coordenadas[1]][coordenadas[0]] = SUPERFICIE
    
    return [grilla, ficha]



def buscar_elemento(juego,elemento):
    '''
    Se debe ingresar un Juego y un Elemento a buscar.
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por el elemento ingresado.
    '''
    grilla = juego[0]
    coor_superficie_actual = []
    for f in range(len(grilla)):
            for c in range(len(grilla[f])):
                if grilla[f][c] == elemento:
                    coor_superficie_actual.append((c,f))

    return tuple(coor_superficie_actual)


def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[0][y][x] == SUPERFICIE


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    #DERECHA(=+1) o IZQUIERDA(=-1)
    pieza_movida = trasladar_pieza(juego[1],direccion,0)    
    
    for coordenada in pieza_movida:                 # Si la pieza se sale del juego, devuelvo el mismo juego recibido
        if coordenada[0] > ANCHO_JUEGO-1 or coordenada[0] < 0:
            return juego
        if hay_superficie(juego, coordenada[0], coordenada[1]): 
            return juego    
    
    return [juego[0],pieza_movida]

def buscar_rotacion(pieza, rotaciones):
    '''
    Recibe una pieza y una lista de tuplas con piezas y sus rotaciones.
    Devuelve la proxima rotacion de la pieza recibida
    '''
    for rotaciones_pieza in rotaciones:
        if pieza in rotaciones_pieza:
            if pieza == rotaciones_pieza[len(rotaciones_pieza)-1]:
                return rotaciones_pieza[0]
            return rotaciones_pieza[rotaciones_pieza.index(pieza)+1]        



def rotar_pieza(juego, rotaciones):
    '''
    Recibe un Juego y sus Rotaciones, se translada su ficha en juego a la posicion incial y se busca su siguiente rotacione
    Devuelve el nuevo juego con la ficha rotada en su lugar de origen
    '''
    pieza_ordenada = sorted(juego[1])
    primer_posicion = pieza_ordenada[0]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -primer_posicion[0], -primer_posicion[1])
    siguiente_rotacion = buscar_rotacion(pieza_en_origen, rotaciones)
    
    pieza_rotada = trasladar_pieza(siguiente_rotacion, primer_posicion[0], primer_posicion[1])
    
    libres = buscar_elemento(juego,0)

    for coor in pieza_rotada:
        if coor not in libres:
            return juego
    juego[1] = pieza_rotada
    
    return juego



def puede_descender(juego):
    '''
    Recibe un juego.
    Devuelve True si la ficha en juego puede descender una posicion, si no puede devuelve False
    '''
    ficha_descendida = trasladar_pieza(juego[1],0,1)
    libres = buscar_elemento(juego,0)

    for coor in ficha_descendida:
        if coor not in libres:
            return False
    return True



def eliminar_lineas_y_descender(juego):
    '''
    Recibe el juego. Si encuentra lineas completas las elimina y devuelve el juego con esas lineas llenas de ceros.
    Si no encuentra lineas completas devuelve el mismo juego recibido.
    '''
    for f in range(len(juego[0])):
        if all(n == 2 for n in juego[0][f]):
            juego[0].pop(f)
            juego[0].insert(0,[0] * ANCHO_JUEGO)   #agrega fila completa de 0's arriba de todo

    return juego


def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    

    if terminado(juego):            #Si esta terminado debe devolver el mismo juego.
        return juego, False


    cambiar_pieza = False

    if puede_descender(juego):                                          #Si no colisiona >>> devuelve nuevo juego
        return [ juego[0], trasladar_pieza(juego[1],0,1) ] , False

    consolidar_superficie(juego)         #si colisiona :  consolidar pieza con sup.
    eliminar_lineas_y_descender(juego)  # eliminar linea completas
    juego[1] = centrar_pieza(siguiente_pieza)   #cambiar la ficha

    cambiar_pieza = True

    return juego, cambiar_pieza

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    ficha = juego[1]    
    libres = buscar_elemento(juego,0)

    for coor in ficha:
        if coor not in libres:
            return True
    return False

def cargar_leaderboard():
    '''
    Busca el archivo del TOP10 en la carpeta
    Devuelve la tabla de posiciones
    '''
    leaderboard = [] 
    with open("leaderboard.txt") as f:
        csv_reader = csv.reader(f)
        for nombre, puntaje in csv_reader:
            leaderboard.append((nombre,int(puntaje)))
    return leaderboard

def guardar_leaderboard(tabla_posiciones):
    '''
    Escribe el archivo leaderboard en la carpeta con la info de la Lista recibida
    '''
    leaderboard = tabla_posiciones
    with open("leaderboard.txt", "w") as f_puntos:
        csv_writer = csv.writer(f_puntos)
        for nom_puntos in leaderboard:
            csv_writer.writerow(nom_puntos)


def entra_en_top10(tabla_posiciones, puntaje):
    '''
    Recibe una tabla de posiciones, un puntaje y evalua si este debe ser incluido en la tabla recibida
    '''
    if  len(tabla_posiciones) < 10 or puntaje >= tabla_posiciones[-1][1]  :
        return True
    return False

def sumar_leaderboard(leaderboard, nombre, puntaje):
    '''
    Recibe la tabla de posiciones, un nombre y un puntaje.
    Devuelve el leaderboard actualizado
    '''
    if leaderboard == []: 
        leaderboard.append((nombre, puntaje))
        return leaderboard
    elif puntaje > leaderboard[-1][1]:
        if len(leaderboard) == 10:
            leaderboard.pop(9)
        for p in range(len(leaderboard)):
            if puntaje > leaderboard[p][1]:
                leaderboard.insert(p, (nombre, puntaje))
                return leaderboard
        return leaderboard
    elif len(leaderboard) < 10:
        leaderboard.append((nombre, puntaje))
        return leaderboard

def guardar_partida(juego, siguiente_pieza, puntaje_actual):
    '''
    Recibe [juego, pieza en juego], pieza siguiente y el puntaje actual del juego
    Se guarda la informacion en el archivo "juego_guardado" en la carpeta del juego 
    '''
    with open("juego_guardado.txt", "w") as f:
        for fila in juego[0]:
            for c in fila:
                f.write(str(c))
        f.write("\n")
        
        for coor in juego[1]:
            for i in coor:
                f.write(str(i)+",")
        f.write("\n")
    
        for coor in siguiente_pieza:
            for i in coor:
                f.write(str(i)+",")
        
        f.write("\n")

        f.write(str(puntaje_actual))


def cargar_partida():
    '''
    Se busca el archivo "juego_guardado" y se levanta la informacion
    Devuelve el juego guardado anteriormente, la ficha siguiente y el puntaje cargado
    '''
    tetris_grilla = []
    pieza = ()
    siguiente = ()
    aux = -1
 
    with open("juego_guardado.txt") as f:
        juego_cargado = f.readline().rstrip()
        pieza_cargada = f.readline().rstrip()[:-1].split(",")
        pieza_siguiente_cargada = f.readline().rstrip()[:-1].split(",")
        puntaje_cargado = int(f.readline().rstrip())
    

    for c in range(1, len(pieza_cargada) ,2 ):
        pieza += (int(pieza_cargada[c-1]), int(pieza_cargada[c])),

    for c in range(1, len(pieza_siguiente_cargada) ,2 ):
        siguiente += (int(pieza_siguiente_cargada[c-1]), int(pieza_siguiente_cargada[c])),

    for c in range(len(juego_cargado)):
        if c % ANCHO_JUEGO == 0 :
            tetris_grilla.append([])
            aux += 1
        tetris_grilla[aux].append(int(juego_cargado[c]))


    return [tetris_grilla, pieza], siguiente, puntaje_cargado




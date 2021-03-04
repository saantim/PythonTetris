import gamelib
import tetris

ANCHO_PANT = 800
ALTO_PANT = 600

TAM_PIEZA = (ANCHO_PANT/ALTO_PANT) * 18

TABLERO_x1 = ANCHO_PANT/2 - (TAM_PIEZA * tetris.ANCHO_JUEGO) /2
TABLERO_y1 = ALTO_PANT/2 - (TAM_PIEZA * tetris.ALTO_JUEGO) /2

########## FUNCIONES DE DISENIO:

def cuadrado_pieza(coordenada_pieza, color):
    '''
    Recibe la coordenada de una pieza y el color.
    La dibuja en el tablero segun su posicion y su tamanio relativo al tamanio de la pantalla
    '''
    x, y = coordenada_pieza
    gamelib.draw_rectangle(TABLERO_x1 + (x * TAM_PIEZA)  , TABLERO_y1 + (y * TAM_PIEZA),\
                                           TABLERO_x1 + TAM_PIEZA  + (TAM_PIEZA * x), TABLERO_y1 + TAM_PIEZA + (TAM_PIEZA * y), fill = color)

def tablero(puntaje_actual):
    '''
    Dibuja el tablero relativo al tamanio de la pantalla y el puntaje en el corner derecho
    '''
    gamelib.draw_image("images/tetris_4.gif",0,0)
    gamelib.draw_rectangle( TABLERO_x1 - 5 , TABLERO_y1 - 5,\
                                        TABLERO_x1 + 5 + TAM_PIEZA * tetris.ANCHO_JUEGO, TABLERO_y1 + 5 + TAM_PIEZA * tetris.ALTO_JUEGO, fill = "grey")   
    gamelib.draw_rectangle( TABLERO_x1, TABLERO_y1,\
                                        TABLERO_x1 + TAM_PIEZA * tetris.ANCHO_JUEGO, TABLERO_y1 + TAM_PIEZA * tetris.ALTO_JUEGO, fill = "black") 
    ## Puntaje!:
    gamelib.draw_text("Puntaje:", TABLERO_x1 - TAM_PIEZA*2, TABLERO_y1 - TAM_PIEZA)
    gamelib.draw_text(puntaje_actual, TABLERO_x1 - TAM_PIEZA, TABLERO_y1)

def terminado():
    '''
    Dibuja el titulo de "Juego Terminado" en el centro de la pantalla
    '''
    gamelib.draw_text("Juego Terminado!", ANCHO_PANT/2, ALTO_PANT/6, size= int(TAM_PIEZA * 1.5), fill = "pink")
    
def top_puntajes(leaderboard, puntaje):
    '''
    Recibe un puntaje y evalua si entra en el TOP10.
    Si entra en el top 10 se pide el nombre al Usuario, se suma el nombre, puntaje al TOP10 y se guarda en el archivo
    '''
    nombre = ""

    if tetris.entra_en_top10(leaderboard, puntaje):
        while nombre == "" or nombre == None:
            nombre = gamelib.input(f"Puntaje {puntaje} es TOP10, Ingrese su nombre: ")
        leaderboard = tetris.sumar_leaderboard(leaderboard, nombre, puntaje)
        tetris.guardar_leaderboard(leaderboard)
        return leaderboard, True
    
    return leaderboard, False
    
def imprimir_puntajes(leaderboard):
    '''
    Imprime los nombre,puntaje de los TOP10
    '''
    linea = 0
    gamelib.draw_text("Puntajes TOP 10!",ANCHO_PANT/2, ALTO_PANT/4, size = int(TAM_PIEZA))
    for nombre, puntaje in leaderboard:
        linea += 1
        gamelib.draw_text(f'{linea}° {nombre} - {puntaje}',ANCHO_PANT/2 ,ALTO_PANT/4 + (linea * TAM_PIEZA), size = int(TAM_PIEZA) )


def piezas(juego, siguiente):
    '''
    Recibe un juego y la ficha siguiente.
    Del juego se dibuja la superficie consolidada y la ficha en juego.
    Por otra parte se dibuja la ficha siguiente en el corner superior derecho
    '''
    grilla, pieza = juego
    superficie = tetris.buscar_elemento(juego,tetris.SUPERFICIE)

    # Dibujar cuadrados para ficha en juego
    for coordenada in pieza:
        cuadrado_pieza(coordenada, "blue")
    
    # Dibujar cuadrados para superficie
    for coordenada in superficie:
        cuadrado_pieza(coordenada, "green")
    
    # Dibujar siguiente pieza en un costado:
    gamelib.draw_text("Siguiente:",  TABLERO_x1 + (TAM_PIEZA + 1)* tetris.ANCHO_JUEGO , TABLERO_y1, anchor="sw", fill="white")
    for coordenada in siguiente:
        x, y = coordenada
        gamelib.draw_rectangle( TABLERO_x1 + TAM_PIEZA * tetris.ANCHO_JUEGO + TAM_PIEZA + (x * TAM_PIEZA)  , TABLERO_y1 + (y * TAM_PIEZA),\
                                  TABLERO_x1 + TAM_PIEZA * tetris.ANCHO_JUEGO + TAM_PIEZA + TAM_PIEZA + (TAM_PIEZA * x), TABLERO_y1 + TAM_PIEZA + (TAM_PIEZA * y), fill = "white")





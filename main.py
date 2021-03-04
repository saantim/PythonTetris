import tetris
import grafico
import gamelib
import csv

ESPERA_DESCENDER = 8

def importar_teclas(ruta_teclas):
    '''
    Recibe archivo del tipo "w = ROTAR" e importa las teclas para poder jugar. 
    '''
    teclas = {}
    with open(ruta_teclas) as f:
        csv_reader = csv.reader(f, delimiter= "=")
        for linea in csv_reader:
            if not linea:
                continue
            tecla, movimiento = linea[0].rstrip(), linea[1].lstrip()
            teclas[movimiento] = teclas.get(movimiento, [])
            teclas[movimiento].append(tecla)
    return teclas

def actualizar_movimiento(juego, tecla_recibida, teclas):
    '''
    Recibe un juego, una tecla_recibida presionada y la lista de teclas, y devuelve el nuevo estado de juego 
    evaluado en los movimientos de Rotar, Mover izquierda o mover derecha.
    '''
    _, rotaciones = tetris.importar_piezas(tetris.RUTA_PIEZAS)

    if tecla_recibida in teclas["ROTAR"]:
        return tetris.rotar_pieza(juego, rotaciones)
    if tecla_recibida in teclas["IZQUIERDA"]:
        return tetris.mover(juego, tetris.IZQUIERDA)
    if tecla_recibida in teclas["DERECHA"]:
        return tetris.mover(juego, tetris.DERECHA)
    return juego

def main():
    '''
    Funcion principal del juego. Mantiene la interfaz grafica y evalua las teclas recibidas y si el juego esta terminado 
    '''
    # Inicializar el estado del juego
    tetris.importar_piezas(tetris.RUTA_PIEZAS)
    

    juego = tetris.crear_juego(tetris.generar_pieza())
    salir = False

    puntaje_juego = 0
    ingreso_puntaje = False

    cambiar_ficha = False
    siguiente_ficha = tetris.generar_pieza()
    
    gamelib.resize(grafico.ANCHO_PANT, grafico.ALTO_PANT)
    gamelib.play_sound("sound/bradinsky.wav")

    teclas = importar_teclas(tetris.RUTA_TECLAS)

    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        gamelib.title("TETRIS")
        # Dibujar la pantalla
        grafico.tablero(puntaje_juego)
        grafico.piezas(juego, siguiente_ficha)

        if salir:
            break

        if tetris.terminado(juego):
            grafico.terminado()
            if not ingreso_puntaje:
                leaderboard = tetris.cargar_leaderboard()
                leaderboard, ingreso_puntaje = grafico.top_puntajes(leaderboard, puntaje_juego)
            grafico.imprimir_puntajes(leaderboard)

        gamelib.draw_end()
        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
            # Actualizar el juego, según la tecla presionada ( ROTAR ( w) , MOVER izq der abajo, guardar, cargar )
                
                juego = actualizar_movimiento(juego, tecla, teclas)
                
                if tecla in teclas["GUARDAR"]:
                    tetris.guardar_partida(juego, siguiente_ficha, puntaje_juego)
                if tecla in teclas["CARGAR"]:
                    juego, siguiente_ficha, puntaje_juego = tetris.cargar_partida()
                if tecla in teclas["DESCENDER"]:
                    juego, cambiar_ficha = tetris.avanzar(juego, siguiente_ficha)
                    puntaje_juego += 1
                    continue
                if tecla in teclas["SALIR"]:
                    salir = True

        timer_bajar -= 1 
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente

            if cambiar_ficha == True:
                siguiente_ficha = tetris.generar_pieza()
            juego, cambiar_ficha = tetris.avanzar(juego, siguiente_ficha)
            if not tetris.terminado(juego):
                puntaje_juego += 1

gamelib.init(main)
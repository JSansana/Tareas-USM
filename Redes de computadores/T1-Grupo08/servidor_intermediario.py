import socket as skt

##DEFINICION DEL SERVIDOR INTERMEDIARIO

Puerto_Servidor = 50002

serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

serverSocket.bind(('',Puerto_Servidor))

#Servidor recibe de a 1 stream de bytes
serverSocket.listen(1)

#Mientras se esté dentro del juego , será True, al escoger salir, será False
dentro = True
#Si el servidor cachipun acepta, entonces el juego será True


print("Bienvenido al servidor intemediario!")
while True:
    clientSocket, clientAddr = serverSocket.accept()
    while dentro:
        #Variables que guardaran los puntos del bot y del humano
        puntos_bot = 0
        puntos_cliente = 0
        juego = True
        msg = clientSocket.recv(2048).decode()
        print(msg)
        Puerto_Cachipun = 50001 # Puerto Cachipun
        serverAddr = 'localhost'
        cachipunSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
        #Se escoge la opción jugar partida
        if msg == "EMPEZAR":
            print("Jugador ha solicitado una partida")


            #Envía mensaje START al servidor cachipun
            cachipunSocket.sendto("START".encode(), (serverAddr, Puerto_Cachipun))

            #Se recibe el mensaje del servidor cachipun esperando una respuesta afirmativa o negativa
            msg, addr = cachipunSocket.recvfrom(2048)

            #No hay disponibilidad de partidas
            if msg.decode() == "ERROR":
                respuesta = "ERROR"
                clientSocket.send(respuesta.encode())

            #Hay disponibilidad de partidas y el mensaje recibido de cachipún es el puerto en el que se jugaran las partidas
            elif msg.decode() != "ERROR":
                respuesta = "GO"
                clientSocket.send(respuesta.encode()) # Se le envía
                #Nuevo puerto creado aleatoriamente
                Puerto_match = int(msg.decode()[1:])
                #socket de la nueva conexión
                aleatorioSocket = skt.socket(skt.AF_INET,skt.SOCK_DGRAM)

                #Comienza el juego
                while juego:
                    mensaje_jugada = ''
                    #Mensaje del cliente
                    jugada_C = clientSocket.recv(2048).decode()
                    aleatorioSocket.sendto("JUGO".encode(),(serverAddr,Puerto_match))
                    mensaje_jugada = mensaje_jugada + "[*] Usted jugó " + jugada_C + "\n"

                    #Mensaje del servidor cachipun
                    jugada_B, addr = aleatorioSocket.recvfrom(2048)
                    jugada_B = jugada_B.decode()
                    mensaje_jugada = mensaje_jugada + "[*] El bot jugó " + jugada_B + "\n---\n"
                    print("[*] El bot jugó " + jugada_B)
                    #El juego sigue mientras ninguno gane 3 veces
                    if puntos_bot < 3 and puntos_cliente < 3:

                        if (jugada_C == "Piedra" and jugada_B == "Piedra") or (jugada_C == "Papel" and jugada_B == "Papel") or (jugada_C == "Tijera" and jugada_B == "Tijera"):
                            mensaje_jugada = mensaje_jugada + "[*] Empate en este turno\n"

                        elif (jugada_C == "Piedra" and jugada_B == "Papel" ) or (jugada_C == "Papel" and jugada_B == "Tijera") or (jugada_C == "Tijera" and jugada_B == "Piedra"):
                            mensaje_jugada = mensaje_jugada + "[*] El ganador de esta ronda fue el bot\n"
                            puntos_bot+=1

                        elif (jugada_C == "Piedra" and jugada_B == "Tijera") or (jugada_C == "Papel" and jugada_B == "Piedra") or (jugada_C == "Tijera" and jugada_B == "Papel"):
                            mensaje_jugada = mensaje_jugada + "[*] El ganador de esta ronda fue usted\n"
                            puntos_cliente +=1

                        mensaje_jugada = mensaje_jugada + "[*] El marcador actual es Jugador " + str(puntos_cliente) + ", Bot " + str(puntos_bot) + "\n---"

                    if puntos_bot == 3:
                        mensaje_jugada = mensaje_jugada + "\n---\n"  + "[*] El ganador de la partida fue: Bot\n" + "######################"
                        respuesta = "Servidor cachipún gana la partida"
                        juego = False
                        aleatorioSocket.sendto("TERMINO".encode(),(serverAddr,Puerto_match))
                        aleatorioSocket.close()
                    elif puntos_cliente == 3:
                        mensaje_jugada = mensaje_jugada + "\n---\n"  + "[*] El ganador de la partida fue: Jugador\n" + "######################"
                        juego = False
                        aleatorioSocket.sendto("TERMINO".encode(),(serverAddr,Puerto_match))
                        aleatorioSocket.close()

                    clientSocket.send(mensaje_jugada.encode())

        #Se escoge la opción salir del juego
        elif msg == "PARAR":
            print("Conexion con cliente terminada")
            respuesta = "conexión TCP terminada entre cliente e intermediario"
            clientSocket.send(respuesta.encode())
            cachipunSocket.sendto("STOP".encode(),(serverAddr, Puerto_Cachipun))
            cachipunSocket.close()
            dentro = False
    break

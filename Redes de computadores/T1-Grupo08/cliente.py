import socket as skt

serverPort = 50002 #Puerto servidor intermediario
serverAddr = 'localhost'
empezo = False
#Socket creado TCP
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
clientSocket.connect((serverAddr,serverPort)) #Handshake
print("\n---'   ____)____\n          ______)\n       __________)\n      (____)\n---.__(___)\n")
print("#    CACHIPÚN!   #\n")
while True:
    Disponibilidad = True
    Partida = True
    accion = int(input("[*] Seleccione acción:\n1. Jugar \n2. Salir:  "))
    print("######################")
    #Se solicita una partida
    if accion == 1:
        #Se envia al servidor intermedio una solicitud de partida
        clientSocket.send("EMPEZAR".encode())
        #Empieza loop de disponibilidad
        while Disponibilidad:
            #Respuesta de solicitud de partida
            msg = clientSocket.recv(2048).decode()
            #el servidor intermedio dice que no hay disponibilidad
            if msg == "ERROR":
                print("No hay disponibilidad de partidas")
                Disponibilidad = False

            #El servidor intermedio dice que hay disponibilidad de partida
            elif msg == "GO":
                while Partida:
                    valido = True
                    seleccion = int(input("[*] Seleccione jugada:\n1. Piedra \n2. Papel\n3. Tijera:  "))
                    print("---")
                    if seleccion == 1:
                        seleccion = "Piedra"
                    elif seleccion == 2:
                        seleccion = "Papel"
                    elif seleccion == 3:
                        seleccion = "Tijera"
                    else:
                        valido = False
                    if valido:
                        clientSocket.send(seleccion.encode())
                        msg = clientSocket.recv(2048).decode()
                        if "El ganador de la partida fue:" in msg:
                            print(msg)
                            Partida = False
                            Disponibilidad = False
                        else:
                            print(msg)


    else:
        print("El jugador escogió salir del juego")
        clientSocket.send("PARAR".encode())
        clientSocket.close()
        break

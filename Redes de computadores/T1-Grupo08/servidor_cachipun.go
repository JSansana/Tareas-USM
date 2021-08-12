package main

import (
        "fmt"
        "net"
        "math/rand"
        "time"
        "strconv"
)

func Partida(Puerto_Partida string){
    //Habilitar conexion
    randomtime := rand.New(rand.NewSource(time.Now().UnixNano()))
    s, err := net.ResolveUDPAddr("udp4", Puerto_Partida)
    if err != nil {
        fmt.Println(err)
        return
    }
    connection, err := net.ListenUDP("udp4", s)
    if err != nil{
        fmt.Println(err)
        return
    }
    defer connection.Close()
    buffer := make([]byte, 1024)

    for{
        n, addr, err := connection.ReadFromUDP(buffer)
        jugada := randomtime.Intn(3)
        if err != nil{
            fmt.Println(err)
            return
        }

        if string(buffer[0:n]) == "JUGO"{

            if jugada == 0 {
                connection.WriteToUDP([]byte("Piedra"), addr)
                fmt.Println("Se enviará piedra")
            } else if jugada == 1 {
                connection.WriteToUDP([]byte("Papel"), addr)
                fmt.Println("Se enviará papel")
            } else if jugada == 2 {
                connection.WriteToUDP([]byte("Tijera"), addr)
                fmt.Println("Se enviará tijera")
            }
        } else if string(buffer[0:n]) == "TERMINO"{
            return
        }
    }
}



func main() {
    fmt.Println("Bienvenido al servidor Cachipún!")
    PUERTO := ":50001"
    //Tamaño maximo de mensajes a recibir (?)
    BUFFER := 1024
    randomtime := rand.New(rand.NewSource(time.Now().UnixNano()))
    //Genera puerto UDP y revisa que no esté ocupado
    s, err := net.ResolveUDPAddr("udp4", PUERTO)
    if err != nil {
        fmt.Println(err)
        return
    }

    //Deja funcionando el programa escuchando los mensajes que llegan por UDP
    connection, err := net.ListenUDP("udp4", s)
    if err != nil{
        fmt.Println(err)
        return
    }
    defer connection.Close()

    //Aqui se reciben los mensajes con el tamaño BUFFER
    buffer := make([]byte, BUFFER)

    //while true
    for{
        //En cada vuelta se lee el buffer
        n, addr, err := connection.ReadFromUDP(buffer)
        if err != nil{
            fmt.Println(err)
            return
        }
        //Printea lo que hay en el buffer
        fmt.Print("-> ", string(buffer[0:n]), "\n")

        //Condición de término para el loop (En este caso, que en el buffer haya un STOP)
        if string(buffer[0:n]) == "STOP"{
            fmt.Println("Cerrando el servidor Cachipun!")
            return

        } else if string(buffer[0:n]) == "START" { //EL jugador solicitó inicio de partida
            Puerto_Partida := ":" + strconv.Itoa(randomtime.Intn(50015 - 50003) + 50003)


            if Puerto_Partida == ":50014"{
                fmt.Println("No hay partida disponible")
                connection.WriteToUDP([]byte("ERROR"), addr)

            } else {
                //mensaje :=[]byte(Puerto_Partida)
                fmt.Println("Hay partida disponible en el puerto" + Puerto_Partida)
                connection.WriteToUDP([]byte(Puerto_Partida), addr)
                Partida(Puerto_Partida)
            }
        }

    }//FOR

}//MAIN

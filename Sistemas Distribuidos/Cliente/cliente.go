//NEW CLIENT
package main

import (
	"context"
	"log"
	pb "modulo/gRPC/proto"
	"time"

	"google.golang.org/grpc"
)

const (
	address = "localhost:50051"
)

func main() {

	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("No conectó: %v", err)
	}
	defer conn.Close()

	//nuevo cliente
	c := pb.NewComunicacionJLClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	var num int32 = 1
	//r guarda la respuesta del servidor
	r, err := c.GetRespuesta(ctx, &pb.SolicitudParticipacion{Participacion: num})
	if err != nil {
		log.Fatalf("No se pudo enviar solicitud: %v", err)
	}

	log.Printf("RESPUESTA DEL SERVER : %v", r.GetRespuesta())

	if r.GetRespuesta() == 1 {
		log.Printf("Entrando al juego")
		//codigo cuando se puede entrar al juego

	} else if r.GetRespuesta() == 0 {
		log.Printf("No se puede entrar al juego")
		// codigo cuando no se puede entrar al juego

	}

}

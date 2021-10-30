package main

import (
	"context"
	"log"
	"math/rand"
	pb "modulo/gRPC/proto"
	"net"
	"time"

	"google.golang.org/grpc"
)

//Puerto definido
const (
	port = ":50051"
)

//Implementación del método propuesto por proto, ya que está sin implementar
type ComunicacionJLServer struct {
	pb.UnimplementedComunicacionJLServer
}

//Implementación del método definido en proto
func (s *ComunicacionJLServer) GetRespuesta(ctx context.Context, in *pb.SolicitudParticipacion) (*pb.RespuestaLider, error) {
	log.Printf("Recibida solicitud de juego %v", in.GetParticipacion())
	rand.Seed(time.Now().UnixNano())
	min := 0
	max := 1

	//Lider contesta a jugador un 0 o un 1
	//Si contesta 0, el jugador no puede unirse al juego
	//Si contesta 1, el jugador puede unirse al juego
	var numero int32 = int32(rand.Intn(max-min+1) + min)
	return &pb.RespuestaLider{Respuesta: numero}, nil
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Fallo al escuchar: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterComunicacionJLServer(s, &ComunicacionJLServer{})
	log.Printf("Servidor escuchando en %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Fallo en serve: %v", err)
	}

}

package main

import (
	"flag"
	"fmt"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/cmd/gateway"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/cmd/grpc"
	"strings"
)

var (
	// Mode - Establece el modo de ejecución
	Mode = flag.String("mode", "grpc", "Select execution mode [grpc (default), gateway, client]")
)

func main() {
	flag.Parse()
	switch strings.ToUpper(*Mode) {
	case "CLIENT":
		fmt.Println(*Mode)
	case "GATEWAY":
		gateway.Run()
	default:
		grpc.Run()
	}
}

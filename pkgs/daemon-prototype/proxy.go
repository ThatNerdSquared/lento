package main

import (
	"fmt"
	"net"

	"github.com/nwtgck/go-socks"
)

func handleConn(conn net.Conn) {
}

func main() {
	socksConf := &socks.Config{}
	socksServer, err := socks.New(socksConf)
	if err != nil {
		panic(err)
	}

	l, err := net.Listen("tcp", "127.0.0.1:")
	fmt.Println(
		"Proxying on port",
		l.Addr().(*net.TCPAddr).Port,
	)
	if err != nil {
		panic(err)
	}
	for {
		conn, err := l.Accept()
		if err != nil {
			panic(err)
		}
		fmt.Println("accepted")
		// go handleConn(conn)
		go socksServer.ServeConn(conn)
	}
}

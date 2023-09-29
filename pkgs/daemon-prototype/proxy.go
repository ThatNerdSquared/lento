package main

import (
	"fmt"
	"net"

	"github.com/nwtgck/go-socks"
)

type LentoProxy struct {
	socksServer socks.Server
	listener    net.Listener
}

func (proxy LentoProxy) handleConn(conn net.Conn) {
	print(conn)
	go proxy.socksServer.ServeConn(conn)
}

func (proxy *LentoProxy) initSOCKS() {
	socksConf := &socks.Config{}
	socksServer, err := socks.New(socksConf)
	if err != nil {
		panic(err)
	}
	proxy.socksServer = *socksServer
	l, err := net.Listen("tcp", "127.0.0.1:")
	if err != nil {
		panic(err)
	}
	fmt.Println(
		"Proxying on port",
		l.Addr().(*net.TCPAddr).Port,
	)
	proxy.listener = l
}

func main() {
	lproxy := LentoProxy{}
	lproxy.initSOCKS()
	for {
		conn, err := lproxy.listener.Accept()
		if err != nil {
			panic(err)
		}
		fmt.Println("accepted")
		lproxy.handleConn(conn)
	}
}

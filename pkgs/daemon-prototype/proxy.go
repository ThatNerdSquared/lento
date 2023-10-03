package main

import (
	"context"
	"fmt"
	"net"
	"net/url"
	"time"

	"github.com/google/uuid"
	"github.com/nwtgck/go-socks"
)

/// websites : {url: {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMessage: <String>}},

type BlockedWebsite struct {
	url          url.URL
	popupMessage string
	isSoftBlock  bool
	lastOpened   time.Time
	isAllowed    bool
}

type LentoProxy struct {
	blockedSites map[uuid.UUID]BlockedWebsite
	socksServer  socks.Server
	listener     net.Listener
}

// func (proxy LentoProxy) handleConn(conn net.Conn) {
func (proxy LentoProxy) handleConn(ctx context.Context, network string, addr string) (net.Conn, error) {
	names, err := net.LookupAddr(addr)
	fmt.Printf("%s", names) // Output: Go
	print(err)
	// // socksConn, err := socks.NewRequest(bufio.NewReader(conn))
	// socksConn = socks.
	// err := nil
	// print(conn)
	// if err != nil {
	// 	print("AHHHHHHHHHH")
	// 	panic(err)
	// }

	// for _, val := range proxy.blockedSites {
	// 	if val.url.String() == socksConn.DestAddr.FQDN && !val.isSoftBlock {
	// 		err = conn.Close()
	// 		if err != nil {
	// 			panic(err)
	// 		} else {
	// 			return
	// 		}
	// 	}
	// }
	// print(conn)
	// go proxy.socksServer.ServeConn(conn)
	return net.Dial(network, addr)
}

func (proxy *LentoProxy) initSOCKS() {
	socksConf := &socks.Config{Dial: proxy.handleConn}
	// socksConf := &socks.Config{}
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
	exm, _ := url.Parse("https://example.com")
	lproxy := LentoProxy{
		blockedSites: map[uuid.UUID]BlockedWebsite{
			uuid.New(): {
				url:          *exm,
				popupMessage: "test",
				isSoftBlock:  false,
				lastOpened:   time.Now(),
				isAllowed:    false,
			},
		},
	}
	lproxy.initSOCKS()
	for {
		conn, err := lproxy.listener.Accept()
		if err != nil {
			panic(err)
		}
		fmt.Println("accepted")
		// print(pirate(conn))
		// lproxy.handleConn(conn)
		go lproxy.socksServer.ServeConn(conn)
	}
}

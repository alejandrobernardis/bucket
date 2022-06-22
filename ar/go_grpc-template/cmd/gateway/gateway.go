package gateway

import (
	"context"
	"errors"
	"github.com/grpc-ecosystem/grpc-gateway/runtime"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/config"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/logger"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/sentry"
	pbC "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/common"
	pbH "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/health"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/insecure"
	"log"
	"net"
	"net/http"
	"os"
	"os/signal"
	"strings"
)

func allowCORS(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if origin := r.Header.Get("Origin"); origin != "" {
			w.Header().Set("Access-Control-Allow-Origin", origin)
			if r.Method == "OPTIONS" && r.Header.Get("Access-Control-Request-Method") != "" {
				headers := []string{"Content-Type", "Accept", "Authorization"}
				w.Header().Set("Access-Control-Allow-Headers", strings.Join(headers, ","))
				methods := []string{"GET", "HEAD", "POST", "PUT", "DELETE"}
				w.Header().Set("Access-Control-Allow-Methods", strings.Join(methods, ","))
				return
			}
		}
		h.ServeHTTP(w, r)
	})
}

func Run() {

	// === Configuration =======================================================

	if err := config.Init(); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.CONFIG, err)
	}

	// === Logger ==============================================================

	if err := logger.Init(*config.LogLevel); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.LOGGER, err)
	}

	logger.Log.Debug("DEBUG", zap.Bool("enable", config.Debug))
	logger.Done(config.LOGGER)

	// === Sentry ==============================================================

	if err := sentry.Init(*config.SentryCnxStr, config.Debug); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.SENTRY, err)
	}

	logger.DebugCnxstr(config.SENTRY, *config.SentryCnxStr)
	logger.Done(config.SENTRY)

	// === GATEWAY server ======================================================

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	//... establecemos el endpoint de servidor de GRPC

	addrGrpc := net.JoinHostPort(*config.GrpcHost, *config.GrpcPort)
	logger.Done(config.GATEWAY, zap.String("grcp endpoint", addrGrpc))

	//... definimos y configuramos el servidor del GATEWAY.

	gw := runtime.NewServeMux()
	opt := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	if *config.Tls {

		if len(*config.TlsCa) == 0 {
			logger.Log.Fatal(config.TLS, zap.Error(errors.New("CA file not defined")))
		}

		crd, err := credentials.NewClientTLSFromFile(*config.TlsCa, "")

		if err != nil {
			logger.Log.Fatal(config.TLS, zap.Error(err))
		}

		opt = []grpc.DialOption{grpc.WithTransportCredentials(crd)}

		logger.Log.Debug(config.TLS, zap.String("ca", *config.TlsCa))

	}

	logger.Done(config.TLS, zap.Bool("enable", *config.Tls))

	for _, f := range []func(context.Context, *runtime.ServeMux, string, []grpc.DialOption) error{
		pbC.RegisterCommonServiceHandlerFromEndpoint,
		pbH.RegisterHealthServiceHandlerFromEndpoint,
		//... add more here
	} {
		if err := f(ctx, gw, addrGrpc, opt); err != nil {
			logger.Log.Fatal(config.GATEWAY, zap.Error(err))
		}
	}

	addr := net.JoinHostPort(*config.GatewayHost, *config.GatewayPort)
	logger.Done(config.GATEWAY, zap.String("gateway endpoint", addr))
	srv := &http.Server{Addr: addr, Handler: allowCORS(gw)}

	//... controlamos el apagado del mismo

	gfs := make(chan os.Signal, 1)
	signal.Notify(gfs, os.Interrupt)

	go func() {
		for range gfs {
			if err := srv.Shutdown(context.Background()); err != nil {
				logger.Log.Fatal(config.GATEWAY, zap.Error(err))
			}
			<-ctx.Done()
		}
	}()

	//... run

	if *config.Tls {
		if err := srv.ListenAndServeTLS(*config.TlsCert, *config.TlsKey); err != http.ErrServerClosed {
			logger.Log.Fatal(config.GATEWAY, zap.Error(err))
		}
	} else {
		if err := srv.ListenAndServe(); err != http.ErrServerClosed {
			logger.Log.Fatal(config.GATEWAY, zap.Error(err))
		}
	}
}

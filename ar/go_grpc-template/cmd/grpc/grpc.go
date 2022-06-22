package grpc

import (
	"context"
	"errors"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/cache"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/config"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/etcd"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/logger"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/maria"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/mongo"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/redis"
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/sentry"
	apiC "github.com/alejandrobernardis/bucket/ar/go_grpc-template/pkg/api/v1/common"
	apiH "github.com/alejandrobernardis/bucket/ar/go_grpc-template/pkg/api/v1/health"
	pbC "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/common"
	pbH "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/health"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/alts"
	"google.golang.org/grpc/reflection"
	"log"
	"net"
	"os"
	"os/signal"
)

func Run() {

	// === Configuration =======================================================

	if err := config.Init(); err != nil {
		log.Printf("failed to initialize config: %v", err)
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

	// === Maria ===============================================================

	if db, err := maria.Init(*config.MariaCnxStr); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.MARIA, err)
	} else if db != nil {
		defer maria.Close()
	}

	logger.DebugCnxstr(config.MARIA, *config.MariaCnxStr)
	logger.Done(config.MARIA)

	// === Mongo ===============================================================

	if db, err := mongo.Init(*config.MongoCnxStr); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.MONGO, err)
	} else if db != nil {
		defer mongo.Close()
	}

	logger.DebugCnxstr(config.MONGO, *config.MongoCnxStr)
	logger.Done(config.MONGO)

	// === Redis ===============================================================

	if db, err := redis.Init(*config.RedisCnxStr); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.REDIS, err)
	} else if db != nil {
		defer redis.Close()
	}

	logger.DebugCnxstr(config.REDIS, *config.RedisCnxStr)
	logger.Done(config.REDIS)

	// === Etcd ================================================================

	if db, err := etcd.Init(*config.EtcdCnxStr); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.ETCD, err)
	} else if db != nil {
		defer etcd.Close()
	}

	logger.DebugCnxstr(config.ETCD, *config.EtcdCnxStr)
	logger.Done(config.ETCD)

	// === Ristretto ===========================================================

	if db, err := cache.Init(); err != nil {
		log.Fatalf("failed to initialize %v: %v", config.RISTRETTO, err)
	} else if db != nil {
		defer cache.Close()
	}

	logger.DebugCnxstr(config.RISTRETTO, "...")
	logger.Done(config.RISTRETTO)

	// === GRPC server =========================================================

	// Definimos el puerto a escuchar (default: 50051)

	lis, err := net.Listen("tcp", net.JoinHostPort(*config.GrpcHost, *config.GrpcPort))

	if err != nil {
		logger.Log.Fatal(config.RPC, zap.Error(err))
	}

	logger.Done(config.RPC, zap.String("port", *config.GrpcPort))

	// Comenzamos con la configuración del servidor

	var opt []grpc.ServerOption

	// ... agregamos el logger

	opt = logger.AddLogger(logger.Log, opt)

	// ... configuramos la capa de transporte segura en caso de estar habilitada

	if *config.Alts {

		crd := alts.NewServerCreds(alts.DefaultServerOptions())
		opt = append(opt, grpc.Creds(crd))

	} else if *config.Tls {

		if len(*config.TlsCert) == 0 || len(*config.TlsKey) == 0 {
			logger.Log.Fatal(config.TLS, zap.Error(errors.New("Cert/Key file not defined")))
		}

		crd, err := credentials.NewServerTLSFromFile(*config.TlsCert, *config.TlsKey)

		if err != nil {
			logger.Log.Fatal(config.TLS, zap.Error(err))
		}

		opt = append(opt, grpc.Creds(crd))

		logger.Log.Debug(
			config.TLS,
			zap.String("cert", *config.TlsCert),
			zap.String("key", *config.TlsKey),
		)

	}

	logger.Done(config.ATLS, zap.Bool("enable", *config.Alts))
	logger.Done(config.TLS, zap.Bool("enable", *config.Tls))

	// ... creamos a la instancia del servidor, registramos los protocolos
	// soportados y el modo de reflexión

	srv := grpc.NewServer(opt...)
	pbC.RegisterCommonServiceServer(srv, apiC.New())
	pbH.RegisterHealthServiceServer(srv, apiH.New())
	reflection.Register(srv)

	// ... creamos el contexto de ejecución y el canal para escuchar la solicitud
	// de interrupción del servicio

	ctx := context.Background()
	gfs := make(chan os.Signal, 1)
	signal.Notify(gfs, os.Interrupt)

	go func() {
		for range gfs {
			srv.GracefulStop()
			<-ctx.Done()
		}
	}()

	// ... finalmente iniciamos el servicio

	if err := srv.Serve(lis); err != nil {
		logger.Log.Fatal(config.RPC, zap.Error(err))
	}

}

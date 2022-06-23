package config

import (
	"flag"
	"github.com/jamiealquiza/envy"
	"github.com/joho/godotenv"
	"sync"
	"time"
)

const (
	CONFIG    = "CONFIG"
	LOGGER    = "LOGGER"
	SENTRY    = "SENTRY"
	MONGO     = "MONGO"
	MARIA     = "MARIA"
	REDIS     = "REDIS"
	ETCD      = "ETCD"
	RISTRETTO = "RISTRETTO"
	TLS       = "TLS"
	ATLS      = "ATLS"
	RPC       = "RPC"
	GATEWAY   = "GATEWAY"
	CNXSTR    = "cnxstr"
)

var (

	// Alts - Habilita el modo de conexión segura
	Alts = flag.Bool("alts", false, "Enable ALTS connection")

	// Tls - Habilita el modo de conexión segura
	Tls = flag.Bool("tls", false, "Enable TLS connection")

	// TlsCert - Ruta del certificado para la conexión por TLS
	TlsCert = flag.String("tls-cert", "/certs/server.crt", "TLS cert file")

	// TlsKey - Ruta de la clave para la conexión por TLS
	TlsKey = flag.String("tls-key", "/certs/server.pem", "TLS key file")

	// TlsCa - Ruta de la entidad para la conexión por TLS
	TlsCa = flag.String("tls-ca", "/certs/server-ca.crt", "TLS ca file")

	// GrpcHost - GrpcHost y puerto de conexión para el servicio
	GrpcHost = flag.String("grpc-host", "", "Host to serve GRPC")

	// GrpcPort - GrpcHost y puerto de conexión para el servicio
	GrpcPort = flag.String("grpc-port", "50051", "Port to serve GRPC")

	// GatewayHost - GrpcHost y puerto de conexión para el servicio
	GatewayHost = flag.String("gateway-host", "", "Host to serve GATEWAY")

	// GatewayPort - GrpcHost y puerto de conexión para el gateway de servicio
	GatewayPort = flag.String("gateway-port", "8080", "Port to serve GATEWAY")

	// MongoCnxStr - String de conexión para MongoDB
	MongoCnxStr = flag.String("mongo-cnxstr", "", "Mongo connection string")

	// MariaCnxStr - String de conexión para MariaDB
	MariaCnxStr = flag.String("maria-cnxstr", "", "Maria connection string")

	// RedisCnxStr - String de conexión para Redis
	RedisCnxStr = flag.String("redis-cnxstr", "", "Redis connection string")

	// EtcdCnxStr - String de conexión para Etcd
	EtcdCnxStr = flag.String("etcd-cnxstr", "", "Etcd connection string")

	// SentryCnxStr - String de conexión para redis
	SentryCnxStr = flag.String("sentry-cnxstr", "", "Sentry connection string")

	// LogLevel - Definición del nivel de logging
	LogLevel = flag.Int("log-level", 2, "Logging level")

	// EnvFilename - Definición del nombre de archivo de environment
	EnvFilename = flag.String("env-filename", "/etc/server.conf", "Environment file name")

	// ExpireAt - Definición del tiempo de expiración (default: 5m)
	ExpireAt = flag.Duration("expire-at", 5*time.Minute, "Cache expire time")

	// Debug - Modo debug ON/OFF
	Debug bool

	// once - Just once
	once sync.Once
)

func Init() error {
	var err error
	once.Do(func() {
		flag.Parse()
		err = godotenv.Overload(*EnvFilename)
		envy.Parse("CFG")
		Debug = *LogLevel < 0
	})
	return err
}

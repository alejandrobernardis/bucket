package logger

import (
	grpcmiddleware "github.com/grpc-ecosystem/go-grpc-middleware"
	grpczap "github.com/grpc-ecosystem/go-grpc-middleware/logging/zap"
	grpcctxtags "github.com/grpc-ecosystem/go-grpc-middleware/tags"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
)

func codeToLevel(code codes.Code) zapcore.Level {

	if code == codes.OK {
		return zapcore.DebugLevel
	}

	return grpczap.DefaultCodeToLevel(code)

}

func AddLogger(logger *zap.Logger, opt []grpc.ServerOption) []grpc.ServerOption {

	opts := []grpczap.Option{
		grpczap.WithLevels(codeToLevel),
	}

	grpczap.ReplaceGrpcLoggerV2(logger)

	opt = append(opt, grpcmiddleware.WithUnaryServerChain(
		grpcctxtags.UnaryServerInterceptor(
			grpcctxtags.WithFieldExtractor(
				grpcctxtags.CodeGenRequestFieldExtractor,
			),
		),
		grpczap.UnaryServerInterceptor(logger, opts...),
	))

	opt = append(opt, grpcmiddleware.WithStreamServerChain(
		grpcctxtags.StreamServerInterceptor(
			grpcctxtags.WithFieldExtractor(
				grpcctxtags.CodeGenRequestFieldExtractor,
			),
		),
		grpczap.StreamServerInterceptor(logger, opts...),
	))

	return opt

}

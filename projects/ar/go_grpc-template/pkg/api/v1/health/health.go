package health

import (
	"context"
	pbC "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/common"
	pb "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/health"
	"google.golang.org/protobuf/types/known/emptypb"
)

type apiHealth struct {
	pb.UnimplementedHealthServiceServer
}

func New() *apiHealth {
	return &apiHealth{}
}

func (x *apiHealth) Ping(_ context.Context, _ *emptypb.Empty) (*pbC.Response, error) {
	return &pbC.Response{Message: "Pong"}, nil
}

func (x *apiHealth) Health(_ context.Context, _ *emptypb.Empty) (*pbC.Response, error) {
	return &pbC.Response{Message: "Health"}, nil
}

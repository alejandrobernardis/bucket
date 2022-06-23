package common

import (
	"context"
	pb "github.com/alejandrobernardis/bucket/ar/go_grpc-template/proto/api/v1/common"
	"google.golang.org/protobuf/types/known/emptypb"
)

type apiCommon struct {
	pb.UnimplementedCommonServiceServer
}

func New() *apiCommon {
	return &apiCommon{}
}

func (x *apiCommon) Version(_ context.Context, _ *emptypb.Empty) (*pb.Response, error) {
	return &pb.Response{Message: "1.0.0"}, nil
}

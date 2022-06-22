package mongo

import (
	"context"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"sync"
)

var (
	Db   *mongo.Client
	once sync.Once
)

func Init(cnx string) (*mongo.Client, error) {
	var err error
	if cnx != "" {
		once.Do(func() {
			opt := options.Client().ApplyURI(cnx)
			Db, err = mongo.Connect(context.TODO(), opt)
		})
	}
	return Db, err
}

func Close() {
	if Db != nil {
		Db.Disconnect(context.Background())
	}
}

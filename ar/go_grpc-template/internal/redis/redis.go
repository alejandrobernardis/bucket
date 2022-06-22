package redis

import (
	"github.com/go-redis/redis/v8"
	"sync"
)

var (
	Db   *redis.Client
	once sync.Once
)

func Init(cnx string) (*redis.Client, error) {
	var err error
	if cnx != "" {
		once.Do(func() {
			var opt *redis.Options
			if opt, err = redis.ParseURL(cnx); err == nil {
				Db = redis.NewClient(opt)
			}
		})
	}
	return Db, err
}

func Close() {
	if Db != nil {
		_ = Db.Close()
	}
}

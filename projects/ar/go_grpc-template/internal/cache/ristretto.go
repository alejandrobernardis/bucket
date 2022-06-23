package cache

import (
	"github.com/dgraph-io/ristretto"
	"sync"
)

var (
	Db   *ristretto.Cache
	once sync.Once
)

func Init() (*ristretto.Cache, error) {
	var err error
	once.Do(func() {
		Db, err = ristretto.NewCache(
			&ristretto.Config{
				NumCounters: 1e7,
				MaxCost:     1 << 30,
				BufferItems: 64,
				Metrics:     false,
			},
		)
	})
	return Db, err
}

func Close() {
	if Db != nil {
		Db.Close()
	}
}

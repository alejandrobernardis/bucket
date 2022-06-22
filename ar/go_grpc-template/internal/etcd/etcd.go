package etcd

import (
	etcdc "go.etcd.io/etcd/client/v3"
	"strings"
	"sync"
)

var (
	Db   *etcdc.Client
	once sync.Once
)

func Init(cnx string) (*etcdc.Client, error) {
	var err error
	if cnx != "" {
		// TODO(berna): revisar el tema del acceso mediante usuario y contraseña
		ep := strings.Split(cnx, ";")
		once.Do(func() {
			Db, err = etcdc.New(etcdc.Config{
				Endpoints: ep,
			})
		})
	}
	return Db, err
}

func Close() {
	if Db != nil {
		_ = Db.Close()
	}
}

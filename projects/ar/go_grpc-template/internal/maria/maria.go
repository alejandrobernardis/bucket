package maria

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"sync"
)

var (
	Db   *sql.DB
	once sync.Once
)

func Init(cnx string) (*sql.DB, error) {
	var err error
	if cnx != "" {
		once.Do(func() {
			Db, err = sql.Open("mysql", cnx)
		})
	}
	return Db, err
}

func Close() {
	if Db != nil {
		_ = Db.Close()
	}
}

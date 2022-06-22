package sentry

import (
	sentryc "github.com/getsentry/sentry-go"
	"sync"
	"time"
)

var once sync.Once

func Init(cnx string, debug bool) error {
	var err error
	if cnx != "" {
		once.Do(func() {
			if !debug {
				if err = sentryc.Init(sentryc.ClientOptions{Dsn: cnx}); err == nil {
					defer func() {
						sentryc.Flush(2 * time.Second)
					}()
				}
			}
		})
	}
	return err
}

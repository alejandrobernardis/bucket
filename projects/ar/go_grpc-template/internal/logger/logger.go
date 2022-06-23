package logger

import (
	"github.com/alejandrobernardis/bucket/ar/go_grpc-template/internal/config"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"os"
	"sync"
)

var (
	Log  *zap.Logger
	once sync.Once
)

func DebugCnxstr(cmp string, cnxstr string) {
	Log.Debug(cmp, zap.String(config.CNXSTR, cnxstr))
}

func Done(cmp string, opt ...zap.Field) {
	Log.Info(cmp, append([]zap.Field{zap.String("status", "done")}, opt...)...)
}

func Init(level int) error {
	var err error
	once.Do(func() {
		gl := zapcore.Level(level)
		hp := zap.LevelEnablerFunc(func(l zapcore.Level) bool {
			return l >= zapcore.ErrorLevel
		})
		hpe := zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig())
		lp := zap.LevelEnablerFunc(func(l zapcore.Level) bool {
			return l >= gl && l < zapcore.ErrorLevel
		})
		lpe := zapcore.NewJSONEncoder(zap.NewDevelopmentEncoderConfig())
		Log = zap.New(zapcore.NewTee(
			zapcore.NewCore(hpe, zapcore.Lock(os.Stderr), hp),
			zapcore.NewCore(lpe, zapcore.Lock(os.Stdout), lp),
		))
		zap.RedirectStdLog(Log)
	})
	return err
}

package log

import (
	"context"
	"sync"

	"go.uber.org/zap"
)

var (
	suger *zap.SugaredLogger
	mx    sync.Mutex
)

func WithContext(ctx context.Context) *zap.SugaredLogger {
	if suger != nil {
		return suger
	}

	defer mx.Unlock()
	mx.Lock()

	// config := zap.NewDevelopmentConfig()
	// config.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
	// config.EncoderConfig.TimeKey = "timestamp"
	// config.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	// logger, _ := config.Build()
	// zap.ReplaceGlobals(logger)
	logger, _ := zap.NewProduction()
	suger = logger.Sugar()
	return suger
}

func Close() {
	suger.Sync()
}

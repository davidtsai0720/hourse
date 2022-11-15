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

	logger, _ := zap.NewProduction()
	suger = logger.Sugar()
	return suger
}

func Close() {
	suger.Sync()
}

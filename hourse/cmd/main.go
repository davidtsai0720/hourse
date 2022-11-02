package main

import (
	"context"
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/hourse"
	hourseHTTP "github.com/hourse/http"
	"github.com/hourse/log"
	"github.com/hourse/postgres"
	_ "github.com/lib/pq"
	"github.com/spf13/viper"
)

func NewDatabaseConn() (*sql.DB, error) {
	user := viper.GetString("service.postgres.user")
	password := viper.GetString("service.postgres.password")
	db := viper.GetString("service.postgres.db")
	return sql.Open("postgres", fmt.Sprintf("user=%s password=%s dbname=%s sslmode=disable", user, password, db))
}

func main() {
	loger := log.WithContext(context.Background())
	defer log.Close()

	viper.SetConfigType("yaml")
	viper.SetConfigFile("./config/setting.yaml")

	if err := viper.ReadInConfig(); err != nil {
		loger.Fatalln("cannot read config: %v", err)
	}

	conn, err := NewDatabaseConn()
	if err != nil {
		loger.Fatalln(err)
	}

	db := postgres.New(conn)
	service := hourse.NewService(db)
	server := hourseHTTP.NewServer(service)
	handler := server.Handler()
	srv := &http.Server{Addr: fmt.Sprintf(":%d", viper.GetInt("service.port")), Handler: handler}

	loger.Info("Start server...")
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			loger.Fatalf("listen: %s\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	loger.Info("Shutdown Server ...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		loger.Fatal("Server Shutdown: ", err)
	}

	loger.Info("Server exiting")
}

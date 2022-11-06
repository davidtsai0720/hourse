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
)

func NewDatabaseConn(ctx context.Context) (*sql.DB, error) {
	user := os.Getenv("POSTGRES_USER")
	password := os.Getenv("POSTGRES_PASSWORD")
	db := os.Getenv("POSTGRES_DB")
	port := os.Getenv("POSTGRES_PORT")
	host := os.Getenv("POSTGRES_HOST")

	loger := log.WithContext(ctx)
	if user == "" || password == "" || db == "" || port == "" || host == "" {
		loger.Fatalln("wrong db connecttion params")
	}

	return sql.Open("postgres", fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, db))
}

func main() {
	ctx := context.Background()
	loger := log.WithContext(ctx)
	defer log.Close()

	conn, err := NewDatabaseConn(ctx)
	if err != nil {
		loger.Fatalln(err)
	}

	db := postgres.New(conn)
	service := hourse.NewService(db)
	server := hourseHTTP.NewServer(service)
	handler := server.Handler()
	srv := &http.Server{Addr: fmt.Sprintf(":%s", os.Getenv("SERVICE_PORT")), Handler: handler}

	go func() {
		loger.Info("Start Listen...")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			loger.Fatalf("listen: %s\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	loger.Info("Shutdown Server ...")

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		loger.Fatal("Server Shutdown: ", err)
	}

	loger.Info("Server exiting")
}

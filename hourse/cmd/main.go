package main

import (
	"context"
	"database/sql"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/hourse"
	"github.com/hourse/postgres"
	"github.com/hourse/route"
	_ "github.com/lib/pq"
)

func main() {
	conn, err := sql.Open("postgres", "user=postgres password=postgres dbname=db sslmode=disable")
	if err != nil {
		log.Fatalln(err)
	}

	db := postgres.New(conn)
	service := hourse.NewService(db)
	router := route.NewService(service)
	handler := router.Handler()
	srv := &http.Server{Addr: ":8080", Handler: handler}

	log.Println("Start server")
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutdown Server ...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server Shutdown: ", err)
	}

	log.Println("Server exiting")
}

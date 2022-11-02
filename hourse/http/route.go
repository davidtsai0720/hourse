package http

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/hourse"
)

func NewServer(service hourse.HourseService) *Server {
	return &Server{router: chi.NewRouter(), service: service}
}

type Server struct {
	router  *chi.Mux
	service hourse.HourseService
}

func (server *Server) Handler() http.Handler {
	server.router.Get("/city", server.HandleGetCities())
	server.router.Get("/section/{name}", server.HandleGetSectionsByCity())
	server.router.Get("/sections", server.HandleGetSectionsWithCity())
	server.router.Get("/hourse", server.HandleGetHourses())
	server.router.Post("/hourse", server.HandleCreateHourse())
	return server.router
}

package http

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/hourse"
)

func NewServer(service hourse.HourseService) *Server {
	router := chi.NewRouter()
	router.Use(func(h http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Add("Access-Control-Request-Method", "POST,GET,PUT")
			w.Header().Add("Access-Control-Allow-Origin", r.Header.Get("Origin"))
			w.Header().Add("Access-Control-Allow-Headers", "*")
			if r.Method == http.MethodOptions {
				w.WriteHeader(http.StatusOK)
				return
			}
			h.ServeHTTP(w, r)
		})
	})
	return &Server{router: router, service: service}
}

type Server struct {
	router  *chi.Mux
	service hourse.HourseService
}

func (server *Server) Handler() http.Handler {
	server.router.Route("/api", func(r chi.Router) {
		r.Get("/city", server.HandleGetCities())
		r.Get("/section/{name}", server.HandleGetSectionsByCity())
		r.Get("/sections", server.HandleGetSectionsWithCity())
		r.Get("/hourse", server.HandleGetHourses())
		r.Put("/hourse", server.HandleUpsertHourse())
	})
	return server.router
}

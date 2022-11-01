package route

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/hourse"
)

func NewService(service hourse.HourseService) *Service {
	return &Service{service: service}
}

type Service struct {
	service hourse.HourseService
}

func (service *Service) Handler() http.Handler {
	r := chi.NewRouter()
	r.Get("/city", service.HandleGetCity())
	r.Get("/section/{name}", service.HandleGetSection())
	r.Post("/hourse", service.HandlePostHourse())
	return r
}

package route

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/go-chi/chi/v5"
	"github.com/hourse"
)

func response(w http.ResponseWriter, in interface{}) {
	resp, _ := json.Marshal(in)
	w.Write(resp)
}

func responseError(w http.ResponseWriter, in error) {
	resp, _ := json.Marshal(struct {
		Message string `json:"message"`
	}{Message: in.Error()})
	http.Error(w, string(resp), http.StatusBadRequest)
}

func (service *Service) HandleGetCity() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		resp, err := service.service.GetCity(r.Context())
		if err != nil {
			responseError(w, err)
			return
		}

		response(w, resp)
	}
}

func (service *Service) HandleGetSection() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		name := strings.Trim(chi.URLParam(r, "name"), " ")
		if name == "" {
			responseError(w, fmt.Errorf("name cannot be empty"))
			return
		}

		resp, err := service.service.GetSection(r.Context(), name)
		if err != nil {
			responseError(w, err)
			return
		}

		response(w, resp)
	}
}

func (service *Service) HandlePostHourse() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		body := &hourse.GetHourseRequest{}
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			responseError(w, err)
			return
		}

		if body.Page <= 1 {
			body.Page = 1
		}

		if body.PageSize <= 0 {
			body.PageSize = 30
		}

		resp, err := service.service.GetHourse(r.Context(), body)
		if err != nil {
			responseError(w, err)
			return
		}

		response(w, resp)
	}
}

package http

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/go-chi/chi/v5"
	"github.com/hourse"
)

const (
	ContentType     = "content-type"
	ApplicationJson = "application/json; charset=utf-8"
)

func response(w http.ResponseWriter, in interface{}, status int) {
	w.Header().Set(ContentType, ApplicationJson)
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(in)
}

func responseError(w http.ResponseWriter, err error, status int) {
	w.Header().Set(ContentType, ApplicationJson)
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(struct {
		Message string `json:"message"`
	}{Message: err.Error()})
}

func (server *Server) HandleGetCities() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		resp, err := server.service.GetCities(r.Context())
		if err != nil {
			responseError(w, err, http.StatusInternalServerError)
			return
		}

		response(w, resp, http.StatusOK)
	}
}

func (server *Server) HandleGetSectionsByCity() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		name := strings.Trim(chi.URLParam(r, "name"), " ")
		if name == "" {
			responseError(w, fmt.Errorf("name cannot be empty"), http.StatusBadRequest)
			return
		}

		resp, err := server.service.GetSectionsByCity(r.Context(), name)
		if err != nil {
			responseError(w, err, http.StatusInternalServerError)
			return
		}

		response(w, resp, http.StatusOK)
	}
}

func (server *Server) HandleGetHourses() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		body, err := parseGetHoursesRequest(r)
		if err != nil {
			responseError(w, err, http.StatusBadRequest)
			return
		}

		totalCount, resp, err := server.service.GetHourses(r.Context(), body)
		if err != nil {
			responseError(w, err, http.StatusInternalServerError)
			return
		}

		w.Header().Add("total-count", strconv.Itoa(int(totalCount)))
		w.Header().Add("page-size", strconv.Itoa(body.PageSize))
		response(w, resp, http.StatusOK)
	}
}

func (server *Server) HandleGetSectionsWithCity() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		resp, err := server.service.GetSectionsWithCity(r.Context())
		if err != nil {
			responseError(w, err, http.StatusInternalServerError)
			return
		}

		response(w, resp, http.StatusOK)
	}
}

func (server *Server) HandleCreateHourse() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		body := new(hourse.CreateHourseRequest)
		if err := json.NewDecoder(r.Body).Decode(body); err != nil {
			responseError(w, err, http.StatusBadRequest)
			return
		}

		if err := server.service.CreateHourse(r.Context(), body); err != nil {
			responseError(w, err, http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusNoContent)
	}
}

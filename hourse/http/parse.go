package http

import (
	"net/http"
	"strconv"
	"strings"

	"github.com/hourse"
	"github.com/shopspring/decimal"
)

func parseGetHoursesRequest(r *http.Request) (*hourse.GetHoursesRequest, error) {
	result := new(hourse.GetHoursesRequest)
	var err error

	city := strings.TrimSpace(r.URL.Query().Get("city"))
	if city != "" {
		result.City = strings.Split(city, ",")
	}

	section := strings.TrimSpace(r.URL.Query().Get("section"))
	if section != "" {
		result.Section = strings.Split(section, ",")
	}

	page := strings.TrimSpace(r.URL.Query().Get("page"))
	if page != "" {
		result.Page, err = strconv.Atoi(page)
		if err != nil {
			return nil, err
		}
	}

	pageSize := strings.TrimSpace(r.URL.Query().Get("page_size"))
	if pageSize != "" {
		result.PageSize, err = strconv.Atoi(pageSize)
		if err != nil {
			return nil, err
		}
	}

	maxPrice := strings.TrimSpace(r.URL.Query().Get("max_price"))
	if maxPrice != "" {
		result.MaxPrice, err = strconv.Atoi(maxPrice)
		if err != nil {
			return nil, err
		}
	}

	minMainArea := strings.TrimSpace(r.URL.Query().Get("min_main_area"))
	if minMainArea != "" {
		result.MinMainArea, err = decimal.NewFromString(minMainArea)
		if err != nil {
			return nil, err
		}
	}

	shape := strings.TrimSpace(r.URL.Query().Get("shape"))
	if shape != "" {
		result.Shape = strings.Split(shape, ",")
	}

	excludedTopFloor := strings.TrimSpace(r.URL.Query().Get("excluded_top_floor"))
	if excludedTopFloor != "" {
		result.ExcludedTopFloor, err = strconv.ParseBool(excludedTopFloor)
		if err != nil {
			return nil, err
		}
	}

	result.Age = strings.TrimSpace(r.URL.Query().Get("age"))

	// if result.Page <= 1 {
	// 	result.Page = viper.GetInt("service.min_page")
	// }

	// if result.PageSize <= 0 {
	// 	result.PageSize = viper.GetInt("service.page_size")
	// }

	return result, nil
}

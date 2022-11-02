package hourse

import (
	"context"
	"time"

	"github.com/hourse/postgres"
	"github.com/shopspring/decimal"
)

type GetHoursesRequest struct {
	City             []string
	Section          []string
	Page             int
	PageSize         int
	MaxPrice         int
	MinMainArea      decimal.Decimal
	Shape            []string
	ExcludedTopFloor bool
}

type GetCitiesResponse struct {
	City []string `json:"city"`
}

type GetSectionsByNameResponse struct {
	Section []string `json:"section"`
}

type GetSectionsWithCity struct {
	City     string   `json:"city"`
	Sections []string `json:"sections"`
}

type GetHourseResponse struct {
	ID        int       `json:"id"`
	Link      string    `json:"link"`
	City      string    `json:"city"`
	Section   string    `json:"section"`
	Address   string    `json:"address"`
	Price     int       `json:"price"`
	Floor     string    `json:"floor"`
	Shape     string    `json:"shape"`
	Age       string    `json:"age"`
	MainArea  string    `json:"main_area"`
	Area      string    `json:"area"`
	Commit    string    `json:"commit"`
	CreatedAt time.Time `json:"created_at"`
}

type CreateHourseRequest struct {
	City     string `json:"city" validate:"required"`
	Section  string `json:"section" validate:"required"`
	Link     string `json:"link" validate:"required"`
	Layout   string `json:"layout,omitempty"`
	Address  string `json:"address" validate:"required"`
	Price    int    `json:"price" validate:"required"`
	Floor    string `json:"floor" validate:"required"`
	Shape    string `json:"shape" validate:"required"`
	Age      string `json:"age" validate:"required"`
	Area     string `json:"area" validate:"required"`
	MainArea string `json:"main_area,omitempty"`
	Raw      string `json:"raw" validate:"required"`
}

type HourseService interface {
	GetHourses(ctx context.Context, in *GetHoursesRequest) ([]GetHourseResponse, error)
	GetCities(ctx context.Context) (*GetCitiesResponse, error)
	GetSectionsByCity(ctx context.Context, name string) (*GetSectionsByNameResponse, error)
	GetSectionsWithCity(ctx context.Context) ([]GetSectionsWithCity, error)
	CreateHourse(ctx context.Context, in *CreateHourseRequest) error
}

type RDS interface {
	GetCities(ctx context.Context) ([]string, error)
	GetHourses(ctx context.Context, arg postgres.GetHoursesParams) ([]postgres.GetHoursesRow, error)
	GetSectionsByCity(ctx context.Context, cityName string) ([]string, error)
	GetSectionsWithCity(ctx context.Context) ([]postgres.GetSectionsWithCityRow, error)
	CreateHourse(ctx context.Context, arg postgres.CreateHourseParams) error
	GetSection(ctx context.Context, arg postgres.GetSectionParams) (postgres.GetSectionRow, error)
}

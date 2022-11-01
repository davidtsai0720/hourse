package hourse

import (
	"context"
	"time"

	"github.com/shopspring/decimal"
)

type GetHourseRequest struct {
	City             []string
	Section          []string
	Page             int
	PageSize         int
	MaxPrice         int
	MinMainArea      decimal.Decimal
	Shape            []string
	ExcludedTopFloor bool
}

type CityResponse struct {
	City []string `json:"city"`
}

type SectionResponse struct {
	Section []string `json:"section"`
}

type HourseResponse struct {
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

type HourseService interface {
	GetHourse(ctx context.Context, in *GetHourseRequest) ([]HourseResponse, error)
	GetCity(ctx context.Context) (*CityResponse, error)
	GetSection(ctx context.Context, name string) (*SectionResponse, error)
}

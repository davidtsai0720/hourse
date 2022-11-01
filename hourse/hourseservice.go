package hourse

import (
	"context"
	"strings"

	"github.com/hourse/postgres"
)

func NewService(db *postgres.Queries) HourseService {
	return &Service{db: db}
}

type Service struct {
	db *postgres.Queries
}

func (service *Service) GetHourse(ctx context.Context, in *GetHourseRequest) ([]HourseResponse, error) {
	request := postgres.GetHourseParams{
		OffsetParam:      int32(in.Page * in.PageSize),
		LimitParam:       int32(in.PageSize),
		MaxPrice:         int32(in.MaxPrice),
		MinMainArea:      in.MinMainArea.String(),
		ExcludedTopFloor: in.ExcludedTopFloor,
	}

	if len(in.City) != 0 {
		request.City = strings.Join(in.City, ",")
	}

	if len(in.Section) != 0 {
		request.Section = strings.Join(in.Section, ",")
	}

	if len(in.Shape) != 0 {
		request.Shape = strings.Join(in.Shape, ",")
	}

	results, err := service.db.GetHourse(ctx, request)

	if err != nil {
		return nil, err
	}

	output := make([]HourseResponse, 0, len(results))
	for _, result := range results {
		output = append(output, HourseResponse{
			ID:        int(result.ID),
			Link:      result.Link,
			City:      result.City.String,
			Section:   result.Section.String,
			Address:   result.Address,
			Price:     int(result.Price),
			Floor:     result.Floor,
			Shape:     result.Shape,
			Age:       result.Age,
			MainArea:  result.MainArea.String,
			Area:      result.Area,
			Commit:    result.Commit,
			CreatedAt: result.CreatedAt,
		})
	}

	return output, nil
}

func (service *Service) GetCity(ctx context.Context) (*CityResponse, error) {
	cities, err := service.db.GetCities(ctx)
	if err != nil {
		return nil, err
	}

	return &CityResponse{City: cities}, nil
}

func (service *Service) GetSection(ctx context.Context, name string) (*SectionResponse, error) {
	section, err := service.db.GetSection(ctx, name)
	if err != nil {
		return nil, err
	}

	return &SectionResponse{Section: section}, nil
}

package hourse

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/go-playground/validator/v10"
	"github.com/hourse/log"
	"github.com/hourse/postgres"
)

func NewService(rds RDS) HourseService {
	return &Service{rds: rds, validator: validator.New()}
}

type Service struct {
	rds       RDS
	validator *validator.Validate
}

func convertToUpsertHourseParams(
	in *UpsertHourseRequest,
	section postgres.GetSectionRow,
) (postgres.UpsertHourseParams, error) {

	floors := strings.Split(in.Floor, "/")
	if len(floors) != 2 {
		return postgres.UpsertHourseParams{}, fmt.Errorf("invalid floor")
	}

	output := postgres.UpsertHourseParams{
		SectionID:    int32(section.ID),
		Link:         in.Link,
		Layout:       sql.NullString{String: in.Layout, Valid: in.Layout != ""},
		Address:      sql.NullString{String: in.Address, Valid: in.Address != ""},
		Price:        in.Price,
		CurrentFloor: floors[0],
		TotalFloor:   floors[1],
		Shape:        in.Shape,
		Age:          in.Age,
		Area:         in.Area,
		MainArea:     sql.NullString{String: in.MainArea, Valid: in.MainArea != ""},
		Raw:          json.RawMessage(in.Raw),
	}
	return output, nil
}

func (service *Service) UpsertHourse(ctx context.Context, in *UpsertHourseRequest) error {
	logger := log.WithContext(ctx)

	if err := service.validator.Struct(in); err != nil {
		logger.Errorf("failed to validate body: %v", in)
		return err
	}

	section, err := service.rds.GetSection(ctx, postgres.GetSectionParams{
		City:    in.City,
		Section: in.Section,
	})
	if err != nil {
		logger.Errorf("failed to get section: %v", err)
		return err
	}

	request, err := convertToUpsertHourseParams(in, section)
	if err != nil {
		logger.Errorf("failed to convert create hourse params: %v", err)
		return err
	}

	if err := service.rds.UpsertHourse(ctx, request); err != nil {
		logger.Errorf("failed to create hourse: %v", err)
		return err
	}

	return nil
}

func convertToGetHoursesParams(in *GetHoursesRequest) postgres.GetHoursesParams {
	request := postgres.GetHoursesParams{
		// OffsetParam:      int32(in.Page * in.PageSize),
		// LimitParam:       in.PageSize,
		MaxPrice:    int32(in.MaxPrice),
		MinMainArea: in.MinMainArea.String(),
		// ExcludedTopFloor: in.ExcludedTopFloor,
		Age: in.Age,
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

	return request
}

func convertToGetHourseResponse(in postgres.GetHoursesRow) GetHourseResponse {
	return GetHourseResponse{
		ID:        int(in.ID),
		Link:      in.Link,
		City:      in.City.String,
		Section:   in.Section.String,
		Address:   in.Address,
		Price:     in.Price,
		Floor:     in.Floor,
		Shape:     in.Shape,
		Age:       in.Age,
		MainArea:  in.MainArea.String,
		Area:      in.Area,
		Commit:    in.Commit,
		CreatedAt: in.CreatedAt,
		Layout:    in.Layout.String,
	}
}

func (service *Service) GetHourses(ctx context.Context, in *GetHoursesRequest) (int64, []GetHourseResponse, error) {
	logger := log.WithContext(ctx)

	results, err := service.rds.GetHourses(ctx, convertToGetHoursesParams(in))
	if err != nil {
		logger.Errorf("failed to get hourse: %v", err)
		return 0, nil, err
	}

	if len(results) == 0 {
		return 0, nil, nil
	}

	output := make([]GetHourseResponse, 0, len(results))
	for _, result := range results {
		output = append(output, convertToGetHourseResponse(result))
	}

	return results[0].TotalCount, output, nil
}

func (service *Service) GetCities(ctx context.Context) (*GetCitiesResponse, error) {
	logger := log.WithContext(ctx)
	cities, err := service.rds.GetCities(ctx)
	if err != nil {
		logger.Errorf("failed ti get cities: %v", err)
		return nil, err
	}

	return &GetCitiesResponse{City: cities}, nil
}

func (service *Service) GetSectionsByCity(ctx context.Context, name string) (*GetSectionsByNameResponse, error) {
	logger := log.WithContext(ctx)
	section, err := service.rds.GetSectionsByCity(ctx, name)
	if err != nil {
		logger.Errorf("failed to get section by city: %v", err)
		return nil, err
	}

	return &GetSectionsByNameResponse{Section: section}, nil
}

func (service *Service) GetSectionsWithCity(ctx context.Context) ([]GetSectionsWithCity, error) {
	logger := log.WithContext(ctx)
	results, err := service.rds.GetSectionsWithCity(ctx)
	if err != nil {
		logger.Error("failed to get section with city: %v", err)
		return nil, err
	}

	mymap := make(map[string][]string)
	for _, row := range results {
		mymap[row.City.String] = append(mymap[row.City.String], row.Section)
	}

	var response []GetSectionsWithCity
	for city, sections := range mymap {
		response = append(response, GetSectionsWithCity{
			City:     city,
			Sections: sections,
		})
	}

	return response, nil
}

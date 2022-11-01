-- name: GetCities :many
SELECT name FROM city;

-- name: GetSection :many
SELECT section.name
FROM section
LEFT JOIN city ON (section.city_id = city.id)
WHERE city.name = @city_name;

-- name: GetHourse :many
WITH duplicate_conditions AS (
    SELECT MIN(id) AS id, section_id, address, age, area
    FROM hourse
    WHERE link LIKE 'https://sale.591.com.tw/home%'
    AND updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
    GROUP BY section_id, address, age, area
    HAVING count(1) > 1
),
duplicate AS (
    SELECT hourse.id
    FROM hourse
    INNER JOIN duplicate_conditions ON(
            hourse.section_id = duplicate_conditions.section_id
        AND hourse.address = duplicate_conditions.address
        AND hourse.age = duplicate_conditions.age
        AND hourse.area = duplicate_conditions.area
        AND hourse.link LIKE 'https://sale.591.com.tw/home%'
    )
    WHERE hourse.id NOT IN (SELECT id FROM duplicate_conditions)
    AND hourse.updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
),
candidates AS (
    SELECT hourse.id
    FROM hourse
    LEFT JOIN section ON (section.id=hourse.section_id)
    LEFT JOIN city ON (city.id=section.city_id)
    WHERE hourse.updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
    AND hourse.id NOT IN (SELECT id FROM duplicate)
    AND hourse.main_area IS NOT NULL
    AND (city.name IN (@city) OR COALESCE(@city, '') = '')
    AND (section.name IN (@section) OR COALESCE(@section, '') = '')
    AND (@max_price = 0 OR hourse.price < @max_price)
    AND (@min_main_area = 0 OR hourse.main_area > @min_main_area :: DECIMAL)
    AND (hourse.shape IN (@shape) OR COALESCE(@shape, '') = '')
    AND (
        CASE
        WHEN @excluded_top_floor :: BOOLEAN THEN hourse.current_floor != hourse.total_floor
        ELSE TRUE
        END
    )
)
SELECT
    hourse.id,
    CONCAT(city.name, section.name, hourse.address) :: TEXT AS address,
    city.name AS city,
    section.name AS section,
    hourse.price,
    hourse.current_floor,
    CONCAT(hourse.current_floor, '/', hourse.total_floor) :: TEXT AS floor,
    hourse.shape,
    hourse.age,
    hourse.main_area,
    hourse.area,
    section.name AS section,
    hourse.link,
    COALESCE(hourse.commit, '') AS commit,
    hourse.created_at,
    (SELECT COUNT(1) FROM candidates) AS total_count
FROM hourse
INNER JOIN candidates USING(id)
LEFT JOIN section ON (section.id=hourse.section_id)
LEFT JOIN city ON (city.id=section.city_id)
ORDER BY city.name, section.name, hourse.age, hourse.price, hourse.address
OFFSET @offset_param :: INTEGER LIMIT @limit_param :: INTEGER;
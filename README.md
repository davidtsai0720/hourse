# house

## **Install Webdriver**

- [Link](https://github.com/mozilla/geckodriver/releases)

## **Start**

```sh
$ python -m venv venv && \
source ./venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt
```

## **Exec**

```sh
$ ./main.py
```

## **Format**

```sh
$ autopep8 --in-place --aggressive *.py --max-line-length 120
```

```sh
$ flask run --host=0.0.0.0 --reload
```

```sql
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
    ORDER BY hourse.address, hourse.age, hourse.area
)
SELECT
    CONCAT(city.name, section.name, hourse.address) AS address,
    hourse.price,
    CONCAT(hourse.current_floor, '/', hourse.total_floor) AS floor,
    hourse.shape,
    hourse.age,
    hourse.main_area,
    hourse.area,
    section.name AS section,
    hourse.link,
    COALESCE(hourse.commit, '') AS commit
FROM hourse
LEFT JOIN section ON (section.id=hourse.section_id)
LEFT JOIN city ON (city.id=section.city_id)
WHERE hourse.updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
AND hourse.id NOT IN (SELECT id FROM duplicate)
AND hourse.main_area IS NOT NULL
ORDER BY city.name, section.name, hourse.age, hourse.price, hourse.address;

SELECT sum(numbackends) FROM pg_stat_database;
```

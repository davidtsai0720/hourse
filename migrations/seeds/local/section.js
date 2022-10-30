const tableName = "section"

var locale = [
    {
        "id": 1,
        "city_id": 1,
        "name": "中正區",
    },
    {
        "id": 2,
        "city_id": 1,
        "name": "萬華區",
    },
    {
        "id": 3,
        "city_id": 1,
        "name": "大同區",
    },
    {
        "id": 4,
        "city_id": 1,
        "name": "中山區",
    },
    {
        "id": 5,
        "city_id": 1,
        "name": "松山區",
    },
    {
        "id": 6,
        "city_id": 1,
        "name": "大安區",
    },
    {
        "id": 7,
        "city_id": 1,
        "name": "信義區",
    },
    {
        "id": 8,
        "city_id": 1,
        "name": "內湖區",
    },
    {
        "id": 9,
        "city_id": 1,
        "name": "南港區",
    },
    {
        "id": 10,
        "city_id": 1,
        "name": "士林區",
    },
    {
        "id": 11,
        "city_id": 1,
        "name": "北投區",
    },
    {
        "id": 12,
        "city_id": 1,
        "name": "文山區",
    },
    {
        "id": 13,
        "city_id": 2,
        "name": "土城區",
    },
    {
        "id": 14,
        "city_id": 2,
        "name": "雙溪區",
    },
    {
        "id": 15,
        "city_id": 2,
        "name": "鶯歌區",
    },
    {
        "id": 16,
        "city_id": 2,
        "name": "萬里區",
    },
    {
        "id": 17,
        "city_id": 2,
        "name": "三重區",
    },
    {
        "id": 18,
        "city_id": 2,
        "name": "中和區",
    },
    {
        "id": 19,
        "city_id": 2,
        "name": "八里區",
    },
    {
        "id": 20,
        "city_id": 2,
        "name": "蘆洲區",
    },
    {
        "id": 21,
        "city_id": 2,
        "name": "林口區",
    },
    {
        "id": 22,
        "city_id": 2,
        "name": "汐止區",
    },
    {
        "id": 23,
        "city_id": 2,
        "name": "泰山區",
    },
    {
        "id": 24,
        "city_id": 2,
        "name": "淡水區",
    },
    {
        "id": 25,
        "city_id": 2,
        "name": "瑞芳區",
    },
    {
        "id": 26,
        "city_id": 2,
        "name": "石碇區",
    },
    {
        "id": 27,
        "city_id": 2,
        "name": "石門區",
    },
    {
        "id": 28,
        "city_id": 2,
        "name": "五股區",
    },
    {
        "id": 29,
        "city_id": 2,
        "name": "平溪區",
    },
    {
        "id": 30,
        "city_id": 2,
        "name": "貢寮區",
    },
    {
        "id": 31,
        "city_id": 2,
        "name": "坪林區",
    },
    {
        "id": 32,
        "city_id": 2,
        "name": "金山區",
    },
    {
        "id": 33,
        "city_id": 2,
        "name": "三芝區",
    },
    {
        "id": 34,
        "city_id": 2,
        "name": "永和區",
    },
    {
        "id": 35,
        "city_id": 2,
        "name": "新店區",
    },
    {
        "id": 36,
        "city_id": 2,
        "name": "板橋區",
    },
    {
        "id": 37,
        "city_id": 2,
        "name": "樹林區",
    },
    {
        "id": 38,
        "city_id": 2,
        "name": "深坑區",
    },
    {
        "id": 39,
        "city_id": 2,
        "name": "三峽區",
    },
    {
        "id": 40,
        "city_id": 2,
        "name": "烏來區",
    },
    {
        "id": 41,
        "city_id": 2,
        "name": "新莊區",
    },
]

exports.seed = function(knex, Promise) {
    return knex(tableName).del().then(() => {
        return knex(tableName).insert(locale);
    });
}
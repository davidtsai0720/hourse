const tableName = "city"

var locale = [
    {
        "id": 1,
        "name": "台北市",
    },
    {
        "id": 2,
        "name": "新北市",
    }
]

exports.seed = function(knex, Promise) {
    return knex(tableName).del().then(() => {
        return knex(tableName).insert(locale);
    });
}
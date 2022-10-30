exports.up = function(knex, Promise) {
    return knex.schema.createTable('city', table => {
            table.increments('id').primary()
            table.string('name').notNullable()
            table.timestamp('created_at').defaultTo(knex.raw('CURRENT_TIMESTAMP'))
            table.timestamp('deleted_at')
            table.unique('name')
        })
};

exports.down = function(knex, Promise) {
    return knex.schema.dropTableIfExists('city')
};
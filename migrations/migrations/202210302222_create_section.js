exports.up = function(knex, Promise) {
    return knex.schema.createTable('section', table => {
            table.increments('id').primary()
            table.integer('city_id').notNullable()
            table.string('name').notNullable()
            table.timestamp('created_at').defaultTo(knex.raw('CURRENT_TIMESTAMP'))
            table.timestamp('deleted_at')
            table.unique(['name', 'city_id'])
            table.foreign('city_id').references('id').inTable('city').onUpdate('CASCADE').onDelete('CASCADE')
        })
};

exports.down = function(knex, Promise) {
    return knex.schema.dropTableIfExists('section')
};
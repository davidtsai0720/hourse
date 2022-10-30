exports.up = function(knex, Promise) {
    return knex.schema.createTable('hourse', table => {
            table.increments('id').primary()
            table.integer('section_id').notNullable()
            table.string('link').notNullable()
            table.string('layout')
            table.string('address').notNullable()
            table.string('section').notNullable()
            table.string('price').notNullable()
            table.string('floor').notNullable()
            table.string('shape').notNullable()
            table.string('age').notNullable()
            table.string('area').notNullable()
            table.string('main_area')
            table.timestamp('created_at').defaultTo(knex.raw('CURRENT_TIMESTAMP'))
            table.timestamp('updated_at').defaultTo(knex.raw('CURRENT_TIMESTAMP'))
            table.timestamp('deleted_at')
            table.foreign('section_id').references('id').inTable('section').onUpdate('CASCADE').onDelete('CASCADE')
            table.unique('link')
        })
};

exports.down = function(knex, Promise) {
    return knex.schema.dropTableIfExists('hourse')
};
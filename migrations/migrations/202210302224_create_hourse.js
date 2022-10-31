exports.up = function(knex, Promise) {
    return knex.schema.createTable('hourse', table => {
            table.increments('id').primary()
            table.integer('section_id').notNullable()
            table.string('link', 128).notNullable()
            table.string('layout', 32)
            table.string('address', 64).notNullable()
            table.integer('price', 6).notNullable()
            table.string('floor', 16).notNullable()
            table.string('shape', 16).notNullable()
            table.string('age', 16).notNullable()
            table.decimal('area', 4, 2).notNullable()
            table.decimal('main_area', 4, 2)
            table.string('commit')
            table.jsonb('raw').notNullable()
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
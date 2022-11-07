const local = {
    client: 'postgresql',
    connection: {
        host: '127.0.0.1',
        user: 'postgres',
        password: 'postgres',
        port: 5432,
        database: 'hourse',
    },
    seeds: {
        directory: './seeds/local'
    }
}

module.exports = { local }
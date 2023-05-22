import { Client } from "pg"
// import createSubscriber from "pg-listen"

const pgClient = new Client({
    host: 'localhost',
    port: 5433,
    database: 'agregator_messages',
    user: 'postgres',
    password: 'WRCOIN',
})

// pgClient.connect()

// export default pgClient

export default {
    pgClient
}
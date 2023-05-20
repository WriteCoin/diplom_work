import axios from 'axios'

const isDev = process.env.NODE_ENV === 'development'

export const $url = isDev ? 'http://localhost:5000/' : process.env.API_URL

let config
if (isDev) {
    config = {
        baseURL: $url,
        headers: {
            'Access-Control-Allow-Origin': 'http://localhost:3000' 
        }
    }
} else {
    config = {
        baseURL: $url
    }
}

export const $host = axios.create(config)
import axios from 'axios'

const isDev = process.env.NODE_ENV === 'development'

// console.log('API_URL', process.env.API_URL)

export const $url = isDev ? 'http://localhost:5000/' : process.env.REACT_APP_API_URL

let config
if (isDev) {
    config = {
        baseURL: $url,
        headers: {
            'Access-Control-Allow-Origin': `http://localhost:${process.env.PORT}`,
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Headers': 'content-type'
        }
    }
} else {
    config = {
        baseURL: $url
    }
}

export const $host = axios.create(config)
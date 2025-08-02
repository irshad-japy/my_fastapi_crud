import axios from 'axios'

const http = axios.create({
  baseURL: 'http://localhost:8000',  // FastAPI local dev
  headers: {
    'Content-Type': 'application/json'
  }
})

export default http

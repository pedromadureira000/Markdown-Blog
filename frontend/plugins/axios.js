import axios from 'axios'
 
export default axios.create({
	xsrfHeaderName: 'X-CSRFToken',
	xsrfCookieName: 'csrftoken',
  baseURL: process.env.GENERATE_PROXY_URL,
  // baseURL: "http://127.0.0.1:8000",
	withCredentials: true,
  timeout: 15000
})

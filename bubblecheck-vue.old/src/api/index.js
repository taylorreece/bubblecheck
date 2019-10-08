import axios from 'axios'

const API_URL = '/api'

// ==================================================
// Course API Calls
export function fetchCourses () {
  return axios.get(`${API_URL}/course/list`)
}

export function postNewCourse (course) {
  return axios.post(`${API_URL}/course/add`, course)
}

export function fetchCourse (courseId) {
  return axios.get(`${API_URL}/course/get/${courseId}`)
}

export function updateCourse (course, courseId) {
  return axios.put(`${API_URL}/course/update/${courseId}`, course)
}

// ==================================================
// User API calls

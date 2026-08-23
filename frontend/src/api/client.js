const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const token = localStorage.getItem('school_access_token')
  const headers = new Headers(options.headers || {})
  if (options.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  const contentType = response.headers.get('content-type') || ''
  const payload = contentType.includes('application/json') ? await response.json() : null
  if (!response.ok) {
    const detail = payload?.detail || payload?.message || `Request failed (${response.status})`
    throw new Error(detail)
  }
  return payload
}

export const api = {
  login: (username, password) => {
    const body = new URLSearchParams({ username, password })
    return request('/auth/login', { method: 'POST', body, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  },
  me: () => request('/auth/me'),
  students: () => request('/students/'),
  createStudent: (student) => request('/students/', { method: 'POST', body: JSON.stringify(student) }),
  updateStudent: (id, student) => request(`/students/${id}`, { method: 'PATCH', body: JSON.stringify(student) }),
  deleteStudent: (id) => request(`/students/${id}`, { method: 'DELETE' }),
  classes: () => request('/classes/'),
  createClass: (item) => request('/classes/', { method: 'POST', body: JSON.stringify(item) }),
  posts: () => request('/posts/'),
  createPost: (post) => request('/posts/', { method: 'POST', body: JSON.stringify(post) }),
  deletePost: (id) => request(`/posts/${id}`, { method: 'DELETE' }),
}

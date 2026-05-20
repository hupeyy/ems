import api from '../api/axios'

export const authService = {
  login:    (email: string, password: string) => api.post('/auth/login',    { email, password }),
  register: (email: string, password: string) => api.post('/auth/register', { email, password }),
  me:       ()                                => api.get('/auth/me'),
}
import api from '../api/axios'

export type EmployeeStatus = 'Active' | 'Inactive' | 'On Leave' | 'Terminated' | 'Retired'

export interface EmployeeCreate {
  employeeId: string
  name: string
  email: string
  department: string
  position: string
  status?: EmployeeStatus
}

export interface EmployeeUpdate {
  employeeId?: string
  name?: string
  email?: string
  department?: string
  position?: string
  status?: EmployeeStatus
}

export const employeeService = {
  list:   ()                                 => api.get('/employees'),
  get:    (id: string)                       => api.get(`/employees/${id}`),
  create: (data: EmployeeCreate)             => api.post('/employees', data),
  update: (id: string, data: EmployeeUpdate) => api.put(`/employees/${id}`, data),
  remove: (id: string)                       => api.delete(`/employees/${id}`),
}

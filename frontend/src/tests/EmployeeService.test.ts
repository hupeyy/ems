import { beforeEach, describe, expect, test, vi } from 'vitest'
import api from '../api/axios'
import { employeeService } from '../services/EmployeeService'

vi.mock('../api/axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

describe('employeeService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('list gets /employees', async () => {
    const mockedResponse = { data: [] }
    vi.mocked(api.get).mockResolvedValue(mockedResponse as any)

    const response = await employeeService.list()

    expect(api.get).toHaveBeenCalledWith('/employees')
    expect(response).toBe(mockedResponse)
  })

  test('create posts employee data to /employees', async () => {
    const payload = {
      employeeId: 'EMP12345',
      name: 'Jane Doe',
      email: 'jane.doe@example.com',
      department: 'Engineering',
      position: 'Software Engineer',
      status: 'Active' as const,
    }
    const mockedResponse = { data: payload }
    vi.mocked(api.post).mockResolvedValue(mockedResponse as any)

    const response = await employeeService.create(payload)

    expect(api.post).toHaveBeenCalledWith('/employees', payload)
    expect(response).toBe(mockedResponse)
  })

  test('update puts employee data to /employees/:id', async () => {
    const payload = { position: 'Senior Software Engineer' }
    const mockedResponse = { data: { ...payload, employeeId: 'EMP12345' } }
    vi.mocked(api.put).mockResolvedValue(mockedResponse as any)

    const response = await employeeService.update('EMP12345', payload)

    expect(api.put).toHaveBeenCalledWith('/employees/EMP12345', payload)
    expect(response).toBe(mockedResponse)
  })

  test('remove deletes /employees/:id', async () => {
    const mockedResponse = { data: { ok: true } }
    vi.mocked(api.delete).mockResolvedValue(mockedResponse as any)

    const response = await employeeService.remove('EMP12345')

    expect(api.delete).toHaveBeenCalledWith('/employees/EMP12345')
    expect(response).toBe(mockedResponse)
  })
})

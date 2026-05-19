import { beforeEach, describe, expect, test, vi } from 'vitest'
import api from '../api/axios'
import { employeeService } from '../services/employeeService'

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

  test('list rejects on API error', async () => {
    const error = new Error('Failed to fetch')
    vi.mocked(api.get).mockRejectedValue(error)

    await expect(employeeService.list()).rejects.toThrow('Failed to fetch')
  })

  test('create rejects on API error', async () => {
    const payload = {
      employeeId: 'EMP12345',
      name: 'Jane Doe',
      email: 'jane.doe@example.com',
      department: 'Engineering',
      position: 'Software Engineer',
    }
    const error = new Error('Invalid employee data')
    vi.mocked(api.post).mockRejectedValue(error)

    await expect(employeeService.create(payload)).rejects.toThrow('Invalid employee data')
  })

  test('update rejects on API error', async () => {
    const payload = { position: 'Senior Engineer' }
    const error = new Error('Employee not found')
    vi.mocked(api.put).mockRejectedValue(error)

    await expect(employeeService.update('EMP12345', payload)).rejects.toThrow('Employee not found')
  })

  test('remove rejects on API error', async () => {
    const error = new Error('Cannot delete')
    vi.mocked(api.delete).mockRejectedValue(error)

    await expect(employeeService.remove('EMP12345')).rejects.toThrow('Cannot delete')
  })
})

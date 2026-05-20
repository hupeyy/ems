import { renderHook, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, test, vi } from 'vitest'
import { employeeService } from '../services/employeeService'
import { useEmployees } from '../hooks/useEmployees'

vi.mock('../services/employeeService', () => ({
  employeeService: {
    list: vi.fn(),
  },
}))

describe('useEmployees', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('starts with loading=true and empty employees', () => {
    vi.mocked(employeeService.list).mockImplementation(() => new Promise(() => {})) // Never resolves

    const { result } = renderHook(() => useEmployees())

    expect(result.current.loading).toBe(true)
    expect(result.current.employees).toEqual([])
    expect(result.current.error).toBe(null)
  })

  test('loads employees successfully', async () => {
    const mockEmployees = [
      {
        employeeId: 'EMP00001',
        name: 'John Doe',
        email: 'john@example.com',
        department: 'Engineering',
        position: 'Software Engineer',
        status: 'Active',
      },
    ]
    vi.mocked(employeeService.list).mockResolvedValue({ data: mockEmployees } as any)

    const { result } = renderHook(() => useEmployees())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.employees).toEqual(mockEmployees)
    expect(result.current.error).toBe(null)
  })

  test('handles error when fetching fails', async () => {
    const error = new Error('Failed to load')
    const axiosError = {
      response: { data: { detail: 'Connection failed' } },
    }
    vi.mocked(employeeService.list).mockRejectedValue(axiosError)

    const { result } = renderHook(() => useEmployees())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.employees).toEqual([])
    expect(result.current.error).toBe('Connection failed')
  })

  test('uses fallback error message when no detail provided', async () => {
    const axiosError = { response: { data: {} } }
    vi.mocked(employeeService.list).mockRejectedValue(axiosError)

    const { result } = renderHook(() => useEmployees())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to load employees')
  })

  test('calls employeeService.list on mount', async () => {
    vi.mocked(employeeService.list).mockResolvedValue({ data: [] } as any)

    renderHook(() => useEmployees())

    await waitFor(() => {
      expect(employeeService.list).toHaveBeenCalledTimes(1)
    })
  })
})

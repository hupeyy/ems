import { renderHook, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, test, vi } from 'vitest'
import { authService } from '../services/authService'
import { useCurrentUser } from '../hooks/useCurrentUser'

vi.mock('../services/authService', () => ({
  authService: {
    me: vi.fn(),
  },
}))

describe('useCurrentUser', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('starts with loading=true and null user', () => {
    vi.mocked(authService.me).mockImplementation(() => new Promise(() => {})) // Never resolves

    const { result } = renderHook(() => useCurrentUser())

    expect(result.current.loading).toBe(true)
    expect(result.current.user).toBe(null)
    expect(result.current.error).toBe(null)
  })

  test('loads current user successfully', async () => {
    const mockUser = {
      id: '1',
      email: 'test@example.com',
      role: 'user' as const,
    }
    vi.mocked(authService.me).mockResolvedValue({ data: mockUser } as any)

    const { result } = renderHook(() => useCurrentUser())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.user).toEqual(mockUser)
    expect(result.current.error).toBe(null)
  })

  test('handles error when fetching current user fails', async () => {
    const axiosError = {
      response: { data: { detail: 'Not authenticated' } },
    }
    vi.mocked(authService.me).mockRejectedValue(axiosError)

    const { result } = renderHook(() => useCurrentUser())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.user).toBe(null)
    expect(result.current.error).toBe('Not authenticated')
  })

  test('uses fallback error message when no detail provided', async () => {
    const axiosError = { response: { data: {} } }
    vi.mocked(authService.me).mockRejectedValue(axiosError)

    const { result } = renderHook(() => useCurrentUser())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to load user')
  })

  test('calls authService.me on mount', async () => {
    vi.mocked(authService.me).mockResolvedValue({ data: { id: '1', email: 'test@example.com', role: 'user' } } as any)

    renderHook(() => useCurrentUser())

    await waitFor(() => {
      expect(authService.me).toHaveBeenCalledTimes(1)
    })
  })

  test('handles admin role correctly', async () => {
    const adminUser = {
      id: '2',
      email: 'admin@example.com',
      role: 'admin' as const,
    }
    vi.mocked(authService.me).mockResolvedValue({ data: adminUser } as any)

    const { result } = renderHook(() => useCurrentUser())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.user?.role).toBe('admin')
  })
})

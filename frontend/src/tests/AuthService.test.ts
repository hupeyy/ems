import { beforeEach, describe, expect, test, vi } from 'vitest'
import api from '../api/axios'
import { authService } from '../services/authService'

vi.mock('../api/axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('login posts credentials to /auth/login', async () => {
    const mockedResponse = { data: { access_token: 'token' } }
    vi.mocked(api.post).mockResolvedValue(mockedResponse as any)

    const response = await authService.login('test@example.com', 'password123')

    expect(api.post).toHaveBeenCalledWith('/auth/login', {
      email: 'test@example.com',
      password: 'password123',
    })
    expect(response).toBe(mockedResponse)
  })

  test('register posts credentials to /auth/register', async () => {
    const mockedResponse = { data: { id: '1', email: 'test@example.com' } }
    vi.mocked(api.post).mockResolvedValue(mockedResponse as any)

    const response = await authService.register('test@example.com', 'password123')

    expect(api.post).toHaveBeenCalledWith('/auth/register', {
      email: 'test@example.com',
      password: 'password123',
    })
    expect(response).toBe(mockedResponse)
  })

  test('me gets /auth/me', async () => {
    const mockedResponse = { data: { id: '1', email: 'test@example.com', role: 'user' } }
    vi.mocked(api.get).mockResolvedValue(mockedResponse as any)

    const response = await authService.me()

    expect(api.get).toHaveBeenCalledWith('/auth/me')
    expect(response).toBe(mockedResponse)
  })

  test('login rejects on API error', async () => {
    const error = new Error('Network error')
    vi.mocked(api.post).mockRejectedValue(error)

    await expect(authService.login('test@example.com', 'password123')).rejects.toThrow('Network error')
  })

  test('register rejects on API error', async () => {
    const error = new Error('Email already exists')
    vi.mocked(api.post).mockRejectedValue(error)

    await expect(authService.register('test@example.com', 'password123')).rejects.toThrow('Email already exists')
  })

  test('me rejects on API error', async () => {
    const error = new Error('Unauthorized')
    vi.mocked(api.get).mockRejectedValue(error)

    await expect(authService.me()).rejects.toThrow('Unauthorized')
  })
})

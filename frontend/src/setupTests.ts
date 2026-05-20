import '@testing-library/jest-dom'
import { afterEach, vi } from 'vitest'

afterEach(() => {
  localStorage.clear()
  vi.restoreAllMocks() // Restore all mocks after each test to ensure test isolation
  
})
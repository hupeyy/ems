import { useEffect, useState } from 'react'
import { authService } from '../services/AuthService'

export interface User {
  id: string
  email: string
  role: 'admin' | 'user'
}

export function useCurrentUser() {
  const [user, setUser]       = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState<string | null>(null)

  useEffect(() => {
    authService.me()
      .then(({ data }) => setUser(data))
      .catch((err)     => setError(err.response?.data?.detail ?? 'Failed to load user'))
      .finally(()      => setLoading(false))
  }, [])

  return { user, loading, error }
}
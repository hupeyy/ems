import { useEffect, useState } from 'react'
import { employeeService } from '../services/employeeService'

export interface Employee {
  employeeId: string
  name: string
  email: string
  department: string
  position: string
  status: string
}

export function useEmployees() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState<string | null>(null)

  useEffect(() => {
    employeeService.list()
      .then(({ data }) => setEmployees(data))
      .catch((err)     => setError(err.response?.data?.detail ?? 'Failed to load employees'))
      .finally(()      => setLoading(false))
  }, [])

  return { employees, loading, error }
}
import { useEmployees } from "../hooks/useEmployees";


function EmployeesList() {
    const { employees, loading, error } = useEmployees();

    return (
        <div className="page-content">
            <h2 className="section-title">Employees List</h2>
            {loading && <p>Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {!loading && !error && (
                <ul className="employees-list">
                    {employees.map(emp => (
                        <li className="employee-card" key={emp.employeeId}>
                            <strong>{emp.name}</strong> - {emp.position} in {emp.department} ({emp.status})
                        </li>
                    ))}
                </ul>
            )}
        </div>

    )
}

export default EmployeesList
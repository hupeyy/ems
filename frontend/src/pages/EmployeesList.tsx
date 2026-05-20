import { useNavigate } from "react-router-dom";
import { useEmployees } from "../hooks/useEmployees";
import { employeeService } from "../services/employeeService";


function EmployeesList() {
    const { employees, loading, error } = useEmployees();
    const navigate = useNavigate();

    const handleDelete = async (id: string) => {
        if (!confirm(`Delete employee ${id}?`)) return;
        try {
            await employeeService.remove(id);
            window.location.reload();
        } catch {
            alert('Failed to delete employee');
        }
    };

    return (
        <div className="page-content">
            <h2 className="section-title">Employees List</h2>
            {loading && <p>Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {!loading && !error && (
                <>
                <div className="list-toolbar">
                    <button className="form-button" onClick={() => navigate('/employees/form')}>+ Add Employee</button>
                </div>
                <ul className="employees-list">
                    {employees.map(emp => (
                        <li className="employee-card" key={emp.employeeId}>
                            <div className="employee-card-info">
                                <strong>{emp.name}</strong> — {emp.position} in {emp.department} ({emp.status})
                            </div>
                            <div className="employee-card-actions">
                                <button className="btn-secondary btn-sm" onClick={() => navigate('/employees/form', { state: { employee: emp } })}>Edit</button>
                                <button className="btn-danger btn-sm" onClick={() => handleDelete(emp.employeeId)}>Delete</button>
                            </div>
                        </li>
                    ))}
                </ul>
                </>
            )}
        </div>

    )
}

export default EmployeesList
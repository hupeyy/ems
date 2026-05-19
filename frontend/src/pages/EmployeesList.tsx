import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { employeeService } from "../services/EmployeeService";
import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";

interface Employee {
    employeeId: string;
    name: string;
    email: string;
    department: string;
    position: string;
    status: string;
}


function EmployeesList() {
    const [employees, setEmployees] = useState<Employee[]>([]);

    useEffect(() => {
        employeeService.list()
            .then(res => setEmployees(res.data))
            .catch(err => console.error('Failed to fetch employees:', err))
    }
    ,[])

    return (
        <div className="page-content">
            <h2 className="section-title">Employees List</h2>
            <ul className="employees-list">
                {employees.map(emp => (
                    <li className="employee-card" key={emp.employeeId}>
                        <strong>{emp.name}</strong> - {emp.position} in {emp.department} ({emp.status})
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default EmployeesList
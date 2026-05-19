import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";
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
        api.get('/employees').then(res => setEmployees(res.data))
    }
    ,[])

    return (
        <div>
            <h2>Employees List</h2>
            <ul>
                {employees.map(emp => (
                    <li key={emp.employeeId}>
                        <h3>{emp.name}</h3>
                        <p>Email: {emp.email}</p>
                        <p>Department: {emp.department}</p>
                        <p>Position: {emp.position}</p>
                        <p>Status: {emp.status}</p>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default EmployeesList
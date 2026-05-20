import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { test, expect, vi } from "vitest";
import { employeeService } from '../services/employeeService';
import EmployeesList from "../pages/EmployeesList";

vi.mock('../services/employeeService', () => ({
    employeeService: {
        list: vi.fn().mockResolvedValue({ data: [{
            "employeeId": "EMP00001",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "department": "Engineering",
            "position": "Software Engineer",
            "status": "Active",
        }] }),
    }
}));

test('render list of employees after successful login', async () => {

    render(
        <AuthProvider>
            <MemoryRouter>
                <EmployeesList />
            </MemoryRouter>
        </AuthProvider>
    )

    await waitFor(() => {
        expect(employeeService.list).toHaveBeenCalled();
        expect(screen.getByText(/john doe/i)).toBeInTheDocument();
    });
});
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { test, expect, vi } from "vitest";
import api from '../api/axios';
import EmployeesList from "../pages/EmployeesList";

vi.mock('../api/axios');

test('render list of employees after successful login', async () => {
    api.get = vi.fn().mockResolvedValue({ data: [{   
        "employeeId": "EMP00001",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "position": "Software Engineer",
        "status": "Active",
    }] });

    render(
        <AuthProvider>
            <MemoryRouter>
                <EmployeesList />
            </MemoryRouter>
        </AuthProvider>
    )

    await waitFor(() => {
        expect(api.get).toHaveBeenCalledWith('/employees');
        expect(screen.getByText(/john doe/i)).toBeInTheDocument();
    });
});
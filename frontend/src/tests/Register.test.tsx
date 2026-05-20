import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { test, expect, vi } from "vitest";
import { authService } from '../services/authService';
import Register from "../pages/Register";

vi.mock('../services/authService', () => ({
    authService: {
        register: vi.fn().mockResolvedValue({ data: { access_token: 'fake-token' } }),
    }
}));

test('registers a new user successfully', async () => {
    render(
        <AuthProvider>
            <MemoryRouter>
                <Register />
            </MemoryRouter>
        </AuthProvider>
    )

    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/^password$/i), { target: { value: 'password123' } });
    fireEvent.change(screen.getByPlaceholderText(/confirm password/i), { target: { value: 'password123' } });
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'user' } });

    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await waitFor(() => {
        expect(authService.register).toHaveBeenCalledWith('test@example.com', 'password123');
    });
});
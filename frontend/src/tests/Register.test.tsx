import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { test, expect, vi } from "vitest";
import api from '../api/axios';
import Register from "../pages/Register";

vi.mock('../api/axios');

test('registers a new user successfully', async () => {
    api.post = vi.fn().mockResolvedValue({ data: { message: 'User registered successfully' } });

    render(
        <AuthProvider>
            <MemoryRouter>
                <Register />
            </MemoryRouter>
        </AuthProvider>
    )

    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/^password$/i), { target: { value: 'password' } });
    fireEvent.change(screen.getByPlaceholderText(/confirm password/i), { target: { value: 'password' } });
    fireEvent.change(screen.getByPlaceholderText(/role/i), { target: { value: 'user' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await waitFor(() => {
        expect(api.post).toHaveBeenCalledWith('/auth/register', { email: 'test@example.com', password: 'password', confirmPassword: 'password' });
    });
});
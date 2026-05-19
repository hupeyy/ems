import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Login from '../pages/Login';
import { AuthProvider } from "../context/AuthContext";
import { test, expect, vi } from "vitest";
import api from '../api/axios';

vi.mock('../api/axios');

test('stored token and redirects to /employees on successful login', async () => {
    api.post = vi.fn().mockResolvedValue({ data: { token: 'fake-jwt', token_type: 'Bearer' } });

    render(
        <AuthProvider>
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        </AuthProvider>
    )

    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
        expect(api.post).toHaveBeenCalledWith('/auth/login', { username: 'test@example.com', password: 'password' });
        expect(localStorage.getItem('token')).toBe('fake-jwt');
    });
});
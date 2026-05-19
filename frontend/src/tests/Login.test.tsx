import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Login from '../pages/Login';
import { AuthProvider } from "../context/AuthContext";
import { test, expect, vi } from "vitest";
import { authService } from '../services/AuthService';

vi.mock('../services/AuthService', () => ({
    authService: {
        login: vi.fn().mockResolvedValue({ data: { access_token: 'fake-jwt', token_type: 'Bearer' } }),
    }
}));

test('stored token and redirects to /employees on successful login', async () => {

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
        expect(authService.login).toHaveBeenCalledWith('test@example.com', 'password');
        expect(localStorage.getItem('token')).toBe('fake-jwt');
    });
});
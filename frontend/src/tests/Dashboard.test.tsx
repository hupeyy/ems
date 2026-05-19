import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";
import Dashboard from "../pages/Dashboard";

const mockNavigate = vi.fn();
const mockUseCurrentUser = vi.fn();

vi.mock("react-router-dom", async () => {
	const actual = await vi.importActual<typeof import("react-router-dom")>("react-router-dom");
	return {
		...actual,
		useNavigate: () => mockNavigate,
	};
});

vi.mock("../hooks/UseCurrentUser", () => ({
	useCurrentUser: () => mockUseCurrentUser(),
}));

describe("Dashboard", () => {
	beforeEach(() => {
		vi.clearAllMocks();
		mockUseCurrentUser.mockReturnValue({
			user: null,
			loading: false,
			error: null,
		});
	});

	test("shows loading state", () => {
		mockUseCurrentUser.mockReturnValue({
			user: null,
			loading: true,
			error: null,
		});

		render(<Dashboard />);

		expect(screen.getByText(/loading/i)).toBeInTheDocument();
	});

	test("shows error state", () => {
		mockUseCurrentUser.mockReturnValue({
			user: null,
			loading: false,
			error: "Failed to load user",
		});

		render(<Dashboard />);

		expect(screen.getByText(/failed to load user/i)).toBeInTheDocument();
	});

	test("shows user details when loaded", () => {
		mockUseCurrentUser.mockReturnValue({
			user: {
				id: "1",
				email: "admin@example.com",
				role: "admin",
			},
			loading: false,
			error: null,
		});

		render(<Dashboard />);

		expect(screen.getByText(/email:/i)).toBeInTheDocument();
		expect(screen.getByText(/admin@example.com/i)).toBeInTheDocument();
		expect(screen.getByText(/role:/i)).toBeInTheDocument();
		expect(screen.getByText(/^admin$/i)).toBeInTheDocument();
	});

	test("navigates to employees when button is clicked", () => {
		render(<Dashboard />);

		fireEvent.click(screen.getByRole("button", { name: /view all employees/i }));

		expect(mockNavigate).toHaveBeenCalledWith("/employees");
	});
});

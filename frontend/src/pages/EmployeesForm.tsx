import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { employeeService, type EmployeeCreate, type EmployeeStatus } from "../services/employeeService";

const STATUS_OPTIONS: EmployeeStatus[] = ['Active', 'Inactive', 'On Leave', 'Terminated', 'Retired'];

const EMPTY_FORM: EmployeeCreate = {
    employeeId: '',
    name: '',
    email: '',
    department: '',
    position: '',
    status: 'Active',
};

function EmployeesForm() {
    const location = useLocation();
    const existing: EmployeeCreate | undefined = location.state?.employee;
    const isEdit = Boolean(existing);
    const navigate = useNavigate();

    const [form, setForm] = useState<EmployeeCreate>(existing ?? EMPTY_FORM);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);
        setSuccess(null);
        try {
            if (isEdit) {
                await employeeService.update(form.employeeId, form);
                setSuccess('Employee updated successfully');
            } else {
                await employeeService.create(form);
                setSuccess('Employee created successfully');
                setForm(EMPTY_FORM);
            }
        } catch (err: any) {
            const detail = err?.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.map((d: any) => d.msg).join(', '));
            } else {
                setError(detail ?? (isEdit ? 'Failed to update employee' : 'Failed to create employee'));
            }
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="page-content">
            <div className="form-page-header">
                <h2 className="section-title">{isEdit ? 'Edit Employee' : 'Add Employee'}</h2>
                <button className="btn-secondary" onClick={() => navigate('/employees/form')}>
                    Reset
                </button>
            </div>

            <div className="employee-form-card">
                <form className="employee-form" onSubmit={handleSubmit}>
                    <div className="form-row">
                        <div className="form-group">
                            <label className="field-label" htmlFor="employeeId">Employee ID</label>
                            <input
                                id="employeeId"
                                className="form-input"
                                name="employeeId"
                                placeholder="EMP12345"
                                value={form.employeeId}
                                onChange={handleChange}
                                pattern="^EMP[0-9]{5}$"
                                title="Format: EMP followed by 5 digits (e.g. EMP12345)"
                                disabled={isEdit}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="field-label" htmlFor="name">Full Name</label>
                            <input
                                id="name"
                                className="form-input"
                                name="name"
                                placeholder="Jane Doe"
                                value={form.name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label className="field-label" htmlFor="email">Email</label>
                            <input
                                id="email"
                                className="form-input"
                                name="email"
                                type="email"
                                placeholder="jane.doe@example.com"
                                value={form.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="field-label" htmlFor="department">Department</label>
                            <input
                                id="department"
                                className="form-input"
                                name="department"
                                placeholder="Engineering"
                                value={form.department}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label className="field-label" htmlFor="position">Position</label>
                            <input
                                id="position"
                                className="form-input"
                                name="position"
                                placeholder="Software Engineer"
                                value={form.position}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="field-label" htmlFor="status">Status</label>
                            <select
                                id="status"
                                className="form-input"
                                name="status"
                                value={form.status}
                                onChange={handleChange}
                            >
                                {STATUS_OPTIONS.map(s => (
                                    <option key={s} value={s}>{s}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {error && <p className="error-message">{error}</p>}
                    {success && <p className="success-message">{success}</p>}

                    <div className="form-actions">
                        <button className="btn-secondary" type="button" onClick={() => navigate('/employees/form')}>
                            Clear
                        </button>
                        <button className="form-button" type="submit" disabled={submitting}>
                            {submitting ? 'Saving...' : isEdit ? 'Update Employee' : 'Add Employee'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default EmployeesForm;

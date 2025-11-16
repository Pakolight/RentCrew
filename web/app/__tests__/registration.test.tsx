import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { createMemoryRouter, RouterProvider } from 'react-router';
import Registration, { action } from '../routes/registration';

// Mock crypto for password generation
vi.mock('crypto', () => ({
  randomBytes: () => ({
    toString: () => 'mockedBase64String',
    replace: () => 'mockedPassword',
    slice: () => 'mockedPassword',
  }),
}));

// Mock dotenv
vi.mock('dotenv', () => ({
  config: vi.fn(),
}));

describe('Registration Form', () => {
  // Setup fake data for form submission
  const fakeUserData = {
    email: 'test@example.com',
    first_name: 'Test',
    last_name: 'User',
  };

  const fakeCompanyData = {
    legalName: 'Test Company',
    country: 'United States',
    street_address: '123 Test St',
    city: 'Test City',
    state_province: 'Test State',
    zip_postal_code: '12345',
  };

  // Setup router for testing
  const setupRouter = () => {
    const routes = [
      {
        path: '/',
        element: <Registration />,
        action: action,
      },
    ];

    const router = createMemoryRouter(routes, {
      initialEntries: ['/'],
    });

    return router;
  };

  beforeEach(() => {
    // Reset fetch mock
    global.fetch = vi.fn().mockImplementation((url) => {
      if (url.includes('/api/auth/create/user/')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ id: 1, ...fakeUserData }),
        });
      }
      if (url.includes('/api/auth/create/company/')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ id: 1, ...fakeCompanyData }),
        });
      }
      return Promise.reject(new Error('Not found'));
    });
  });

  it('should render the registration form', () => {
    render(<RouterProvider router={setupRouter()} />);
    
    // Check if form elements are rendered
    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/company name/i)).toBeInTheDocument();
  });

  it('should submit the form with fake data', async () => {
    render(<RouterProvider router={setupRouter()} />);
    
    // Fill in personal information
    fireEvent.change(screen.getByLabelText(/first name/i), {
      target: { value: fakeUserData.first_name },
    });
    fireEvent.change(screen.getByLabelText(/last name/i), {
      target: { value: fakeUserData.last_name },
    });
    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: fakeUserData.email },
    });
    
    // Fill in company information
    fireEvent.change(screen.getByLabelText(/company name/i), {
      target: { value: fakeCompanyData.legalName },
    });
    fireEvent.change(screen.getByLabelText(/street address/i), {
      target: { value: fakeCompanyData.street_address },
    });
    fireEvent.change(screen.getByLabelText(/city/i), {
      target: { value: fakeCompanyData.city },
    });
    fireEvent.change(screen.getByLabelText(/state \/ province/i), {
      target: { value: fakeCompanyData.state_province },
    });
    fireEvent.change(screen.getByLabelText(/zip \/ postal code/i), {
      target: { value: fakeCompanyData.zip_postal_code },
    });
    
    // Submit the form
    fireEvent.click(screen.getByText('Save'));
    
    // Wait for API calls to be made
    await waitFor(() => {
      // Verify that fetch was called with the correct data
      expect(global.fetch).toHaveBeenCalledTimes(2);
      
      // Check user creation API call
      expect(global.fetch).toHaveBeenCalledWith(
        'http://test-api.example.com/api/auth/create/user/',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
          body: expect.stringContaining(fakeUserData.email),
        })
      );
      
      // Check company creation API call
      expect(global.fetch).toHaveBeenCalledWith(
        'http://test-api.example.com/api/auth/create/company/',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
          body: expect.stringContaining(fakeCompanyData.legalName),
        })
      );
    });
  });
});
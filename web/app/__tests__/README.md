# Testing with Vitest

This directory contains tests for the RentCrew web application using Vitest and React Testing Library.

## Setup

The testing environment is configured with:

- **Vitest**: Test runner compatible with Vite
- **React Testing Library**: For rendering and testing React components
- **JSDOM**: Browser environment simulation
- **Jest-DOM**: Additional DOM matchers for better assertions

## Test Files

- `registration.test.tsx`: Tests for the registration form component

## Running Tests

To run the tests, you need to install the dependencies first:

```bash
npm install
```

Then you can run the tests using one of the following commands:

```bash
# Run tests once
npm test

# Run tests in watch mode (useful during development)
npm run test:watch
```

## Writing Tests

When writing tests for form components:

1. Mock any external dependencies (API calls, environment variables, etc.)
2. Render the component with the necessary context (Router, etc.)
3. Interact with the form using Testing Library's utilities
4. Assert that the component behaves as expected

Example:

```tsx
it('should submit the form with fake data', async () => {
  render(<RouterProvider router={setupRouter()} />);
  
  // Fill in form fields
  fireEvent.change(screen.getByLabelText(/email/i), {
    target: { value: 'test@example.com' },
  });
  
  // Submit the form
  fireEvent.click(screen.getByText('Save'));
  
  // Verify API calls
  await waitFor(() => {
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/auth/create/user/'),
      expect.objectContaining({
        method: 'POST',
        body: expect.stringContaining('test@example.com'),
      })
    );
  });
});
```
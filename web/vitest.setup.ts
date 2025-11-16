import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock fetch globally
global.fetch = vi.fn();

// Mock environment variables
vi.mock('node:process', () => ({
  env: {
    API_URL: 'http://test-api.example.com',
  },
}));

// Reset mocks before each test
beforeEach(() => {
  vi.resetAllMocks();
});
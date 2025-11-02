/**
 * Frontend configuration
 * Centralized config for API endpoints and environment variables
 */

export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
} as const;

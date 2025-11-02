/**
 * Frontend configuration
 * Centralized config for API endpoints and environment variables
 */

export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://52.73.252.35',
} as const;

/**
 * Frontend configuration
 * Centralized config for API endpoints and environment variables
 */

export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://api.quotenow-app.com:',
} as const;

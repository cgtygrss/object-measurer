/**
 * API Configuration
 */

// Change this to your backend URL
// For development with Expo Go on physical device, use your machine's local IP
// For emulator: Android = 10.0.2.2, iOS Simulator = localhost
const DEV_API_URL = 'http://localhost:8000';
const PROD_API_URL = 'https://api.objectmeasurer.com'; // Replace with your production URL

export const API_BASE_URL = __DEV__ ? DEV_API_URL : PROD_API_URL;

export const API_ENDPOINTS = {
  measure: '/api/measure/',
  history: '/api/history/',
  export: '/api/export/',
  health: '/health',
} as const;

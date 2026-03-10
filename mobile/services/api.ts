/**
 * API client for communicating with the FastAPI backend.
 */

import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

// In development, point to your local machine
// In production, this will be your deployed API URL
const API_BASE_URL = __DEV__
    ? 'http://192.168.1.100:8000/api/v1'  // Update with your local IP
    : 'https://your-api.example.com/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30s timeout for image uploads
    headers: {
        'Content-Type': 'application/json',
    },
});

// ─── Interceptors ────────────────────────────────────────────

// Attach auth token to every request
api.interceptors.request.use(async (config) => {
    const token = await SecureStore.getItemAsync('auth_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle 401 (expired token)
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            await SecureStore.deleteItemAsync('auth_token');
            // The auth store will handle navigation to login
        }
        return Promise.reject(error);
    }
);

// ─── Auth API ─────────────────────────────────────────────────

export const authAPI = {
    register: (email: string, password: string, displayName?: string) =>
        api.post('/auth/register', { email, password, display_name: displayName }),

    login: (email: string, password: string) =>
        api.post('/auth/login', { email, password }),

    getProfile: () => api.get('/auth/me'),

    updateProfile: (data: { display_name?: string; unit_preference?: string }) =>
        api.patch('/auth/me', data),
};

// ─── Measurement API ──────────────────────────────────────────

export const measurementAPI = {
    upload: (imageUri: string, referenceHeightMm: number, sessionId?: string) => {
        const formData = new FormData();
        formData.append('image', {
            uri: imageUri,
            type: 'image/jpeg',
            name: 'measurement.jpg',
        } as any);
        formData.append('reference_height_mm', referenceHeightMm.toString());
        if (sessionId) {
            formData.append('session_id', sessionId);
        }

        return api.post('/measure/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },

    getHistory: (page = 1, pageSize = 20) =>
        api.get('/measure/history', { params: { page, page_size: pageSize } }),

    getById: (id: string) => api.get(`/measure/${id}`),

    delete: (id: string) => api.delete(`/measure/${id}`),

    createSession: (data: {
        reference_object: string;
        reference_width_mm: number;
        reference_height_mm: number;
    }) => api.post('/measure/sessions', data),
};

export default api;

/**
 * Global state management with Zustand.
 * Handles auth state, measurement state, and settings.
 */

import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';

// ─── Types ────────────────────────────────────────────────────

export interface User {
    id: string;
    email: string;
    display_name: string | null;
    unit_preference: 'cm' | 'mm' | 'in';
    is_premium: boolean;
    created_at: string;
}

export interface MeasurementItem {
    id: string;
    session_id: string | null;
    original_image_url: string | null;
    annotated_image_url: string | null;
    width_mm: number | null;
    height_mm: number | null;
    area_mm2: number | null;
    unit: string;
    mode: string;
    metadata_json: Record<string, any> | null;
    created_at: string;
}

export interface CalibrationData {
    referenceObject: string;
    referenceWidthMm: number;
    referenceHeightMm: number;
    pixelRatio: number | null;
    sessionId: string | null;
}

// ─── Store ────────────────────────────────────────────────────

interface AppState {
    // Auth
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;

    // Calibration
    calibration: CalibrationData | null;

    // Measurements
    measurements: MeasurementItem[];
    totalMeasurements: number;

    // Settings
    unit: 'cm' | 'mm' | 'in';

    // Actions
    setUser: (user: User, token: string) => void;
    logout: () => void;
    setCalibration: (calibration: CalibrationData) => void;
    clearCalibration: () => void;
    setMeasurements: (measurements: MeasurementItem[], total: number) => void;
    addMeasurement: (measurement: MeasurementItem) => void;
    removeMeasurement: (id: string) => void;
    setUnit: (unit: 'cm' | 'mm' | 'in') => void;
    setLoading: (loading: boolean) => void;
    loadToken: () => Promise<void>;
}

export const useAppStore = create<AppState>((set, get) => ({
    // Initial state
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
    calibration: null,
    measurements: [],
    totalMeasurements: 0,
    unit: 'cm',

    // Auth actions
    setUser: async (user, token) => {
        await SecureStore.setItemAsync('auth_token', token);
        set({ user, token, isAuthenticated: true });
    },

    logout: async () => {
        await SecureStore.deleteItemAsync('auth_token');
        set({
            user: null,
            token: null,
            isAuthenticated: false,
            calibration: null,
            measurements: [],
        });
    },

    // Calibration actions
    setCalibration: (calibration) => set({ calibration }),
    clearCalibration: () => set({ calibration: null }),

    // Measurement actions
    setMeasurements: (measurements, total) =>
        set({ measurements, totalMeasurements: total }),

    addMeasurement: (measurement) =>
        set((state) => ({
            measurements: [measurement, ...state.measurements],
            totalMeasurements: state.totalMeasurements + 1,
        })),

    removeMeasurement: (id) =>
        set((state) => ({
            measurements: state.measurements.filter((m) => m.id !== id),
            totalMeasurements: state.totalMeasurements - 1,
        })),

    // Settings
    setUnit: (unit) => set({ unit }),
    setLoading: (isLoading) => set({ isLoading }),

    // Load persisted token on app start
    loadToken: async () => {
        try {
            const token = await SecureStore.getItemAsync('auth_token');
            if (token) {
                set({ token, isAuthenticated: true, isLoading: false });
            } else {
                set({ isLoading: false });
            }
        } catch {
            set({ isLoading: false });
        }
    },
}));

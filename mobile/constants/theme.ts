/**
 * Design tokens — colors, spacing, typography.
 * Dark-first, premium aesthetic.
 */

export const Colors = {
    // Primary brand
    primary: '#6C63FF',
    primaryLight: '#8B85FF',
    primaryDark: '#4A42E0',

    // Accent for measurements
    accent: '#00D9FF',
    accentGlow: 'rgba(0, 217, 255, 0.3)',

    // Success / Error / Warning
    success: '#4ADE80',
    error: '#FF6B6B',
    warning: '#FFB800',

    // Dark theme
    background: '#0A0A0F',
    surface: '#14141F',
    surfaceLight: '#1E1E2E',
    surfaceElevated: '#252536',

    // Text
    textPrimary: '#FFFFFF',
    textSecondary: '#A0A0B8',
    textMuted: '#6B6B80',

    // Borders
    border: '#2A2A3D',
    borderLight: '#363650',

    // Overlays
    overlayDark: 'rgba(0, 0, 0, 0.7)',
    overlayLight: 'rgba(255, 255, 255, 0.05)',

    // Camera
    crosshair: '#00D9FF',
    measureLine: '#FF6B6B',
    measureText: '#FFFFFF',
};

export const Spacing = {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
};

export const BorderRadius = {
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    full: 999,
};

export const FontSize = {
    xs: 10,
    sm: 12,
    md: 14,
    lg: 16,
    xl: 20,
    xxl: 28,
    hero: 36,
};

export const Shadows = {
    sm: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 4,
        elevation: 3,
    },
    md: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 6,
    },
    glow: {
        shadowColor: Colors.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.4,
        shadowRadius: 12,
        elevation: 8,
    },
};

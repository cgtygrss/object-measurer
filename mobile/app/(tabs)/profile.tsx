/**
 * Profile Tab — User settings, calibration, unit preferences, and auth.
 */

import React, { useState } from 'react';
import {
    StyleSheet,
    View,
    Text,
    TouchableOpacity,
    TextInput,
    Alert,
    ScrollView,
    KeyboardAvoidingView,
    Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { Colors, Spacing, BorderRadius, FontSize, Shadows } from '../../constants/theme';
import { useAppStore, CalibrationData } from '../../store';
import { authAPI } from '../../services/api';
import { UnitType } from '../../utils/units';

// Reference object presets (width × height in mm)
const REFERENCE_PRESETS = [
    { label: 'Credit Card', object: 'credit_card', width: 85.6, height: 53.98 },
    { label: 'US Dollar Bill', object: 'dollar', width: 156.1, height: 66.3 },
    { label: 'A4 Paper', object: 'a4', width: 210, height: 297 },
    { label: 'iPhone 15', object: 'iphone15', width: 71.6, height: 147.6 },
];

export default function ProfileScreen() {
    const {
        user,
        isAuthenticated,
        calibration,
        unit,
        setUser,
        logout,
        setCalibration,
        setUnit,
    } = useAppStore();

    // Auth form state
    const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [displayName, setDisplayName] = useState('');
    const [authLoading, setAuthLoading] = useState(false);

    // Custom calibration state
    const [customWidth, setCustomWidth] = useState('');
    const [customHeight, setCustomHeight] = useState('');

    const handleAuth = async () => {
        if (!email || !password) {
            Alert.alert('Error', 'Please fill in all fields');
            return;
        }

        setAuthLoading(true);
        try {
            let response;
            if (authMode === 'register') {
                response = await authAPI.register(email, password, displayName || undefined);
            } else {
                response = await authAPI.login(email, password);
            }

            const { user: userData, access_token } = response.data;
            await setUser(userData, access_token);
            await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || 'Authentication failed');
        } finally {
            setAuthLoading(false);
        }
    };

    const handleCalibrationPreset = (preset: typeof REFERENCE_PRESETS[0]) => {
        setCalibration({
            referenceObject: preset.object,
            referenceWidthMm: preset.width,
            referenceHeightMm: preset.height,
            pixelRatio: null,
            sessionId: null,
        });
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        Alert.alert('Calibrated ✓', `Reference set to ${preset.label} (${preset.width}×${preset.height} mm)`);
    };

    const handleCustomCalibration = () => {
        const w = parseFloat(customWidth);
        const h = parseFloat(customHeight);
        if (isNaN(w) || isNaN(h) || w <= 0 || h <= 0) {
            Alert.alert('Error', 'Please enter valid dimensions');
            return;
        }
        setCalibration({
            referenceObject: 'custom',
            referenceWidthMm: w,
            referenceHeightMm: h,
            pixelRatio: null,
            sessionId: null,
        });
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        Alert.alert('Calibrated ✓', `Reference set to custom (${w}×${h} mm)`);
    };

    // ─── Render ──────────────────────────────────────────────────

    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        >
            <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
                <Text style={styles.pageTitle}>Settings</Text>

                {/* ── Auth Section ────────────────────────────────── */}
                {!isAuthenticated ? (
                    <View style={styles.section}>
                        <Text style={styles.sectionTitle}>
                            {authMode === 'login' ? 'Sign In' : 'Create Account'}
                        </Text>

                        {authMode === 'register' && (
                            <TextInput
                                style={styles.input}
                                placeholder="Display Name"
                                placeholderTextColor={Colors.textMuted}
                                value={displayName}
                                onChangeText={setDisplayName}
                                autoCapitalize="words"
                            />
                        )}
                        <TextInput
                            style={styles.input}
                            placeholder="Email"
                            placeholderTextColor={Colors.textMuted}
                            value={email}
                            onChangeText={setEmail}
                            keyboardType="email-address"
                            autoCapitalize="none"
                        />
                        <TextInput
                            style={styles.input}
                            placeholder="Password"
                            placeholderTextColor={Colors.textMuted}
                            value={password}
                            onChangeText={setPassword}
                            secureTextEntry
                        />

                        <TouchableOpacity
                            style={[styles.authButton, authLoading && styles.authButtonDisabled]}
                            onPress={handleAuth}
                            disabled={authLoading}
                        >
                            <Text style={styles.authButtonText}>
                                {authLoading ? 'Loading...' : authMode === 'login' ? 'Sign In' : 'Sign Up'}
                            </Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            onPress={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
                        >
                            <Text style={styles.toggleText}>
                                {authMode === 'login' ? "Don't have an account? Sign Up" : 'Already have an account? Sign In'}
                            </Text>
                        </TouchableOpacity>
                    </View>
                ) : (
                    <View style={styles.section}>
                        <View style={styles.profileCard}>
                            <View style={styles.avatar}>
                                <Text style={styles.avatarText}>
                                    {(user?.display_name || user?.email || '?')[0].toUpperCase()}
                                </Text>
                            </View>
                            <View style={styles.profileInfo}>
                                <Text style={styles.profileName}>{user?.display_name || 'User'}</Text>
                                <Text style={styles.profileEmail}>{user?.email}</Text>
                            </View>
                        </View>
                        <TouchableOpacity style={styles.logoutButton} onPress={logout}>
                            <Ionicons name="log-out-outline" size={18} color={Colors.error} />
                            <Text style={styles.logoutText}>Sign Out</Text>
                        </TouchableOpacity>
                    </View>
                )}

                {/* ── Calibration Section ─────────────────────────── */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>📐 Calibration</Text>
                    <Text style={styles.sectionSubtitle}>
                        Choose a reference object that will be in the camera frame to establish scale.
                    </Text>

                    {/* Current calibration */}
                    {calibration && (
                        <View style={styles.calibrationCurrent}>
                            <Ionicons name="checkmark-circle" size={18} color={Colors.success} />
                            <Text style={styles.calibrationText}>
                                {REFERENCE_PRESETS.find(p => p.object === calibration.referenceObject)?.label || 'Custom'} — {calibration.referenceWidthMm}×{calibration.referenceHeightMm} mm
                            </Text>
                        </View>
                    )}

                    {/* Presets */}
                    <View style={styles.presetGrid}>
                        {REFERENCE_PRESETS.map((preset) => (
                            <TouchableOpacity
                                key={preset.object}
                                style={[
                                    styles.presetButton,
                                    calibration?.referenceObject === preset.object && styles.presetButtonActive,
                                ]}
                                onPress={() => handleCalibrationPreset(preset)}
                            >
                                <Text
                                    style={[
                                        styles.presetLabel,
                                        calibration?.referenceObject === preset.object && styles.presetLabelActive,
                                    ]}
                                >
                                    {preset.label}
                                </Text>
                                <Text style={styles.presetDims}>
                                    {preset.width}×{preset.height}mm
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    {/* Custom */}
                    <Text style={styles.customLabel}>Custom Reference</Text>
                    <View style={styles.customRow}>
                        <TextInput
                            style={[styles.input, styles.customInput]}
                            placeholder="Width (mm)"
                            placeholderTextColor={Colors.textMuted}
                            value={customWidth}
                            onChangeText={setCustomWidth}
                            keyboardType="decimal-pad"
                        />
                        <Text style={styles.customX}>×</Text>
                        <TextInput
                            style={[styles.input, styles.customInput]}
                            placeholder="Height (mm)"
                            placeholderTextColor={Colors.textMuted}
                            value={customHeight}
                            onChangeText={setCustomHeight}
                            keyboardType="decimal-pad"
                        />
                        <TouchableOpacity style={styles.customButton} onPress={handleCustomCalibration}>
                            <Ionicons name="checkmark" size={20} color={Colors.textPrimary} />
                        </TouchableOpacity>
                    </View>
                </View>

                {/* ── Unit Preference ─────────────────────────────── */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>📏 Measurement Unit</Text>
                    <View style={styles.unitRow}>
                        {(['mm', 'cm', 'in'] as UnitType[]).map((u) => (
                            <TouchableOpacity
                                key={u}
                                style={[styles.unitButton, unit === u && styles.unitButtonActive]}
                                onPress={() => {
                                    setUnit(u);
                                    Haptics.selectionAsync();
                                }}
                            >
                                <Text style={[styles.unitText, unit === u && styles.unitTextActive]}>
                                    {u === 'in' ? 'Inches' : u.toUpperCase()}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                </View>

                {/* ── App Info ────────────────────────────────────── */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>ℹ️ About</Text>
                    <Text style={styles.aboutText}>
                        Object Measurer v1.0.0{'\n'}
                        Measure real-world objects using your phone camera.{'\n'}
                        Hybrid processing: on-device for speed, server for precision.
                    </Text>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Colors.background,
    },
    scrollContent: {
        paddingTop: 60,
        paddingBottom: 100,
        paddingHorizontal: Spacing.lg,
    },
    pageTitle: {
        fontSize: FontSize.hero,
        fontWeight: '800',
        color: Colors.textPrimary,
        marginBottom: Spacing.lg,
    },
    section: {
        backgroundColor: Colors.surface,
        borderRadius: BorderRadius.lg,
        padding: Spacing.lg,
        marginBottom: Spacing.md,
        borderWidth: 1,
        borderColor: Colors.border,
    },
    sectionTitle: {
        fontSize: FontSize.lg,
        fontWeight: '700',
        color: Colors.textPrimary,
        marginBottom: Spacing.xs,
    },
    sectionSubtitle: {
        fontSize: FontSize.sm,
        color: Colors.textSecondary,
        marginBottom: Spacing.md,
        lineHeight: 18,
    },
    input: {
        backgroundColor: Colors.surfaceLight,
        borderRadius: BorderRadius.md,
        paddingHorizontal: Spacing.md,
        paddingVertical: Spacing.sm + 4,
        fontSize: FontSize.md,
        color: Colors.textPrimary,
        marginBottom: Spacing.sm,
        borderWidth: 1,
        borderColor: Colors.border,
    },
    authButton: {
        backgroundColor: Colors.primary,
        borderRadius: BorderRadius.md,
        paddingVertical: Spacing.md,
        alignItems: 'center',
        marginTop: Spacing.sm,
        ...Shadows.glow,
    },
    authButtonDisabled: {
        opacity: 0.6,
    },
    authButtonText: {
        fontSize: FontSize.lg,
        fontWeight: '700',
        color: Colors.textPrimary,
    },
    toggleText: {
        fontSize: FontSize.sm,
        color: Colors.primary,
        textAlign: 'center',
        marginTop: Spacing.md,
    },
    profileCard: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: Spacing.md,
    },
    avatar: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: Colors.primary,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: Spacing.md,
    },
    avatarText: {
        fontSize: FontSize.xl,
        fontWeight: '700',
        color: Colors.textPrimary,
    },
    profileInfo: {},
    profileName: {
        fontSize: FontSize.lg,
        fontWeight: '700',
        color: Colors.textPrimary,
    },
    profileEmail: {
        fontSize: FontSize.sm,
        color: Colors.textSecondary,
    },
    logoutButton: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        paddingVertical: Spacing.sm,
    },
    logoutText: {
        fontSize: FontSize.md,
        color: Colors.error,
        fontWeight: '600',
    },
    calibrationCurrent: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        backgroundColor: 'rgba(74, 222, 128, 0.1)',
        borderRadius: BorderRadius.md,
        padding: Spacing.sm,
        marginBottom: Spacing.md,
        borderWidth: 1,
        borderColor: 'rgba(74, 222, 128, 0.2)',
    },
    calibrationText: {
        fontSize: FontSize.sm,
        color: Colors.success,
        fontWeight: '500',
    },
    presetGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Spacing.sm,
        marginBottom: Spacing.md,
    },
    presetButton: {
        backgroundColor: Colors.surfaceLight,
        borderRadius: BorderRadius.md,
        paddingHorizontal: Spacing.md,
        paddingVertical: Spacing.sm,
        borderWidth: 1,
        borderColor: Colors.border,
        width: '47%',
    },
    presetButtonActive: {
        borderColor: Colors.primary,
        backgroundColor: 'rgba(108, 99, 255, 0.1)',
    },
    presetLabel: {
        fontSize: FontSize.sm,
        fontWeight: '600',
        color: Colors.textPrimary,
    },
    presetLabelActive: {
        color: Colors.primary,
    },
    presetDims: {
        fontSize: FontSize.xs,
        color: Colors.textMuted,
        marginTop: 2,
    },
    customLabel: {
        fontSize: FontSize.sm,
        fontWeight: '600',
        color: Colors.textSecondary,
        marginBottom: Spacing.xs,
    },
    customRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    customInput: {
        flex: 1,
        marginBottom: 0,
    },
    customX: {
        fontSize: FontSize.lg,
        color: Colors.textMuted,
    },
    customButton: {
        backgroundColor: Colors.primary,
        width: 44,
        height: 44,
        borderRadius: BorderRadius.md,
        justifyContent: 'center',
        alignItems: 'center',
    },
    unitRow: {
        flexDirection: 'row',
        gap: Spacing.sm,
        marginTop: Spacing.sm,
    },
    unitButton: {
        flex: 1,
        backgroundColor: Colors.surfaceLight,
        borderRadius: BorderRadius.md,
        paddingVertical: Spacing.sm + 4,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: Colors.border,
    },
    unitButtonActive: {
        backgroundColor: Colors.primary,
        borderColor: Colors.primary,
    },
    unitText: {
        fontSize: FontSize.md,
        fontWeight: '600',
        color: Colors.textSecondary,
    },
    unitTextActive: {
        color: Colors.textPrimary,
    },
    aboutText: {
        fontSize: FontSize.sm,
        color: Colors.textSecondary,
        lineHeight: 20,
        marginTop: Spacing.sm,
    },
});

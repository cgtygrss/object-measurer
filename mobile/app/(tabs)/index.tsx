/**
 * Camera Tab — Main measurement screen.
 *
 * Two modes:
 *   🔴 REAL-TIME: Live camera feed with on-device edge detection
 *   📷 PHOTO:     Capture photo → send to server for precise measurement
 */

import React, { useState, useCallback, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { Colors, Spacing, BorderRadius, FontSize, Shadows } from '../../constants/theme';
import { measurementAPI } from '../../services/api';
import { useAppStore } from '../../store';
import { formatMeasurement, UnitType } from '../../utils/units';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export default function CameraScreen() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const device = useCameraDevice('back');
  const cameraRef = useRef<Camera>(null);

  const [mode, setMode] = useState<'realtime' | 'photo'>('photo');
  const [isProcessing, setIsProcessing] = useState(false);
  const [lastResult, setLastResult] = useState<{
    width: number;
    height: number;
    area: number;
  } | null>(null);

  const { calibration, unit, addMeasurement, isAuthenticated } = useAppStore();

  // ─── Permission Handling ─────────────────────────────────────

  if (!hasPermission) {
    return (
      <View style={styles.container}>
        <View style={styles.permissionBox}>
          <Ionicons name="camera-outline" size={64} color={Colors.textSecondary} />
          <Text style={styles.permissionTitle}>Camera Access Required</Text>
          <Text style={styles.permissionText}>
            We need camera access to measure objects in real-time.
          </Text>
          <TouchableOpacity style={styles.primaryButton} onPress={requestPermission}>
            <Text style={styles.primaryButtonText}>Grant Permission</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  if (!device) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>No camera device found</Text>
      </View>
    );
  }

  // ─── Photo Capture ───────────────────────────────────────────

  const handleCapture = useCallback(async () => {
    if (!cameraRef.current || isProcessing) return;

    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsProcessing(true);

    try {
      const photo = await cameraRef.current.takePhoto({
        qualityPrioritization: 'quality',
      });

      if (!calibration) {
        Alert.alert(
          'Calibration Required',
          'Please calibrate with a reference object first. Go to Profile → Calibrate.',
          [{ text: 'OK' }]
        );
        setIsProcessing(false);
        return;
      }

      if (!isAuthenticated) {
        Alert.alert(
          'Login Required',
          'Please log in to use server-side measurement.',
          [{ text: 'OK' }]
        );
        setIsProcessing(false);
        return;
      }

      // Upload to server for precise measurement
      const response = await measurementAPI.upload(
        `file://${photo.path}`,
        calibration.referenceHeightMm,
        calibration.sessionId || undefined
      );

      const { measurement, dimensions } = response.data;

      setLastResult({
        width: dimensions.width_mm,
        height: dimensions.height_mm,
        area: dimensions.area_mm2,
      });

      addMeasurement(measurement);
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch (error: any) {
      console.error('Measurement failed:', error);
      Alert.alert('Error', error.response?.data?.detail || 'Measurement failed. Please try again.');
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setIsProcessing(false);
    }
  }, [calibration, isAuthenticated, isProcessing, addMeasurement]);

  // ─── Render ──────────────────────────────────────────────────

  return (
    <View style={styles.container}>
      {/* Camera Preview */}
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true}
      />

      {/* Crosshair Overlay */}
      <View style={styles.crosshairContainer} pointerEvents="none">
        <View style={[styles.crosshairLine, styles.crosshairH]} />
        <View style={[styles.crosshairLine, styles.crosshairV]} />
        <View style={styles.crosshairCenter} />
      </View>

      {/* Mode Switcher */}
      <View style={styles.modeBar}>
        <TouchableOpacity
          style={[styles.modeButton, mode === 'realtime' && styles.modeButtonActive]}
          onPress={() => setMode('realtime')}
        >
          <Ionicons
            name="videocam"
            size={18}
            color={mode === 'realtime' ? Colors.textPrimary : Colors.textMuted}
          />
          <Text style={[styles.modeText, mode === 'realtime' && styles.modeTextActive]}>
            Real-Time
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.modeButton, mode === 'photo' && styles.modeButtonActive]}
          onPress={() => setMode('photo')}
        >
          <Ionicons
            name="camera"
            size={18}
            color={mode === 'photo' ? Colors.textPrimary : Colors.textMuted}
          />
          <Text style={[styles.modeText, mode === 'photo' && styles.modeTextActive]}>
            Photo
          </Text>
        </TouchableOpacity>
      </View>

      {/* Result Card */}
      {lastResult && (
        <View style={styles.resultCard}>
          <Text style={styles.resultLabel}>Measurement Result</Text>
          <View style={styles.resultRow}>
            <View style={styles.resultItem}>
              <Text style={styles.resultValue}>
                {formatMeasurement(lastResult.width, unit as UnitType)}
              </Text>
              <Text style={styles.resultDimLabel}>Width</Text>
            </View>
            <View style={styles.resultDivider} />
            <View style={styles.resultItem}>
              <Text style={styles.resultValue}>
                {formatMeasurement(lastResult.height, unit as UnitType)}
              </Text>
              <Text style={styles.resultDimLabel}>Height</Text>
            </View>
            <View style={styles.resultDivider} />
            <View style={styles.resultItem}>
              <Text style={styles.resultValue}>
                {formatMeasurement(lastResult.area, unit as UnitType)}²
              </Text>
              <Text style={styles.resultDimLabel}>Area</Text>
            </View>
          </View>
        </View>
      )}

      {/* Capture Button */}
      {mode === 'photo' && (
        <View style={styles.captureBar}>
          <TouchableOpacity
            style={[styles.captureButton, isProcessing && styles.captureButtonDisabled]}
            onPress={handleCapture}
            disabled={isProcessing}
            activeOpacity={0.7}
          >
            {isProcessing ? (
              <ActivityIndicator color={Colors.textPrimary} size="large" />
            ) : (
              <View style={styles.captureButtonInner} />
            )}
          </TouchableOpacity>
        </View>
      )}

      {/* Real-time Mode Indicator */}
      {mode === 'realtime' && (
        <View style={styles.realtimeIndicator}>
          <View style={styles.realtimeDot} />
          <Text style={styles.realtimeText}>On-Device Processing</Text>
        </View>
      )}

      {/* Calibration Warning */}
      {!calibration && (
        <View style={styles.warningBanner}>
          <Ionicons name="warning" size={16} color={Colors.warning} />
          <Text style={styles.warningText}>
            No calibration set. Tap Profile → Calibrate first.
          </Text>
        </View>
      )}
    </View>
  );
}

// ─── Styles ────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  permissionBox: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xl,
  },
  permissionTitle: {
    fontSize: FontSize.xl,
    fontWeight: '700',
    color: Colors.textPrimary,
    marginTop: Spacing.lg,
    marginBottom: Spacing.sm,
  },
  permissionText: {
    fontSize: FontSize.md,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginBottom: Spacing.lg,
  },
  primaryButton: {
    backgroundColor: Colors.primary,
    paddingHorizontal: Spacing.xl,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.lg,
    ...Shadows.glow,
  },
  primaryButtonText: {
    fontSize: FontSize.lg,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
  errorText: {
    fontSize: FontSize.lg,
    color: Colors.error,
    textAlign: 'center',
    marginTop: 100,
  },

  // Crosshair
  crosshairContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  crosshairLine: {
    position: 'absolute',
    backgroundColor: Colors.crosshair,
    opacity: 0.4,
  },
  crosshairH: {
    width: 60,
    height: 1,
  },
  crosshairV: {
    width: 1,
    height: 60,
  },
  crosshairCenter: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.crosshair,
    opacity: 0.8,
  },

  // Mode switcher
  modeBar: {
    position: 'absolute',
    top: 60,
    alignSelf: 'center',
    flexDirection: 'row',
    backgroundColor: Colors.overlayDark,
    borderRadius: BorderRadius.full,
    padding: 4,
  },
  modeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.full,
    gap: 6,
  },
  modeButtonActive: {
    backgroundColor: Colors.primary,
  },
  modeText: {
    fontSize: FontSize.sm,
    color: Colors.textMuted,
    fontWeight: '600',
  },
  modeTextActive: {
    color: Colors.textPrimary,
  },

  // Result card
  resultCard: {
    position: 'absolute',
    top: 120,
    left: Spacing.md,
    right: Spacing.md,
    backgroundColor: Colors.overlayDark,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    borderWidth: 1,
    borderColor: Colors.accent,
  },
  resultLabel: {
    fontSize: FontSize.xs,
    color: Colors.accent,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: Spacing.sm,
    textAlign: 'center',
  },
  resultRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  resultItem: {
    alignItems: 'center',
    flex: 1,
  },
  resultValue: {
    fontSize: FontSize.xl,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  resultDimLabel: {
    fontSize: FontSize.xs,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  resultDivider: {
    width: 1,
    height: 30,
    backgroundColor: Colors.border,
  },

  // Capture button
  captureBar: {
    position: 'absolute',
    bottom: 100,
    alignSelf: 'center',
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 4,
    borderColor: Colors.textPrimary,
  },
  captureButtonDisabled: {
    opacity: 0.5,
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: Colors.textPrimary,
  },

  // Real-time indicator
  realtimeIndicator: {
    position: 'absolute',
    bottom: 120,
    alignSelf: 'center',
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.overlayDark,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.full,
    gap: 8,
  },
  realtimeDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.success,
  },
  realtimeText: {
    fontSize: FontSize.sm,
    color: Colors.textSecondary,
    fontWeight: '500',
  },

  // Warning banner
  warningBanner: {
    position: 'absolute',
    bottom: 40,
    left: Spacing.md,
    right: Spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 184, 0, 0.15)',
    borderRadius: BorderRadius.md,
    padding: Spacing.sm,
    gap: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 184, 0, 0.3)',
  },
  warningText: {
    fontSize: FontSize.sm,
    color: Colors.warning,
    flex: 1,
  },
});

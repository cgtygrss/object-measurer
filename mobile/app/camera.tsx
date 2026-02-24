import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { useRouter } from 'expo-router';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { Colors, Spacing, FontSize, BorderRadius } from '../src/theme';
import Button from '../src/components/ui/Button';

const { width, height } = Dimensions.get('window');

export default function CameraScreen() {
  const router = useRouter();
  const cameraRef = useRef<CameraView>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<'front' | 'back'>('back');
  const [flash, setFlash] = useState<'off' | 'on'>('off');
  const [capturing, setCapturing] = useState(false);

  if (!permission) {
    return <View style={styles.container} />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.permissionContainer}>
        <Ionicons name="camera-outline" size={64} color={Colors.textMuted} />
        <Text style={styles.permissionTitle}>Camera Access Required</Text>
        <Text style={styles.permissionDesc}>
          We need camera access to photograph objects for measurement.
        </Text>
        <Button title="Grant Permission" onPress={requestPermission} />
        <Button
          title="Go Back"
          onPress={() => router.back()}
          variant="ghost"
          style={{ marginTop: Spacing.sm }}
        />
      </View>
    );
  }

  const takePicture = async () => {
    if (!cameraRef.current || capturing) return;

    setCapturing(true);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

    try {
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.9,
      });

      if (photo) {
        router.replace({
          pathname: '/measure',
          params: { imageUri: photo.uri },
        });
      }
    } catch (err) {
      console.error('Failed to take picture:', err);
    } finally {
      setCapturing(false);
    }
  };

  const toggleFacing = () => {
    setFacing((prev) => (prev === 'back' ? 'front' : 'back'));
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const toggleFlash = () => {
    setFlash((prev) => (prev === 'off' ? 'on' : 'off'));
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  return (
    <View style={styles.container}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing={facing}
        flash={flash}
      >
        {/* Grid overlay for alignment */}
        <View style={styles.gridOverlay}>
          <View style={styles.gridRow}>
            <View style={styles.gridCell} />
            <View style={[styles.gridCell, styles.gridBorderLeft]} />
            <View style={[styles.gridCell, styles.gridBorderLeft]} />
          </View>
          <View style={[styles.gridRow, styles.gridBorderTop]}>
            <View style={styles.gridCell} />
            <View style={[styles.gridCell, styles.gridBorderLeft]} />
            <View style={[styles.gridCell, styles.gridBorderLeft]} />
          </View>
          <View style={[styles.gridRow, styles.gridBorderTop]}>
            <View style={styles.gridCell} />
            <View style={[styles.gridCell, styles.gridBorderLeft]} />
            <View style={[styles.gridCell, styles.gridBorderLeft]} />
          </View>
        </View>

        {/* Top bar */}
        <View style={styles.topBar}>
          <TouchableOpacity
            onPress={() => router.back()}
            style={styles.topButton}
          >
            <Ionicons name="close" size={28} color={Colors.white} />
          </TouchableOpacity>
          <TouchableOpacity onPress={toggleFlash} style={styles.topButton}>
            <Ionicons
              name={flash === 'on' ? 'flash' : 'flash-off'}
              size={24}
              color={Colors.white}
            />
          </TouchableOpacity>
        </View>

        {/* Center crosshair */}
        <View style={styles.crosshair}>
          <View style={styles.crosshairH} />
          <View style={styles.crosshairV} />
        </View>

        {/* Bottom controls */}
        <View style={styles.bottomBar}>
          <View style={styles.controlsRow}>
            <View style={{ width: 50 }} />
            <TouchableOpacity
              onPress={takePicture}
              disabled={capturing}
              style={styles.captureButton}
            >
              <View
                style={[
                  styles.captureInner,
                  capturing && { backgroundColor: Colors.textMuted },
                ]}
              />
            </TouchableOpacity>
            <TouchableOpacity onPress={toggleFacing} style={styles.flipButton}>
              <Ionicons
                name="camera-reverse"
                size={28}
                color={Colors.white}
              />
            </TouchableOpacity>
          </View>
          <Text style={styles.hint}>
            Position the object in the center for best results
          </Text>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.black,
  },
  camera: {
    flex: 1,
  },
  permissionContainer: {
    flex: 1,
    backgroundColor: Colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    padding: Spacing.xl,
    gap: Spacing.md,
  },
  permissionTitle: {
    color: Colors.text,
    fontSize: FontSize.xl,
    fontWeight: '700',
  },
  permissionDesc: {
    color: Colors.textSecondary,
    fontSize: FontSize.md,
    textAlign: 'center',
    marginBottom: Spacing.md,
  },
  topBar: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.lg,
  },
  topButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(0,0,0,0.4)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  gridOverlay: {
    ...StyleSheet.absoluteFillObject,
    opacity: 0.3,
  },
  gridRow: {
    flex: 1,
    flexDirection: 'row',
  },
  gridCell: {
    flex: 1,
  },
  gridBorderLeft: {
    borderLeftWidth: 1,
    borderLeftColor: Colors.white,
  },
  gridBorderTop: {
    borderTopWidth: 1,
    borderTopColor: Colors.white,
  },
  crosshair: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -15,
    marginLeft: -15,
    width: 30,
    height: 30,
    alignItems: 'center',
    justifyContent: 'center',
  },
  crosshairH: {
    position: 'absolute',
    width: 30,
    height: 1,
    backgroundColor: 'rgba(255,255,255,0.8)',
  },
  crosshairV: {
    position: 'absolute',
    width: 1,
    height: 30,
    backgroundColor: 'rgba(255,255,255,0.8)',
  },
  bottomBar: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    paddingBottom: 50,
    paddingTop: Spacing.lg,
    backgroundColor: 'rgba(0,0,0,0.3)',
    alignItems: 'center',
  },
  controlsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: 220,
  },
  captureButton: {
    width: 72,
    height: 72,
    borderRadius: 36,
    borderWidth: 4,
    borderColor: Colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  captureInner: {
    width: 58,
    height: 58,
    borderRadius: 29,
    backgroundColor: Colors.white,
  },
  flipButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  hint: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: FontSize.xs,
    marginTop: Spacing.md,
  },
});

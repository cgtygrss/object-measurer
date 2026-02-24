import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  ScrollView,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import {
  Colors,
  Spacing,
  FontSize,
  BorderRadius,
  Shadow,
} from '../../src/theme';
import Button from '../../src/components/ui/Button';

export default function ScanScreen() {
  const router = useRouter();
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(
        'Permission Required',
        'Camera access is needed to take photos for measurement.'
      );
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ['images'],
      quality: 0.9,
      allowsEditing: true,
    });

    if (!result.canceled && result.assets[0]) {
      setSelectedImage(result.assets[0].uri);
    }
  };

  const pickFromGallery = async () => {
    const { status } =
      await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(
        'Permission Required',
        'Photo library access is needed to import images.'
      );
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      quality: 0.9,
      allowsEditing: true,
    });

    if (!result.canceled && result.assets[0]) {
      setSelectedImage(result.assets[0].uri);
    }
  };

  const proceedToMeasure = () => {
    if (!selectedImage) return;
    router.push({
      pathname: '/measure',
      params: { imageUri: selectedImage },
    });
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.heading}>Capture or Select Image</Text>
      <Text style={styles.subheading}>
        Take a photo of the object you want to measure, or import from your
        gallery.
      </Text>

      {/* Image Preview */}
      <View style={styles.previewContainer}>
        {selectedImage ? (
          <Image source={{ uri: selectedImage }} style={styles.preview} />
        ) : (
          <View style={styles.placeholderPreview}>
            <Ionicons name="image-outline" size={64} color={Colors.textMuted} />
            <Text style={styles.placeholderText}>No image selected</Text>
          </View>
        )}
      </View>

      {/* Action Buttons */}
      <View style={styles.buttonGroup}>
        <Button
          title="Take Photo"
          onPress={takePhoto}
          variant="primary"
          size="lg"
          icon={<Ionicons name="camera" size={20} color={Colors.white} />}
          style={styles.button}
        />
        <Button
          title="Choose from Gallery"
          onPress={pickFromGallery}
          variant="secondary"
          size="lg"
          icon={
            <Ionicons name="images" size={20} color={Colors.text} />
          }
          style={styles.button}
        />
      </View>

      {/* Continue */}
      {selectedImage && (
        <View style={styles.continueSection}>
          <Button
            title="Continue to Measure"
            onPress={proceedToMeasure}
            variant="primary"
            size="lg"
            icon={
              <Ionicons name="arrow-forward" size={20} color={Colors.white} />
            }
            style={styles.continueButton}
          />
          <Button
            title="Clear"
            onPress={() => setSelectedImage(null)}
            variant="ghost"
            size="sm"
          />
        </View>
      )}

      {/* Tips */}
      <View style={styles.tipsSection}>
        <Text style={styles.tipsTitle}>Tips for best results</Text>
        {[
          'Place the object on a plain, contrasting background',
          'Ensure even lighting without harsh shadows',
          'Include a reference object with a known size',
          'Keep the camera parallel to the object surface',
        ].map((tip, idx) => (
          <View key={idx} style={styles.tipRow}>
            <Ionicons
              name="checkmark-circle"
              size={16}
              color={Colors.success}
            />
            <Text style={styles.tipText}>{tip}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    padding: Spacing.lg,
    paddingBottom: Spacing.xxl,
  },
  heading: {
    fontSize: FontSize.xl,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: Spacing.xs,
  },
  subheading: {
    fontSize: FontSize.sm,
    color: Colors.textSecondary,
    marginBottom: Spacing.lg,
    lineHeight: 20,
  },
  previewContainer: {
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    marginBottom: Spacing.lg,
    ...Shadow.md,
  },
  preview: {
    width: '100%',
    height: 300,
    borderRadius: BorderRadius.lg,
  },
  placeholderPreview: {
    width: '100%',
    height: 300,
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    borderStyle: 'dashed',
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeholderText: {
    color: Colors.textMuted,
    fontSize: FontSize.md,
    marginTop: Spacing.sm,
  },
  buttonGroup: {
    gap: Spacing.md,
    marginBottom: Spacing.lg,
  },
  button: {
    width: '100%',
  },
  continueSection: {
    alignItems: 'center',
    gap: Spacing.sm,
    marginBottom: Spacing.lg,
  },
  continueButton: {
    width: '100%',
    backgroundColor: Colors.success,
  },
  tipsSection: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    gap: Spacing.sm,
  },
  tipsTitle: {
    color: Colors.text,
    fontSize: FontSize.sm,
    fontWeight: '600',
    marginBottom: Spacing.xs,
  },
  tipRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
  },
  tipText: {
    color: Colors.textSecondary,
    fontSize: FontSize.sm,
    flex: 1,
  },
});

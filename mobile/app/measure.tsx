import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  Image,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import {
  Colors,
  Spacing,
  FontSize,
  BorderRadius,
  Shadow,
} from '../src/theme';
import Button from '../src/components/ui/Button';
import InputField from '../src/components/ui/InputField';
import UnitPicker from '../src/components/ui/UnitPicker';
import { createMeasurement } from '../src/api/client';

export default function MeasureScreen() {
  const router = useRouter();
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>();

  const [title, setTitle] = useState('');
  const [referenceHeight, setReferenceHeight] = useState('');
  const [unit, setUnit] = useState('cm');
  const [interval, setInterval] = useState('20');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  useEffect(() => {
    loadDefaults();
  }, []);

  const loadDefaults = async () => {
    try {
      const savedUnit = await AsyncStorage.getItem('defaultUnit');
      const savedInterval = await AsyncStorage.getItem('defaultInterval');
      if (savedUnit) setUnit(savedUnit);
      if (savedInterval) setInterval(savedInterval);
    } catch {}
  };

  const validate = (): boolean => {
    if (!imageUri) {
      Alert.alert('Error', 'No image selected. Please go back and select an image.');
      return false;
    }
    if (!referenceHeight || parseFloat(referenceHeight) <= 0) {
      Alert.alert('Error', 'Please enter a valid reference height greater than 0.');
      return false;
    }
    return true;
  };

  const handleMeasure = async () => {
    if (!validate()) return;

    setLoading(true);
    try {
      const result = await createMeasurement({
        imageUri: imageUri!,
        title: title || 'Untitled',
        referenceHeight: parseFloat(referenceHeight),
        unit,
        interval: parseInt(interval) || 20,
        notes: notes || undefined,
      });

      router.replace(`/result/${result.id}`);
    } catch (err: any) {
      Alert.alert(
        'Measurement Failed',
        err.message || 'Something went wrong. Make sure the server is running and try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.content}>
        {/* Image Preview */}
        {imageUri && (
          <View style={styles.imageContainer}>
            <Image source={{ uri: imageUri }} style={styles.image} />
            <View style={styles.imageBadge}>
              <Ionicons name="image" size={14} color={Colors.white} />
              <Text style={styles.imageBadgeText}>Selected Image</Text>
            </View>
          </View>
        )}

        {/* Form */}
        <View style={styles.form}>
          <InputField
            label="Title (optional)"
            value={title}
            onChangeText={setTitle}
            placeholder="e.g., Kitchen Table"
          />

          <InputField
            label="Reference Height *"
            value={referenceHeight}
            onChangeText={setReferenceHeight}
            placeholder="Enter known height of the object"
            keyboardType="decimal-pad"
            suffix={unit}
            error={
              referenceHeight && parseFloat(referenceHeight) <= 0
                ? 'Must be greater than 0'
                : undefined
            }
          />

          <UnitPicker value={unit} onChange={setUnit} />

          {/* Advanced Settings Toggle */}
          <Button
            title={showAdvanced ? 'Hide Advanced' : 'Advanced Settings'}
            onPress={() => setShowAdvanced(!showAdvanced)}
            variant="ghost"
            size="sm"
            icon={
              <Ionicons
                name={showAdvanced ? 'chevron-up' : 'chevron-down'}
                size={16}
                color={Colors.primary}
              />
            }
          />

          {showAdvanced && (
            <View style={styles.advancedSection}>
              <InputField
                label="Grid Interval (pixels)"
                value={interval}
                onChangeText={setInterval}
                placeholder="20"
                keyboardType="numeric"
              />
              <InputField
                label="Notes"
                value={notes}
                onChangeText={setNotes}
                placeholder="Optional notes about this measurement..."
                multiline
              />
            </View>
          )}
        </View>

        {/* Info Card */}
        <View style={styles.infoCard}>
          <Ionicons name="information-circle" size={20} color={Colors.info} />
          <Text style={styles.infoText}>
            The reference height is used to calibrate pixel-to-real-world
            conversion. For best accuracy, enter the exact height of the object
            or a known reference in the image.
          </Text>
        </View>

        {/* Submit */}
        <Button
          title={loading ? 'Processing...' : 'Measure Object'}
          onPress={handleMeasure}
          size="lg"
          loading={loading}
          disabled={!referenceHeight || loading}
          icon={
            !loading ? (
              <Ionicons name="analytics" size={20} color={Colors.white} />
            ) : undefined
          }
          style={styles.measureButton}
        />
      </ScrollView>
    </KeyboardAvoidingView>
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
  imageContainer: {
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    marginBottom: Spacing.lg,
    ...Shadow.md,
  },
  image: {
    width: '100%',
    height: 220,
    borderRadius: BorderRadius.lg,
  },
  imageBadge: {
    position: 'absolute',
    bottom: Spacing.sm,
    left: Spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.6)',
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: BorderRadius.full,
    gap: 4,
  },
  imageBadgeText: {
    color: Colors.white,
    fontSize: FontSize.xs,
  },
  form: {
    marginBottom: Spacing.md,
  },
  advancedSection: {
    marginTop: Spacing.md,
    paddingTop: Spacing.md,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  infoCard: {
    flexDirection: 'row',
    backgroundColor: Colors.info + '15',
    borderRadius: BorderRadius.sm,
    padding: Spacing.md,
    marginBottom: Spacing.lg,
    gap: Spacing.sm,
  },
  infoText: {
    flex: 1,
    color: Colors.textSecondary,
    fontSize: FontSize.xs,
    lineHeight: 18,
  },
  measureButton: {
    width: '100%',
  },
});

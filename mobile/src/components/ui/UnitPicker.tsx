import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors, BorderRadius, FontSize, Spacing } from '../../theme';

interface UnitPickerProps {
  value: string;
  onChange: (unit: string) => void;
}

const UNITS = [
  { label: 'mm', value: 'mm' },
  { label: 'cm', value: 'cm' },
  { label: 'm', value: 'm' },
  { label: 'in', value: 'in' },
  { label: 'ft', value: 'ft' },
];

export default function UnitPicker({ value, onChange }: UnitPickerProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Unit</Text>
      <View style={styles.row}>
        {UNITS.map((unit) => (
          <TouchableOpacity
            key={unit.value}
            onPress={() => onChange(unit.value)}
            style={[
              styles.chip,
              value === unit.value && styles.chipActive,
            ]}
          >
            <Text
              style={[
                styles.chipText,
                value === unit.value && styles.chipTextActive,
              ]}
            >
              {unit.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: Spacing.md,
  },
  label: {
    color: Colors.textSecondary,
    fontSize: FontSize.sm,
    fontWeight: '500',
    marginBottom: Spacing.sm,
  },
  row: {
    flexDirection: 'row',
    gap: Spacing.sm,
  },
  chip: {
    paddingVertical: Spacing.sm,
    paddingHorizontal: Spacing.md,
    borderRadius: BorderRadius.full,
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  chipActive: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  chipText: {
    color: Colors.textSecondary,
    fontSize: FontSize.sm,
    fontWeight: '600',
  },
  chipTextActive: {
    color: Colors.white,
  },
});

import React from 'react';
import {
  View,
  Image,
  TouchableOpacity,
  Text,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, BorderRadius, Spacing, FontSize, Shadow } from '../theme';
import type { MeasurementSummary } from '../api/client';

interface MeasurementCardProps {
  measurement: MeasurementSummary;
  onPress: () => void;
}

const { width } = Dimensions.get('window');
const CARD_WIDTH = (width - Spacing.lg * 2 - Spacing.md) / 2;

export default function MeasurementCard({
  measurement,
  onPress,
}: MeasurementCardProps) {
  const date = new Date(measurement.created_at);
  const formattedDate = date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <TouchableOpacity
      onPress={onPress}
      activeOpacity={0.8}
      style={styles.card}
    >
      {measurement.result_image_url ? (
        <Image
          source={{ uri: measurement.result_image_url }}
          style={styles.image}
          resizeMode="cover"
        />
      ) : (
        <View style={styles.placeholder}>
          <Ionicons name="cube-outline" size={40} color={Colors.textMuted} />
        </View>
      )}
      <View style={styles.info}>
        <Text style={styles.title} numberOfLines={1}>
          {measurement.title}
        </Text>
        <Text style={styles.meta}>
          {measurement.reference_height} {measurement.unit} · {formattedDate}
        </Text>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    width: CARD_WIDTH,
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.md,
    overflow: 'hidden',
    marginBottom: Spacing.md,
    ...Shadow.sm,
  },
  image: {
    width: '100%',
    height: CARD_WIDTH * 0.75,
    backgroundColor: Colors.surfaceLight,
  },
  placeholder: {
    width: '100%',
    height: CARD_WIDTH * 0.75,
    backgroundColor: Colors.surfaceLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  info: {
    padding: Spacing.sm,
  },
  title: {
    color: Colors.text,
    fontSize: FontSize.sm,
    fontWeight: '600',
  },
  meta: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
    marginTop: 2,
  },
});

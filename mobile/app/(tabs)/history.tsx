import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
  Alert,
  TouchableOpacity,
} from 'react-native';
import { useRouter, useFocusEffect } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, FontSize, BorderRadius } from '../../src/theme';
import MeasurementCard from '../../src/components/MeasurementCard';
import { getMeasurements, MeasurementSummary } from '../../src/api/client';

export default function HistoryScreen() {
  const router = useRouter();
  const [measurements, setMeasurements] = useState<MeasurementSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadMeasurements = async () => {
    try {
      const data = await getMeasurements(0, 50);
      setMeasurements(data);
    } catch (err) {
      // Server might not be available
    } finally {
      setLoading(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadMeasurements();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await loadMeasurements();
    setRefreshing(false);
  };

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <Ionicons name="folder-open-outline" size={64} color={Colors.textMuted} />
      <Text style={styles.emptyTitle}>No measurements yet</Text>
      <Text style={styles.emptyDesc}>
        Take a photo and measure an object to see your results here.
      </Text>
      <TouchableOpacity
        style={styles.emptyButton}
        onPress={() => router.push('/scan')}
      >
        <Text style={styles.emptyButtonText}>Start Measuring</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={measurements}
        numColumns={2}
        columnWrapperStyle={styles.row}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <MeasurementCard
            measurement={item}
            onPress={() => router.push(`/result/${item.id}`)}
          />
        )}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={Colors.primary}
          />
        }
        ListEmptyComponent={!loading ? renderEmpty : null}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  listContent: {
    padding: Spacing.lg,
    flexGrow: 1,
  },
  row: {
    justifyContent: 'space-between',
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 100,
  },
  emptyTitle: {
    color: Colors.text,
    fontSize: FontSize.lg,
    fontWeight: '600',
    marginTop: Spacing.md,
  },
  emptyDesc: {
    color: Colors.textMuted,
    fontSize: FontSize.sm,
    textAlign: 'center',
    marginTop: Spacing.sm,
    maxWidth: 250,
  },
  emptyButton: {
    marginTop: Spacing.lg,
    backgroundColor: Colors.primary,
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.md,
  },
  emptyButtonText: {
    color: Colors.white,
    fontWeight: '600',
  },
});

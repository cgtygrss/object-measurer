import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  Image,
  StyleSheet,
  Alert,
  TouchableOpacity,
  Dimensions,
  ActivityIndicator,
  Linking,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import * as Sharing from 'expo-sharing';
import { Paths, File } from 'expo-file-system';
import { Ionicons } from '@expo/vector-icons';
import {
  Colors,
  Spacing,
  FontSize,
  BorderRadius,
  Shadow,
} from '../../src/theme';
import Button from '../../src/components/ui/Button';
import {
  getMeasurement,
  deleteMeasurement,
  getExportPdfUrl,
  MeasurementResult,
  MeasurementLine,
} from '../../src/api/client';

const { width } = Dimensions.get('window');

export default function ResultScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const [result, setResult] = useState<MeasurementResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'image' | 'data'>('image');

  useEffect(() => {
    loadResult();
  }, [id]);

  const loadResult = async () => {
    try {
      const data = await getMeasurement(parseInt(id!));
      setResult(data);
    } catch (err: any) {
      Alert.alert('Error', 'Failed to load measurement result.');
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const handleShare = async () => {
    if (!result?.result_image_url) return;

    try {
      const response = await fetch(result.result_image_url);
      const blob = await response.blob();
      const file = new File(Paths.cache, `measurement_${result.id}.png`);
      const buffer = await blob.arrayBuffer();
      file.write(new Uint8Array(buffer));
      await Sharing.shareAsync(file.uri);
    } catch (err) {
      Alert.alert('Error', 'Failed to share image.');
    }
  };

  const handleExportPdf = async () => {
    if (!result) return;

    try {
      const pdfUrl = getExportPdfUrl(result.id);
      // Open the PDF URL in the browser for download
      const canOpen = await Linking.canOpenURL(pdfUrl);
      if (canOpen) {
        await Linking.openURL(pdfUrl);
      } else {
        Alert.alert('Error', 'Cannot open PDF URL.');
      }
    } catch (err) {
      Alert.alert('Error', 'Failed to export PDF. Make sure the server is running.');
    }
  };

  const handleDelete = () => {
    Alert.alert(
      'Delete Measurement',
      'Are you sure? This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteMeasurement(parseInt(id!));
              router.replace('/(tabs)/history');
            } catch {
              Alert.alert('Error', 'Failed to delete measurement.');
            }
          },
        },
      ]
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.primary} />
        <Text style={styles.loadingText}>Loading result...</Text>
      </View>
    );
  }

  if (!result) return null;

  const totalLines =
    result.horizontal_lines.length + result.vertical_lines.length;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header Stats */}
      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{totalLines}</Text>
          <Text style={styles.statLabel}>Measurements</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>
            {result.reference_height} {result.unit}
          </Text>
          <Text style={styles.statLabel}>Reference</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>
            {result.pixel_ratio?.toFixed(4) || 'N/A'}
          </Text>
          <Text style={styles.statLabel}>Px Ratio</Text>
        </View>
      </View>

      {/* Tab Switcher */}
      <View style={styles.tabRow}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'image' && styles.tabActive]}
          onPress={() => setActiveTab('image')}
        >
          <Text
            style={[
              styles.tabText,
              activeTab === 'image' && styles.tabTextActive,
            ]}
          >
            Image
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'data' && styles.tabActive]}
          onPress={() => setActiveTab('data')}
        >
          <Text
            style={[
              styles.tabText,
              activeTab === 'data' && styles.tabTextActive,
            ]}
          >
            Data ({totalLines})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Tab Content */}
      {activeTab === 'image' ? (
        <View style={styles.imageContainer}>
          {result.result_image_url ? (
            <Image
              source={{ uri: result.result_image_url }}
              style={styles.resultImage}
              resizeMode="contain"
            />
          ) : (
            <View style={styles.noImage}>
              <Ionicons
                name="image-outline"
                size={48}
                color={Colors.textMuted}
              />
              <Text style={styles.noImageText}>No result image available</Text>
            </View>
          )}
        </View>
      ) : (
        <View style={styles.dataContainer}>
          {result.horizontal_lines.length > 0 && (
            <View style={styles.dataSection}>
              <Text style={styles.dataSectionTitle}>
                Horizontal ({result.horizontal_lines.length})
              </Text>
              {result.horizontal_lines.map((line, idx) => (
                <LineRow key={`h-${idx}`} line={line} index={idx + 1} />
              ))}
            </View>
          )}
          {result.vertical_lines.length > 0 && (
            <View style={styles.dataSection}>
              <Text style={styles.dataSectionTitle}>
                Vertical ({result.vertical_lines.length})
              </Text>
              {result.vertical_lines.map((line, idx) => (
                <LineRow key={`v-${idx}`} line={line} index={idx + 1} />
              ))}
            </View>
          )}
          {totalLines === 0 && (
            <Text style={styles.noDataText}>No measurement data available.</Text>
          )}
        </View>
      )}

      {/* Notes */}
      {result.notes && (
        <View style={styles.notesCard}>
          <Text style={styles.notesTitle}>Notes</Text>
          <Text style={styles.notesText}>{result.notes}</Text>
        </View>
      )}

      {/* Actions */}
      <View style={styles.actionsSection}>
        <Text style={styles.actionsSectionTitle}>Actions</Text>
        <View style={styles.actionsGrid}>
          <Button
            title="Share Image"
            onPress={handleShare}
            variant="secondary"
            size="md"
            icon={<Ionicons name="share-outline" size={18} color={Colors.text} />}
            style={styles.actionButton}
          />
          <Button
            title="Export PDF"
            onPress={handleExportPdf}
            variant="secondary"
            size="md"
            icon={
              <Ionicons name="document-text-outline" size={18} color={Colors.text} />
            }
            style={styles.actionButton}
          />
        </View>
        <Button
          title="Delete Measurement"
          onPress={handleDelete}
          variant="ghost"
          size="sm"
          icon={<Ionicons name="trash-outline" size={16} color={Colors.error} />}
          textStyle={{ color: Colors.error }}
          style={{ alignSelf: 'center', marginTop: Spacing.md }}
        />
      </View>

      {/* Metadata */}
      <View style={styles.metaCard}>
        <Text style={styles.metaText}>
          Created: {new Date(result.created_at).toLocaleString()}
        </Text>
        <Text style={styles.metaText}>
          Updated: {new Date(result.updated_at).toLocaleString()}
        </Text>
      </View>
    </ScrollView>
  );
}

function LineRow({ line, index }: { line: MeasurementLine; index: number }) {
  return (
    <View style={lineStyles.row}>
      <Text style={lineStyles.index}>#{index}</Text>
      <Text style={lineStyles.coords}>
        ({line.start.x}, {line.start.y}) → ({line.end.x}, {line.end.y})
      </Text>
      <Text style={lineStyles.distance}>
        {line.distance} {line.unit}
      </Text>
    </View>
  );
}

const lineStyles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.sm,
    padding: Spacing.sm,
    marginBottom: Spacing.xs,
  },
  index: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
    width: 30,
  },
  coords: {
    flex: 1,
    color: Colors.textSecondary,
    fontSize: FontSize.xs,
  },
  distance: {
    color: Colors.primary,
    fontSize: FontSize.sm,
    fontWeight: '700',
  },
});

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    padding: Spacing.lg,
    paddingBottom: Spacing.xxl,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: Colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    gap: Spacing.md,
  },
  loadingText: {
    color: Colors.textSecondary,
    fontSize: FontSize.md,
  },
  statsRow: {
    flexDirection: 'row',
    gap: Spacing.sm,
    marginBottom: Spacing.lg,
  },
  statCard: {
    flex: 1,
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    alignItems: 'center',
    ...Shadow.sm,
  },
  statValue: {
    color: Colors.text,
    fontSize: FontSize.lg,
    fontWeight: '700',
  },
  statLabel: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
    marginTop: 2,
  },
  tabRow: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.md,
    padding: 3,
    marginBottom: Spacing.lg,
  },
  tab: {
    flex: 1,
    paddingVertical: Spacing.sm + 2,
    alignItems: 'center',
    borderRadius: BorderRadius.sm,
  },
  tabActive: {
    backgroundColor: Colors.primary,
  },
  tabText: {
    color: Colors.textMuted,
    fontSize: FontSize.sm,
    fontWeight: '600',
  },
  tabTextActive: {
    color: Colors.white,
  },
  imageContainer: {
    marginBottom: Spacing.lg,
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    ...Shadow.md,
  },
  resultImage: {
    width: '100%',
    height: width - Spacing.lg * 2,
    backgroundColor: Colors.surface,
  },
  noImage: {
    height: 200,
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  noImageText: {
    color: Colors.textMuted,
    marginTop: Spacing.sm,
  },
  dataContainer: {
    marginBottom: Spacing.lg,
  },
  dataSection: {
    marginBottom: Spacing.md,
  },
  dataSectionTitle: {
    color: Colors.text,
    fontSize: FontSize.md,
    fontWeight: '600',
    marginBottom: Spacing.sm,
  },
  noDataText: {
    color: Colors.textMuted,
    textAlign: 'center',
    paddingVertical: Spacing.xl,
  },
  notesCard: {
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    marginBottom: Spacing.lg,
  },
  notesTitle: {
    color: Colors.text,
    fontSize: FontSize.sm,
    fontWeight: '600',
    marginBottom: Spacing.xs,
  },
  notesText: {
    color: Colors.textSecondary,
    fontSize: FontSize.sm,
    lineHeight: 20,
  },
  actionsSection: {
    marginBottom: Spacing.lg,
  },
  actionsSectionTitle: {
    color: Colors.textSecondary,
    fontSize: FontSize.xs,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: Spacing.sm,
  },
  actionsGrid: {
    flexDirection: 'row',
    gap: Spacing.md,
  },
  actionButton: {
    flex: 1,
  },
  metaCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.sm,
    padding: Spacing.md,
    gap: 4,
  },
  metaText: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
  },
});

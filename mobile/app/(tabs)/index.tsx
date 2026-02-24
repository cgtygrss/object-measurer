import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Image,
  Dimensions,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import {
  Colors,
  Spacing,
  FontSize,
  BorderRadius,
  Shadow,
} from '../../src/theme';
import Button from '../../src/components/ui/Button';
import { getMeasurements, MeasurementSummary } from '../../src/api/client';

const { width } = Dimensions.get('window');

export default function HomeScreen() {
  const router = useRouter();
  const [recentMeasurements, setRecentMeasurements] = useState<
    MeasurementSummary[]
  >([]);
  const [refreshing, setRefreshing] = useState(false);

  const loadRecent = async () => {
    try {
      const data = await getMeasurements(0, 4);
      setRecentMeasurements(data);
    } catch {
      // Server might not be running yet
    }
  };

  useEffect(() => {
    loadRecent();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadRecent();
    setRefreshing(false);
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor={Colors.primary}
        />
      }
    >
      {/* Hero Section */}
      <LinearGradient
        colors={[Colors.primaryDark, Colors.primary, Colors.secondary]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.hero}
      >
        <Ionicons name="cube" size={48} color={Colors.white} />
        <Text style={styles.heroTitle}>Object Measurer</Text>
        <Text style={styles.heroSubtitle}>
          Measure any object instantly with your camera
        </Text>
      </LinearGradient>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick Start</Text>
        <View style={styles.actionGrid}>
          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/camera')}
            activeOpacity={0.8}
          >
            <View
              style={[styles.actionIcon, { backgroundColor: Colors.primary + '20' }]}
            >
              <Ionicons name="camera" size={28} color={Colors.primary} />
            </View>
            <Text style={styles.actionTitle}>Camera</Text>
            <Text style={styles.actionDesc}>Take a photo</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/scan')}
            activeOpacity={0.8}
          >
            <View
              style={[styles.actionIcon, { backgroundColor: Colors.secondary + '20' }]}
            >
              <Ionicons name="images" size={28} color={Colors.secondary} />
            </View>
            <Text style={styles.actionTitle}>Gallery</Text>
            <Text style={styles.actionDesc}>Import image</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/history')}
            activeOpacity={0.8}
          >
            <View
              style={[styles.actionIcon, { backgroundColor: Colors.accent + '20' }]}
            >
              <Ionicons name="time" size={28} color={Colors.accent} />
            </View>
            <Text style={styles.actionTitle}>History</Text>
            <Text style={styles.actionDesc}>Past results</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* How It Works */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>How It Works</Text>
        <View style={styles.stepsContainer}>
          {[
            {
              icon: 'camera-outline' as const,
              title: 'Capture',
              desc: 'Take a photo of your object or pick from gallery',
            },
            {
              icon: 'resize-outline' as const,
              title: 'Set Reference',
              desc: 'Enter a known measurement for calibration',
            },
            {
              icon: 'analytics-outline' as const,
              title: 'Measure',
              desc: 'Get accurate dimensions automatically',
            },
            {
              icon: 'share-outline' as const,
              title: 'Export',
              desc: 'Save as PDF or share with others',
            },
          ].map((step, idx) => (
            <View key={idx} style={styles.step}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>{idx + 1}</Text>
              </View>
              <View style={styles.stepContent}>
                <Ionicons
                  name={step.icon}
                  size={20}
                  color={Colors.primary}
                  style={{ marginRight: Spacing.sm }}
                />
                <View style={{ flex: 1 }}>
                  <Text style={styles.stepTitle}>{step.title}</Text>
                  <Text style={styles.stepDesc}>{step.desc}</Text>
                </View>
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* Recent Measurements */}
      {recentMeasurements.length > 0 && (
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recent</Text>
            <TouchableOpacity onPress={() => router.push('/history')}>
              <Text style={styles.seeAll}>See All</Text>
            </TouchableOpacity>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {recentMeasurements.map((m) => (
              <TouchableOpacity
                key={m.id}
                style={styles.recentCard}
                onPress={() => router.push(`/result/${m.id}`)}
                activeOpacity={0.8}
              >
                {m.result_image_url ? (
                  <Image
                    source={{ uri: m.result_image_url }}
                    style={styles.recentImage}
                  />
                ) : (
                  <View style={styles.recentPlaceholder}>
                    <Ionicons
                      name="cube-outline"
                      size={24}
                      color={Colors.textMuted}
                    />
                  </View>
                )}
                <Text style={styles.recentTitle} numberOfLines={1}>
                  {m.title}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      )}

      {/* CTA */}
      <View style={styles.ctaContainer}>
        <Button
          title="Start Measuring"
          onPress={() => router.push('/scan')}
          size="lg"
          icon={<Ionicons name="scan" size={20} color={Colors.white} />}
          style={{ width: '100%' }}
        />
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
    paddingBottom: Spacing.xxl,
  },
  hero: {
    padding: Spacing.xl,
    paddingTop: Spacing.xxl + 20,
    paddingBottom: Spacing.xl,
    alignItems: 'center',
    borderBottomLeftRadius: BorderRadius.xl,
    borderBottomRightRadius: BorderRadius.xl,
  },
  heroTitle: {
    fontSize: FontSize.hero,
    fontWeight: '800',
    color: Colors.white,
    marginTop: Spacing.md,
  },
  heroSubtitle: {
    fontSize: FontSize.md,
    color: 'rgba(255,255,255,0.8)',
    marginTop: Spacing.sm,
    textAlign: 'center',
  },
  section: {
    paddingHorizontal: Spacing.lg,
    marginTop: Spacing.xl,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.md,
  },
  sectionTitle: {
    fontSize: FontSize.xl,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: Spacing.md,
  },
  seeAll: {
    color: Colors.primary,
    fontSize: FontSize.sm,
    fontWeight: '600',
    marginBottom: Spacing.md,
  },
  actionGrid: {
    flexDirection: 'row',
    gap: Spacing.md,
  },
  actionCard: {
    flex: 1,
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    alignItems: 'center',
    ...Shadow.sm,
  },
  actionIcon: {
    width: 56,
    height: 56,
    borderRadius: BorderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.sm,
  },
  actionTitle: {
    color: Colors.text,
    fontSize: FontSize.sm,
    fontWeight: '600',
  },
  actionDesc: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
    marginTop: 2,
  },
  stepsContainer: {
    gap: Spacing.md,
  },
  step: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  stepNumber: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: Spacing.md,
  },
  stepNumberText: {
    color: Colors.white,
    fontSize: FontSize.sm,
    fontWeight: '700',
  },
  stepContent: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.sm,
    padding: Spacing.md,
  },
  stepTitle: {
    color: Colors.text,
    fontSize: FontSize.sm,
    fontWeight: '600',
  },
  stepDesc: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
    marginTop: 2,
  },
  recentCard: {
    width: 140,
    marginRight: Spacing.md,
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.sm,
    overflow: 'hidden',
    ...Shadow.sm,
  },
  recentImage: {
    width: '100%',
    height: 100,
    backgroundColor: Colors.surfaceLight,
  },
  recentPlaceholder: {
    width: '100%',
    height: 100,
    backgroundColor: Colors.surfaceLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  recentTitle: {
    color: Colors.text,
    fontSize: FontSize.xs,
    fontWeight: '500',
    padding: Spacing.sm,
  },
  ctaContainer: {
    paddingHorizontal: Spacing.lg,
    marginTop: Spacing.xl,
  },
});

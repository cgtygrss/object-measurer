import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Switch,
  TouchableOpacity,
  Alert,
  Linking,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, FontSize, BorderRadius } from '../../src/theme';
import UnitPicker from '../../src/components/ui/UnitPicker';
import { checkHealth } from '../../src/api/client';

export default function SettingsScreen() {
  const [defaultUnit, setDefaultUnit] = useState('cm');
  const [defaultInterval, setDefaultInterval] = useState(20);
  const [serverConnected, setServerConnected] = useState(false);

  useEffect(() => {
    loadSettings();
    checkServerStatus();
  }, []);

  const loadSettings = async () => {
    try {
      const unit = await AsyncStorage.getItem('defaultUnit');
      const interval = await AsyncStorage.getItem('defaultInterval');
      if (unit) setDefaultUnit(unit);
      if (interval) setDefaultInterval(parseInt(interval));
    } catch {}
  };

  const saveUnit = async (unit: string) => {
    setDefaultUnit(unit);
    await AsyncStorage.setItem('defaultUnit', unit);
  };

  const checkServerStatus = async () => {
    const ok = await checkHealth();
    setServerConnected(ok);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Server Status */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Server Status</Text>
        <View style={styles.card}>
          <View style={styles.statusRow}>
            <View style={styles.statusLeft}>
              <View
                style={[
                  styles.statusDot,
                  {
                    backgroundColor: serverConnected
                      ? Colors.success
                      : Colors.error,
                  },
                ]}
              />
              <Text style={styles.statusText}>
                {serverConnected ? 'Connected' : 'Disconnected'}
              </Text>
            </View>
            <TouchableOpacity onPress={checkServerStatus}>
              <Ionicons name="refresh" size={20} color={Colors.primary} />
            </TouchableOpacity>
          </View>
          {!serverConnected && (
            <Text style={styles.hintText}>
              Make sure the backend server is running.{'\n'}
              Run: cd backend && uvicorn app.main:app --reload
            </Text>
          )}
        </View>
      </View>

      {/* Default Unit */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Defaults</Text>
        <View style={styles.card}>
          <UnitPicker value={defaultUnit} onChange={saveUnit} />
        </View>
      </View>

      {/* About */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        <View style={styles.card}>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>Version</Text>
            <Text style={styles.aboutValue}>1.0.0</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>Build</Text>
            <Text style={styles.aboutValue}>2026.1</Text>
          </View>
          <View style={styles.divider} />
          <TouchableOpacity
            style={styles.aboutRow}
            onPress={() =>
              Linking.openURL('https://github.com/object-measurer')
            }
          >
            <Text style={styles.aboutLabel}>Source Code</Text>
            <Ionicons
              name="open-outline"
              size={16}
              color={Colors.primary}
            />
          </TouchableOpacity>
        </View>
      </View>

      {/* Privacy */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Privacy</Text>
        <View style={styles.card}>
          <Text style={styles.privacyText}>
            All image processing happens on your private server. No images are
            sent to third parties. Measurement data is stored locally in the
            server database. You can delete any measurement at any time.
          </Text>
        </View>
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
  section: {
    marginBottom: Spacing.xl,
  },
  sectionTitle: {
    color: Colors.textSecondary,
    fontSize: FontSize.xs,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: Spacing.sm,
  },
  card: {
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: Spacing.sm,
  },
  statusText: {
    color: Colors.text,
    fontSize: FontSize.md,
    fontWeight: '500',
  },
  hintText: {
    color: Colors.textMuted,
    fontSize: FontSize.xs,
    marginTop: Spacing.sm,
    lineHeight: 18,
  },
  aboutRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: Spacing.sm,
  },
  aboutLabel: {
    color: Colors.text,
    fontSize: FontSize.md,
  },
  aboutValue: {
    color: Colors.textSecondary,
    fontSize: FontSize.md,
  },
  divider: {
    height: 1,
    backgroundColor: Colors.border,
  },
  privacyText: {
    color: Colors.textSecondary,
    fontSize: FontSize.sm,
    lineHeight: 20,
  },
});

/**
 * History Tab — Browse past measurements.
 */

import React, { useEffect, useState } from 'react';
import {
    StyleSheet,
    View,
    Text,
    FlatList,
    TouchableOpacity,
    ActivityIndicator,
    Alert,
    RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, BorderRadius, FontSize, Shadows } from '../../constants/theme';
import { useAppStore, MeasurementItem } from '../../store';
import { measurementAPI } from '../../services/api';
import { formatMeasurement, UnitType } from '../../utils/units';

export default function HistoryScreen() {
    const { measurements, totalMeasurements, setMeasurements, removeMeasurement, unit, isAuthenticated } = useAppStore();
    const [loading, setLoading] = useState(false);
    const [refreshing, setRefreshing] = useState(false);

    const fetchHistory = async (isRefresh = false) => {
        if (!isAuthenticated) return;
        isRefresh ? setRefreshing(true) : setLoading(true);

        try {
            const response = await measurementAPI.getHistory(1, 50);
            setMeasurements(response.data.measurements, response.data.total);
        } catch (error) {
            console.error('Failed to fetch history:', error);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, [isAuthenticated]);

    const handleDelete = (id: string) => {
        Alert.alert('Delete Measurement', 'Are you sure?', [
            { text: 'Cancel', style: 'cancel' },
            {
                text: 'Delete',
                style: 'destructive',
                onPress: async () => {
                    try {
                        await measurementAPI.delete(id);
                        removeMeasurement(id);
                    } catch (error) {
                        Alert.alert('Error', 'Failed to delete');
                    }
                },
            },
        ]);
    };

    const renderItem = ({ item }: { item: MeasurementItem }) => (
        <View style={styles.card}>
            <View style={styles.cardHeader}>
                <View style={styles.modeBadge}>
                    <Ionicons
                        name={item.mode === 'photo' ? 'camera' : 'videocam'}
                        size={12}
                        color={Colors.primary}
                    />
                    <Text style={styles.modeBadgeText}>
                        {item.mode === 'photo' ? 'Photo' : 'Real-Time'}
                    </Text>
                </View>
                <Text style={styles.dateText}>
                    {new Date(item.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                    })}
                </Text>
            </View>

            <View style={styles.dimensionsRow}>
                {item.width_mm != null && (
                    <View style={styles.dimItem}>
                        <Text style={styles.dimValue}>
                            {formatMeasurement(item.width_mm, unit as UnitType)}
                        </Text>
                        <Text style={styles.dimLabel}>Width</Text>
                    </View>
                )}
                {item.height_mm != null && (
                    <View style={styles.dimItem}>
                        <Text style={styles.dimValue}>
                            {formatMeasurement(item.height_mm, unit as UnitType)}
                        </Text>
                        <Text style={styles.dimLabel}>Height</Text>
                    </View>
                )}
                {item.area_mm2 != null && (
                    <View style={styles.dimItem}>
                        <Text style={styles.dimValue}>
                            {formatMeasurement(item.area_mm2, unit as UnitType)}²
                        </Text>
                        <Text style={styles.dimLabel}>Area</Text>
                    </View>
                )}
            </View>

            <TouchableOpacity style={styles.deleteButton} onPress={() => handleDelete(item.id)}>
                <Ionicons name="trash-outline" size={16} color={Colors.error} />
            </TouchableOpacity>
        </View>
    );

    if (!isAuthenticated) {
        return (
            <View style={styles.container}>
                <View style={styles.emptyState}>
                    <Ionicons name="log-in-outline" size={48} color={Colors.textSecondary} />
                    <Text style={styles.emptyTitle}>Login Required</Text>
                    <Text style={styles.emptyText}>Sign in to view your measurement history.</Text>
                </View>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <Text style={styles.headerTitle}>Measurement History</Text>
            <Text style={styles.headerSubtitle}>{totalMeasurements} measurements</Text>

            {loading ? (
                <ActivityIndicator color={Colors.primary} size="large" style={{ marginTop: 60 }} />
            ) : (
                <FlatList
                    data={measurements}
                    keyExtractor={(item) => item.id}
                    renderItem={renderItem}
                    contentContainerStyle={styles.list}
                    refreshControl={
                        <RefreshControl
                            refreshing={refreshing}
                            onRefresh={() => fetchHistory(true)}
                            tintColor={Colors.primary}
                        />
                    }
                    ListEmptyComponent={
                        <View style={styles.emptyState}>
                            <Ionicons name="resize-outline" size={48} color={Colors.textSecondary} />
                            <Text style={styles.emptyTitle}>No Measurements Yet</Text>
                            <Text style={styles.emptyText}>
                                Start measuring objects with the camera tab!
                            </Text>
                        </View>
                    }
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Colors.background,
        paddingTop: 60,
    },
    headerTitle: {
        fontSize: FontSize.xxl,
        fontWeight: '800',
        color: Colors.textPrimary,
        paddingHorizontal: Spacing.lg,
    },
    headerSubtitle: {
        fontSize: FontSize.md,
        color: Colors.textSecondary,
        paddingHorizontal: Spacing.lg,
        marginTop: Spacing.xs,
        marginBottom: Spacing.md,
    },
    list: {
        paddingHorizontal: Spacing.md,
        paddingBottom: 100,
    },
    card: {
        backgroundColor: Colors.surface,
        borderRadius: BorderRadius.lg,
        padding: Spacing.md,
        marginBottom: Spacing.sm,
        borderWidth: 1,
        borderColor: Colors.border,
        ...Shadows.sm,
    },
    cardHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Spacing.sm,
    },
    modeBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Colors.surfaceLight,
        paddingHorizontal: Spacing.sm,
        paddingVertical: 4,
        borderRadius: BorderRadius.full,
        gap: 4,
    },
    modeBadgeText: {
        fontSize: FontSize.xs,
        color: Colors.primary,
        fontWeight: '600',
    },
    dateText: {
        fontSize: FontSize.xs,
        color: Colors.textMuted,
    },
    dimensionsRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
    },
    dimItem: {
        alignItems: 'center',
    },
    dimValue: {
        fontSize: FontSize.lg,
        fontWeight: '700',
        color: Colors.textPrimary,
    },
    dimLabel: {
        fontSize: FontSize.xs,
        color: Colors.textSecondary,
        marginTop: 2,
    },
    deleteButton: {
        position: 'absolute',
        top: Spacing.sm,
        right: Spacing.sm,
        padding: Spacing.xs,
    },
    emptyState: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingTop: 80,
    },
    emptyTitle: {
        fontSize: FontSize.xl,
        fontWeight: '700',
        color: Colors.textPrimary,
        marginTop: Spacing.md,
    },
    emptyText: {
        fontSize: FontSize.md,
        color: Colors.textSecondary,
        marginTop: Spacing.xs,
        textAlign: 'center',
        paddingHorizontal: Spacing.xl,
    },
});

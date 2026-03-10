/**
 * Unit conversion utilities for measurements.
 */

export type UnitType = 'mm' | 'cm' | 'in';

const CONVERSION_FACTORS: Record<UnitType, number> = {
    mm: 1,
    cm: 0.1,
    in: 0.0393701,
};

export function convertFromMm(valueMm: number, targetUnit: UnitType): number {
    return Math.round(valueMm * CONVERSION_FACTORS[targetUnit] * 100) / 100;
}

export function getUnitLabel(unit: UnitType): string {
    switch (unit) {
        case 'mm':
            return 'mm';
        case 'cm':
            return 'cm';
        case 'in':
            return 'in';
    }
}

export function formatMeasurement(valueMm: number, unit: UnitType): string {
    const converted = convertFromMm(valueMm, unit);
    return `${converted} ${getUnitLabel(unit)}`;
}

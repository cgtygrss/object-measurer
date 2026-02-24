import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import Svg, { Line, Text as SvgText, Circle } from 'react-native-svg';
import { Colors } from '../theme';
import type { MeasurementLine } from '../api/client';

interface MeasurementOverlayProps {
  horizontalLines: MeasurementLine[];
  verticalLines: MeasurementLine[];
  imageWidth: number;
  imageHeight: number;
  displayWidth: number;
  displayHeight: number;
}

/**
 * SVG overlay that renders measurement lines on top of the result image.
 * Scales coordinates from original image space to display space.
 */
export default function MeasurementOverlay({
  horizontalLines,
  verticalLines,
  imageWidth,
  imageHeight,
  displayWidth,
  displayHeight,
}: MeasurementOverlayProps) {
  if (imageWidth === 0 || imageHeight === 0) return null;

  const scaleX = displayWidth / imageWidth;
  const scaleY = displayHeight / imageHeight;

  const renderLine = (line: MeasurementLine, index: number, color: string) => {
    const x1 = line.start.x * scaleX;
    const y1 = line.start.y * scaleY;
    const x2 = line.end.x * scaleX;
    const y2 = line.end.y * scaleY;
    const midX = (x1 + x2) / 2;
    const midY = (y1 + y2) / 2;

    return (
      <React.Fragment key={`${color}-${index}`}>
        {/* End point circles */}
        <Circle cx={x1} cy={y1} r={4} fill={color} opacity={0.8} />
        <Circle cx={x2} cy={y2} r={4} fill={color} opacity={0.8} />

        {/* Measurement line */}
        <Line
          x1={x1}
          y1={y1}
          x2={x2}
          y2={y2}
          stroke={color}
          strokeWidth={2}
          strokeDasharray="6,3"
          opacity={0.9}
        />

        {/* Distance label */}
        <SvgText
          x={midX}
          y={midY - 8}
          fill={Colors.white}
          fontSize={11}
          fontWeight="bold"
          textAnchor="middle"
          stroke={Colors.black}
          strokeWidth={0.5}
        >
          {line.distance.toFixed(1)} {line.unit}
        </SvgText>
      </React.Fragment>
    );
  };

  return (
    <View style={[styles.container, { width: displayWidth, height: displayHeight }]}>
      <Svg width={displayWidth} height={displayHeight}>
        {horizontalLines.map((line, idx) =>
          renderLine(line, idx, '#FF6B6B')
        )}
        {verticalLines.map((line, idx) =>
          renderLine(line, idx, '#4ECDC4')
        )}
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
  },
});

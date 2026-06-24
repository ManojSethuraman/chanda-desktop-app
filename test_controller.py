#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick test for analysis controller fixes."""

from controllers.analysis_controller import AnalysisController

# Create controller
ac = AnalysisController()

# Test 1: Single line analysis
print("=" * 60)
print("TEST 1: Single Line Analysis")
print("=" * 60)
result = ac.analyze('धर्मक्षेत्रे कुरुक्षेत्रे', scheme='Devanagari')
print(f"Success: {result.success}")
print(f"Detected Scheme: {result.input_scheme}")
print(f"Pattern: {result.lines[0]['pattern']}")
print(f"Syllables: {result.lines[0]['syllables']}")
print(f"Syllable Count: {result.lines[0]['syllable_count']}")
print(f"Meters Found: {len(result.lines[0]['meters'])}")
if result.lines[0]['meters']:
    print(f"First Meter: {result.lines[0]['meters'][0]['name']} (exact: {result.lines[0]['meters'][0]['exact']})")

# Test 2: Fuzzy matching
print("\n" + "=" * 60)
print("TEST 2: Fuzzy Matching")
print("=" * 60)
result2 = ac.analyze('कविता रचना है', scheme='Devanagari', fuzzy=True, k=5)
print(f"Success: {result2.success}")
print(f"Pattern: {result2.lines[0]['pattern']}")
print(f"Fuzzy Meters Found: {len(result2.lines[0]['meters'])}")
for i, meter in enumerate(result2.lines[0]['meters'][:3], 1):
    print(f"  {i}. {meter['name']} (similarity: {meter.get('similarity', 1.0):.1%})")

# Test 3: Multi-line verse
print("\n" + "=" * 60)
print("TEST 3: Multi-line Verse")
print("=" * 60)
verse = """धर्मक्षेत्रे कुरुक्षेत्रे
समवेता युयुत्सवः
मामकाः पाण्डवाश्चैव
किमकुर्वत सञ्जय"""
result3 = ac.analyze(verse, scheme='Devanagari', verse_mode=True)
print(f"Success: {result3.success}")
print(f"Lines Analyzed: {len(result3.lines)}")
for i, line in enumerate(result3.lines, 1):
    print(f"Line {i}: {line['pattern']} ({line['syllable_count']} syllables)")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED ✅")
print("=" * 60)

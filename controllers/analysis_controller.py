#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis Controller for Chanda Desktop.

This module provides a wrapper around the chanda library for meter analysis,
with enhanced error handling, result formatting, and integration with the UI.
"""

from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

try:
    from chanda import Chanda, ChandaError, InvalidInputError
    CHANDA_AVAILABLE = True
except ImportError:
    CHANDA_AVAILABLE = False
    ChandaError = Exception
    InvalidInputError = Exception


@dataclass
class AnalysisResult:
    """
    Container for analysis results.
    
    Attributes:
        input_text: Original input text
        input_scheme: Input transliteration scheme
        success: Whether analysis succeeded
        error_message: Error message if failed
        lines: List of line results
        verse_info: Information about verse structure
        timestamp: When analysis was performed
    """
    input_text: str
    input_scheme: str
    success: bool
    error_message: Optional[str] = None
    lines: Optional[List[Dict[str, Any]]] = None
    verse_info: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class AnalysisController:
    """
    Controller for Sanskrit meter analysis using the chanda library.
    
    This class wraps the chanda library and provides:
    - Single line and multi-line analysis
    - Fuzzy matching with configurable k-value
    - Result formatting for UI display
    - Error handling and validation
    - Transliteration scheme support
    
    Attributes:
        chanda: Instance of the Chanda analyzer
        available: Whether chanda library is available
        fuzzy_enabled: Whether fuzzy matching is enabled
        fuzzy_k: Number of fuzzy matches to return
        verse_mode: Whether to analyze as verse (multi-line)
    """
    
    def __init__(self):
        """Initialize the analysis controller."""
        self.available = CHANDA_AVAILABLE
        self.chanda = None
        
        if self.available:
            try:
                self.chanda = Chanda()
            except Exception as e:
                self.available = False
                print(f"Failed to initialize Chanda: {e}")
        
        # Default settings
        self.fuzzy_enabled = True
        self.fuzzy_k = 10
        self.verse_mode = False
    
    def analyze(
        self,
        text: str,
        scheme: str = "Devanagari",
        fuzzy: bool = True,
        k: int = 10,
        verse_mode: bool = False
    ) -> AnalysisResult:
        """
        Analyze Sanskrit text for meter identification.
        
        Args:
            text: Input text to analyze
            scheme: Transliteration scheme (Devanagari, IAST, etc.)
            fuzzy: Enable fuzzy matching
            k: Number of fuzzy matches to return
            verse_mode: Analyze as verse (multi-line)
            
        Returns:
            AnalysisResult containing analysis results or error
        """
        # Validate
        if not self.available:
            return AnalysisResult(
                input_text=text,
                input_scheme=scheme,
                success=False,
                error_message="Chanda library is not available. Please install it using: pip install chanda"
            )
        
        if not text or not text.strip():
            return AnalysisResult(
                input_text=text,
                input_scheme=scheme,
                success=False,
                error_message="Input text is empty. Please enter some Sanskrit text to analyze."
            )
        
        # Update settings
        self.fuzzy_enabled = fuzzy
        self.fuzzy_k = k
        self.verse_mode = verse_mode
        
        try:
            # Analyze based on mode
            if verse_mode or '\n' in text:
                return self._analyze_multi_line(text, scheme)
            else:
                return self._analyze_single_line(text, scheme)
        
        except InvalidInputError as e:
            return AnalysisResult(
                input_text=text,
                input_scheme=scheme,
                success=False,
                error_message=f"Invalid input: {str(e)}"
            )
        except ChandaError as e:
            return AnalysisResult(
                input_text=text,
                input_scheme=scheme,
                success=False,
                error_message=f"Analysis error: {str(e)}"
            )
        except Exception as e:
            return AnalysisResult(
                input_text=text,
                input_scheme=scheme,
                success=False,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    def _analyze_single_line(self, text: str, scheme: str) -> AnalysisResult:
        """
        Analyze a single line of text.
        
        Args:
            text: Single line of text
            scheme: Transliteration scheme
            
        Returns:
            AnalysisResult with line analysis
        """
        # Use chanda's analyze_line method
        result = self.chanda.analyze_line(
            text.strip(),
            input_scheme=scheme
        )
        
        # Format result
        line_results = []
        
        # Extract pattern (laghu-guru)
        pattern = result.get('pattern', '')
        
        # Extract matched meters
        meters = result.get('meters', [])
        
        # Get syllables
        syllables = result.get('syllables', [])
        
        # Build line result
        line_data = {
            'text': text.strip(),
            'pattern': pattern,
            'syllables': syllables,
            'syllable_count': len(syllables),
            'meters': meters[:self.fuzzy_k] if self.fuzzy_enabled else meters,
            'exact_match': len(meters) > 0 and meters[0].get('exact', False) if meters else False
        }
        
        line_results.append(line_data)
        
        return AnalysisResult(
            input_text=text,
            input_scheme=scheme,
            success=True,
            lines=line_results,
            timestamp=datetime.now()
        )
    
    def _analyze_multi_line(self, text: str, scheme: str) -> AnalysisResult:
        """
        Analyze multiple lines (verse) of text.
        
        Args:
            text: Multi-line text
            scheme: Transliteration scheme
            
        Returns:
            AnalysisResult with verse analysis
        """
        # Split into lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return AnalysisResult(
                input_text=text,
                input_scheme=scheme,
                success=False,
                error_message="No valid lines found in input."
            )
        
        # Analyze each line
        line_results = []
        
        for line_text in lines:
            try:
                result = self.chanda.analyze_line(
                    line_text,
                    input_scheme=scheme
                )
                
                # Extract data
                pattern = result.get('pattern', '')
                meters = result.get('meters', [])
                syllables = result.get('syllables', [])
                
                line_data = {
                    'text': line_text,
                    'pattern': pattern,
                    'syllables': syllables,
                    'syllable_count': len(syllables),
                    'meters': meters[:self.fuzzy_k] if self.fuzzy_enabled else meters,
                    'exact_match': len(meters) > 0 and meters[0].get('exact', False) if meters else False
                }
                
                line_results.append(line_data)
            
            except Exception as e:
                # Add line with error
                line_results.append({
                    'text': line_text,
                    'error': str(e),
                    'pattern': '',
                    'syllables': [],
                    'syllable_count': 0,
                    'meters': []
                })
        
        # Determine verse info
        verse_info = self._analyze_verse_structure(line_results)
        
        return AnalysisResult(
            input_text=text,
            input_scheme=scheme,
            success=True,
            lines=line_results,
            verse_info=verse_info,
            timestamp=datetime.now()
        )
    
    def _analyze_verse_structure(self, line_results: List[Dict]) -> Dict[str, Any]:
        """
        Analyze the structure of a verse based on line patterns.
        
        Args:
            line_results: List of line analysis results
            
        Returns:
            Dictionary with verse structure information
        """
        verse_info = {
            'total_lines': len(line_results),
            'patterns': [line.get('pattern', '') for line in line_results],
            'syllable_counts': [line.get('syllable_count', 0) for line in line_results],
            'uniform_pattern': False,
            'common_meters': []
        }
        
        # Check if all lines have the same pattern
        patterns = verse_info['patterns']
        if patterns and all(p == patterns[0] for p in patterns if p):
            verse_info['uniform_pattern'] = True
            verse_info['common_pattern'] = patterns[0]
        
        # Find meters common to all lines
        if line_results:
            # Get meters from first line
            first_line_meters = set(m.get('name', '') for m in line_results[0].get('meters', []))
            
            # Check which meters appear in all lines
            for line in line_results[1:]:
                line_meters = set(m.get('name', '') for m in line.get('meters', []))
                first_line_meters = first_line_meters.intersection(line_meters)
            
            verse_info['common_meters'] = list(first_line_meters)
        
        return verse_info
    
    def format_result_for_display(self, result: AnalysisResult) -> str:
        """
        Format analysis result for display in the UI.
        
        Args:
            result: AnalysisResult to format
            
        Returns:
            Formatted string for display
        """
        if not result.success:
            return f"ERROR\n\n{result.error_message}"
        
        lines = []
        lines.append("=== Analysis Results ===")
        lines.append("=" * 60)
        lines.append("")
        
        # Display line-by-line results
        if result.lines:
            for i, line_data in enumerate(result.lines, 1):
                if 'error' in line_data:
                    lines.append(f"Line {i}: ❌ {line_data['error']}")
                    continue
                
                lines.append(f"Line {i}: {line_data['text']}")
                lines.append(f"  Pattern: {line_data['pattern']} ({line_data['syllable_count']} syllables)")
                
                # Display meters
                meters = line_data.get('meters', [])
                if meters:
                    lines.append(f"  Identified Meters:")
                    for j, meter in enumerate(meters[:5], 1):  # Show top 5
                        meter_name = meter.get('name', 'Unknown')
                        similarity = meter.get('similarity', 1.0)
                        exact = meter.get('exact', False)
                        
                        if exact:
                            lines.append(f"    {j}. [EXACT] {meter_name}")
                        else:
                            lines.append(f"    {j}. {meter_name} (similarity: {similarity:.2%})")
                else:
                    lines.append(f"  No matching meters found")
                
                lines.append("")
        
        # Display verse info if available
        if result.verse_info:
            verse_info = result.verse_info
            lines.append("=== Verse Structure ===")
            lines.append("-" * 60)
            lines.append(f"Total Lines: {verse_info['total_lines']}")
            
            if verse_info.get('uniform_pattern'):
                lines.append(f"Pattern: Uniform ({verse_info.get('common_pattern', '')})")
            else:
                lines.append(f"Pattern: Non-uniform")
            
            if verse_info.get('common_meters'):
                lines.append(f"Common Meters: {', '.join(verse_info['common_meters'])}")
            
            lines.append("")
        
        # Add timestamp
        if result.timestamp:
            lines.append(f"Analyzed at: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(lines)
    
    def get_all_meters(self) -> List[str]:
        """
        Get list of all available meters.
        
        Returns:
            List of meter names
        """
        if not self.available or not self.chanda:
            return []
        
        try:
            # Get all chanda definitions
            chandas = self.chanda.CHANDA
            return list(chandas.keys())
        except:
            return []
    
    def get_meter_info(self, meter_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific meter.
        
        Args:
            meter_name: Name of the meter
            
        Returns:
            Dictionary with meter information or None
        """
        if not self.available or not self.chanda:
            return None
        
        try:
            chandas = self.chanda.CHANDA
            if meter_name in chandas:
                return chandas[meter_name]
        except:
            pass
        
        return None

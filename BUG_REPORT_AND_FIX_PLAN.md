# Bug Report and Fix Plan

**Date:** 2025-06-24  
**Status:** Critical - Application Non-Functional  
**Severity:** HIGH - Core functionality broken

## Executive Summary

End-user testing revealed that the application **cannot function** due to incorrect Chanda library API usage. The `analysis_controller.py` was written based on assumed API behavior, not the actual Chanda v1.1.0 API.

## Critical Issues Found

### Issue 1: Incorrect API Call ❌ CRITICAL

**Problem:**
```python
# Our code (WRONG):
result = self.chanda.analyze_line(
    line_text,
    input_scheme=scheme  # ← This parameter doesn't exist!
)
```

**Actual API:**
```python
# Correct signature:
def analyze_line(self, line: str, fuzzy: bool = False, k: int = 10) -> ChandaResult
```

**Impact:** Application crashes immediately when trying to analyze any text.

---

### Issue 2: Wrong Data Structure Mapping ❌ CRITICAL

**Problem:** Our code expects result as a dict with keys like `pattern`, `meters`, `syllables`, but Chanda returns a `ChandaResult` dataclass with different attributes.

**What We Expect:**
```python
{
    'pattern': 'LGGLGG',  # String of L and G
    'meters': [{'name': 'Anuṣṭubh', 'similarity': 1.0, 'exact': True}],
    'syllables': ['धर्', 'मक्', 'क्षे', ...]
}
```

**What Chanda Actually Returns:**
```python
ChandaResult(
    line='धर्मक्षेत्रे कुरुक्षेत्रे',
    lg=['ग', 'ग', 'ग', 'ग', 'ल', 'ग', 'ग', 'ग'],  # List of 'ग'/'ल' in Devanagari!
    syllables=['ध', 'र्म', 'क्षे', 'त्रे', 'कु', 'रु', 'क्षे', 'त्रे'],
    chanda=[('वक्त्र', ('1',)), ('अनुष्टुभ्', ('1',))],  # Tuples, not dicts!
    found=True,  # Boolean, not in our structure
    scheme='devanagari',  # Auto-detected
    length=8,
    fuzzy=[],  # List of fuzzy matches (when found=False)
    gana='गगगगलगगगग',
    matra=None,
    jaati=None
)
```

**Impact:** Even if API call worked, all data extraction would fail.

---

### Issue 3: Laghu-Guru Display Wrong ❌ HIGH

**Problem:** We display 'L' and 'G' in blue/red, but Chanda returns 'ल' (laghu) and 'ग' (guru) in Devanagari script.

**Current Display:** `Pattern: LGGLGG`  
**Actual Data:** `['ग', 'ग', 'ल', 'ग', 'ग']`

**Impact:** Pattern display will show Devanagari characters or fail to map colors correctly.

---

### Issue 4: Meter Name Format Wrong ❌ MEDIUM

**Problem:** Meter names are in Devanagari tuples `('अनुष्टुभ्', ('1',))`, not dicts with English names.

**What We Show:** "Anuṣṭubh"  
**What We Get:** "अनुष्टुभ्" with pada number tuple

**Impact:** Meter names display in Devanagari instead of romanized form.

---

### Issue 5: Fuzzy Matching Structure Different ❌ MEDIUM

**Problem:** Fuzzy matches are in a separate `fuzzy` list with different structure:

```python
result.fuzzy = [
    {
        'chanda': [('चित्रपदा', ('',))],
        'gana': 'भभगग',
        'suggestion': [[[...]]],
        'cost': 1,
        'similarity': 0.875
    }
]
```

Our code expects `meters` list with similarity already merged.

---

### Issue 6: Input Scheme Ignored ⚠️ LOW

**Problem:** The script selector dropdown in UI doesn't do anything - Chanda auto-detects the scheme.

**Impact:** User confusion - selecting "IAST" or "Harvard-Kyoto" has no effect on analysis.

## Fix Plan

### Phase 1: Core API Fix (HIGH PRIORITY)

#### Task 1.1: Update `analysis_controller.py` API Calls ✅

**File:** `controllers/analysis_controller.py`

**Changes needed:**

1. Remove `input_scheme` parameter from `analyze_line()` calls
2. Pass `fuzzy` and `k` parameters correctly
3. Handle `ChandaResult` dataclass attributes instead of dict keys

**Before:**
```python
result = self.chanda.analyze_line(
    line_text,
    input_scheme=scheme
)
pattern = result.get('pattern', '')
meters = result.get('meters', [])
syllables = result.get('syllables', [])
```

**After:**
```python
result = self.chanda.analyze_line(
    line_text,
    fuzzy=self.fuzzy_enabled,
    k=self.fuzzy_k
)
# Convert ग/ल to G/L for display
lg_pattern = ''.join(['G' if x == 'ग' else 'L' for x in result.lg])
syllables = result.syllables

# Extract meters
if result.found:
    meters = [{'name': name, 'pada': pada, 'exact': True} 
              for name, pada in result.chanda]
else:
    meters = [{'name': m['chanda'][0][0], 'similarity': m['similarity'], 'exact': False}
              for m in result.fuzzy]
```

#### Task 1.2: Update `_analyze_single_line()` Method ✅

**Changes:**
- Use `result.lg` for pattern (convert ग→G, ल→L)
- Use `result.syllables` directly (already a list)
- Extract meters from `result.chanda` (exact) or `result.fuzzy` (approximate)
- Handle `result.found` boolean

#### Task 1.3: Update `_analyze_multi_line()` Method ✅

**Changes:**
- Apply same fixes for each line
- Remove any dict `.get()` calls
- Use dataclass attribute access

---

### Phase 2: Display Format Fix (MEDIUM PRIORITY)

#### Task 2.1: Fix Laghu-Guru Color Mapping ✅

**File:** `ui/widgets/results_display.py`

**Current:** Expects 'L' and 'G' characters  
**Fix:** Convert 'ग'/'ल' to 'G'/'L' in controller before passing to display

*Note: Already handled in Phase 1 controller fix*

#### Task 2.2: Meter Name Display ✅

**Options:**
1. Display Devanagari names as-is (authentic)
2. Add romanization mapping (more work)
3. Use library's built-in formatting if available

**Recommendation:** Display Devanagari meter names - users working with Sanskrit should read Devanagari.

#### Task 2.3: Similarity Score Display ✅

**Current:** Shows as percentage `98.5%`  
**Fix:** Format `result.fuzzy[i]['similarity']` as percentage

---

### Phase 3: Input Scheme Handling (LOW PRIORITY)

#### Task 3.1: Options for Script Selector

**Option A (Simple):** Remove the dropdown - Chanda auto-detects  
**Option B (Advanced):** Use `process_text()` to pre-convert input  
**Option C (Keep):** Keep for user guidance, add help text "Auto-detected"

**Recommendation:** Option C - Keep the selector for user understanding, but show auto-detected scheme in results.

---

### Phase 4: Testing (REQUIRED)

#### Task 4.1: Unit Tests for Controller

- Test exact match (Devanagari input)
- Test fuzzy match (non-standard input)
- Test multi-line verse
- Test error handling

#### Task 4.2: Integration Tests

- Test UI → Controller → Display flow
- Test history integration
- Test clipboard operations
- Verify color display works

#### Task 4.3: End-User Scenarios

1. **Scenario 1:** Paste Devanagari verse
2. **Scenario 2:** Type IAST text
3. **Scenario 3:** Enable fuzzy matching
4. **Scenario 4:** Multi-line verse analysis
5. **Scenario 5:** History and favorites

---

## Implementation Priority

### Immediate (Must Fix Now):
1. ✅ Fix `analyze_line()` API calls - remove `input_scheme` parameter
2. ✅ Convert `ChandaResult` to expected dict structure
3. ✅ Map ग/ल to G/L for pattern display
4. ✅ Extract meter data from tuples

### Next (Before Release):
5. ✅ Fix meter name display format
6. ✅ Test with real Sanskrit text
7. ✅ Verify all UI features work

### Future (Nice to Have):
8. ⏸️ Add romanization for meter names
9. ⏸️ Improve input scheme handling
10. ⏸️ Add tooltips explaining auto-detection

---

## Testing Checklist

After fixes, verify:

- [ ] App launches without errors
- [ ] Can analyze single line Devanagari text
- [ ] Pattern shows correct blue/red colors for L/G
- [ ] Syllable grid displays correctly
- [ ] Meter names appear (Devanagari or romanized)
- [ ] Fuzzy matching returns multiple results
- [ ] Top-K value changes number of fuzzy results
- [ ] Multi-line verse analysis works
- [ ] History tracking saves correctly
- [ ] Favorites can be added
- [ ] Theme toggle works
- [ ] Keyboard shortcuts respond
- [ ] Copy/paste clipboard operations work

---

## Code Examples

### Example Fix for `_analyze_single_line`:

```python
def _analyze_single_line(self, text: str, scheme: str) -> AnalysisResult:
    """Analyze a single line of text."""
    # Call Chanda API correctly
    result = self.chanda.analyze_line(
        text.strip(),
        fuzzy=self.fuzzy_enabled,
        k=self.fuzzy_k
    )
    
    # Convert Devanagari ग/ल to English G/L
    lg_pattern = ''.join(['G' if x == 'ग' else 'L' if x == 'ल' else x 
                          for x in result.lg])
    
    # Extract meters
    meters = []
    if result.found:
        # Exact matches
        for chanda_name, pada_tuple in result.chanda:
            meters.append({
                'name': chanda_name,
                'pada': pada_tuple[0] if pada_tuple else '',
                'exact': True,
                'similarity': 1.0
            })
    
    if result.fuzzy:
        # Fuzzy matches
        for fuzzy_item in result.fuzzy:
            chanda_name = fuzzy_item['chanda'][0][0] if fuzzy_item['chanda'] else 'Unknown'
            meters.append({
                'name': chanda_name,
                'exact': False,
                'similarity': fuzzy_item['similarity']
            })
    
    # Build line result
    line_data = {
        'text': result.line,
        'pattern': lg_pattern,
        'syllables': result.syllables,
        'syllable_count': result.length,
        'meters': meters,
        'exact_match': result.found
    }
    
    return AnalysisResult(
        input_text=text,
        input_scheme=result.scheme,  # Use detected scheme
        success=True,
        lines=[line_data],
        timestamp=datetime.now()
    )
```

---

## Risk Assessment

**Risk Level:** 🔴 **CRITICAL**

**Why:**
- Core functionality completely broken
- Cannot perform any meter analysis
- All Phase 3 integration work is blocked
- Phase 4 color visualization untestable

**Mitigation:**
- Fix API integration immediately (this session)
- Add comprehensive error handling
- Create test suite before continuing
- Document actual Chanda API for future reference

---

## Lessons Learned

1. **Always verify library API before coding against it**
   - We assumed API structure without testing
   - Should have run `help(Chanda)` first
   
2. **Test incrementally as you build**
   - We built entire controller without testing against real library
   - Should have tested after each method
   
3. **Read library documentation thoroughly**
   - Chanda has specific return types (ChandaResult dataclass)
   - Need to understand these before designing wrapper

4. **Auto-detection vs. Manual Input**
   - Chanda auto-detects transliteration schemes
   - Our manual selector may be redundant (or add confusion)

---

## Next Steps

1. **Immediate:** Fix `analysis_controller.py` (Tasks 1.1-1.3)
2. **Verify:** Run test with sample text
3. **Validate:** Check color display works with corrected data
4. **Document:** Update code comments with correct API usage
5. **Test:** Run through all end-user scenarios

**Estimated Time:** 1-2 hours for core fixes + testing

---

## Questions for User

1. **Meter Names:** Display in Devanagari (authentic) or add romanization mapping?
2. **Script Selector:** Keep for guidance or remove (since auto-detected)?
3. **Error Messages:** How verbose should error messages be for end users?
4. **Fuzzy Threshold:** Should we expose similarity threshold control in UI?

---

**Status:** Ready for implementation  
**Assigned To:** Development team  
**Priority:** P0 - Critical

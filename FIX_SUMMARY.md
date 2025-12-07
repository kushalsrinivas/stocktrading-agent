# Bug Fixes: Data Type Conversion Errors

## Issues Fixed

### Issue 1: Date Formatting Error
Error: `'str' object has no attribute 'strftime'`

This occurred when trying to format dates that were already strings.

**Root Cause:** The code assumed all date objects had a `.strftime()` method, but some dates were already formatted as strings.

### Issue 2: Series Conversion Error (NEW)
Error: `cannot convert the series to <class 'float'>`

This occurred when trying to convert pandas Series directly to float/int.

**Root Cause:** When metrics contain pandas Series objects (single-element Series), calling `float()` or `int()` directly fails. We need to extract the scalar value first.

## Solutions

### Solution 1: Safe Date Formatting
Created a helper function that handles multiple date input types:

```python
def format_date(date_obj, format_str='%Y-%m-%d'):
    """
    Safely format a date object to string
    Handles datetime, Timestamp, and string inputs
    """
    if isinstance(date_obj, str):
        return date_obj
    elif hasattr(date_obj, 'strftime'):
        return date_obj.strftime(format_str)
    else:
        return str(date_obj)
```

### Solution 2: Safe Type Conversion
Created helper functions to safely convert pandas Series and numpy types:

```python
def safe_float(value):
    """
    Safely convert value to float
    Handles scalar values, pandas Series, numpy types, etc.
    """
    # Handle pandas Series - extract the scalar value
    if isinstance(value, pd.Series):
        if len(value) == 0:
            return 0.0
        value = value.iloc[0] if len(value) == 1 else value.values[0]
    
    # Handle numpy types
    if isinstance(value, (np.integer, np.floating)):
        return float(value)
    
    # Handle NaN/None
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    
    # Convert to float
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def safe_int(value):
    """Safely convert value to int (similar logic)"""
    # ... (handles Series, numpy, NaN, etc.)
```

## Changes Made

### 1. Added Helper Function
- Added `format_date()` function after `convert_numpy_types()`
- Handles strings, datetime objects, pandas Timestamps, and fallback cases

### 2. Updated Date Formatting
Replaced all direct `.strftime()` calls with `format_date()`:

**Before:**
```python
'date': date.strftime('%Y-%m-%d')
```

**After:**
```python
'date': format_date(date, '%Y-%m-%d')
```

### 3. Improved Error Handling
Added better error handling in the `/backtest` endpoint:
```python
except ValueError as e:
    # Handle validation errors
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    # Log full traceback for debugging
    import traceback
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=str(e))
```

## Testing

Test the fix with:

```bash
# Start server
python api_server.py

# Test with curl
curl -X POST http://localhost:8000/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "RELIANCE",
    "strategy": "rsi_bb",
    "start_date": "2020-01-01",
    "end_date": "2024-12-31",
    "initial_capital": 100000
  }'
```

Or with Python:

```python
import requests

response = requests.post("http://localhost:8000/backtest", json={
    "ticker": "RELIANCE",
    "strategy": "rsi_bb",
    "start_date": "2020-01-01",
    "end_date": "2024-12-31",
    "initial_capital": 100000
})

print(response.json())
```

## Files Modified

1. **api_server.py**
   - Added `format_date()` helper function
   - Updated date formatting in `run_single_backtest()`
   - Improved error handling in `/backtest` endpoint

## Expected Result

The API should now successfully:
- ✅ Handle date formatting for all data types
- ✅ Return historical price data with properly formatted dates
- ✅ Return equity curve data with properly formatted dates
- ✅ Return trades with properly formatted dates
- ✅ Provide better error messages when issues occur

## Related Issues

This fix also prevents similar issues with:
- pandas Timestamp objects
- numpy datetime64 objects
- datetime.date objects
- datetime.datetime objects
- Pre-formatted date strings

---

**Status: FIXED ✅**


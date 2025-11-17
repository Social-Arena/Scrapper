# Scrapper Trace Logs

This directory contains all runtime logs for the Scrapper system. **NO logs are output to console** - everything is written to files for proper debugging and analysis.

## Directory Structure

```
trace/
├── scrapers/          # Platform-specific scraper logs
│   ├── twitter.log
│   ├── tiktok.log
│   ├── xiaohongshu.log
│   ├── youtube.log
│   └── general.log
├── processing/        # Data processing logs
│   ├── normalizer.log
│   ├── trend_detector.log
│   ├── sentiment_analyzer.log
│   └── general.log
├── feeds/             # Feed system logs
│   ├── aggregator.log
│   ├── enricher.log
│   └── general.log
├── storage/           # Storage operation logs
│   ├── raw_data.log
│   ├── cache.log
│   └── general.log
├── monitoring/        # System monitoring logs
│   ├── scraping.log
│   ├── rate_limiter.log
│   ├── health.log
│   └── general.log
├── errors/            # Error and exception logs
│   ├── errors.log
│   └── exceptions.log
├── performance/       # Performance metrics
│   ├── metrics.log
│   └── benchmark.log
└── main.log          # Main application log
```

## Log Levels

- **DEBUG**: Detailed diagnostic information (API calls, data transformations, etc.)
- **INFO**: General informational messages (operation started/completed, data counts, etc.)
- **WARNING**: Warning messages (rate limits approaching, retries, etc.)
- **ERROR**: Error messages (API failures, data processing errors, etc.)
- **CRITICAL**: Critical errors that may cause system failure

## Log Format

### Standard Format
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [ComponentName] [filename.py:line] - Message
```

Example:
```
[2025-11-16 10:30:45] [INFO] [TwitterScraper] [twitter_scraper.py:123] - Starting to scrape trending topics
[2025-11-16 10:30:47] [DEBUG] [TwitterScraper] [twitter_scraper.py:145] - API call: GET /trends/place.json
[2025-11-16 10:30:48] [INFO] [TwitterScraper] [twitter_scraper.py:167] - Scraped 50 trending topics
[2025-11-16 10:30:50] [ERROR] [TwitterScraper] [twitter_scraper.py:189] - Rate limit exceeded
```

### JSON Format (Optional)
For machine-readable logs, JSON format includes structured data:
```json
{
  "timestamp": "2025-11-16 10:30:45",
  "level": "INFO",
  "logger": "TwitterScraper",
  "module": "twitter_scraper",
  "function": "scrape_trending_topics",
  "line": 123,
  "message": "Starting to scrape trending topics",
  "extra": {
    "location": "global",
    "max_results": 50
  }
}
```

## Log Rotation

Logs are automatically rotated to prevent disk space issues:
- **Max file size**: 10 MB per log file
- **Backup count**: 5 backup files kept
- **Naming**: `logname.log`, `logname.log.1`, `logname.log.2`, etc.

## Debugging Workflow

### 1. Identify the Component
First, determine which component is involved in the issue:
- Scraping issues → Check `scrapers/` directory
- Data processing issues → Check `processing/` directory
- Feed aggregation issues → Check `feeds/` directory
- Storage issues → Check `storage/` directory
- Performance issues → Check `performance/` directory

### 2. Check Error Logs First
Always start with the error logs:
```bash
# View recent errors
tail -n 100 trace/errors/errors.log

# Search for specific error
grep "RateLimitError" trace/errors/errors.log

# View exceptions with full tracebacks
tail -n 200 trace/errors/exceptions.log
```

### 3. Trace the Flow
Follow the execution flow across different components:

```bash
# Example: Debugging a Twitter scraping issue

# 1. Check scraper logs
tail -n 200 trace/scrapers/twitter.log

# 2. Check if data was normalized
tail -n 100 trace/processing/normalizer.log | grep "twitter"

# 3. Check if feeds were created
tail -n 100 trace/feeds/aggregator.log

# 4. Check storage operations
tail -n 100 trace/storage/raw_data.log
```

### 4. Check Performance Metrics
If the issue is performance-related:
```bash
# View performance metrics
tail -n 100 trace/performance/metrics.log

# Look for slow operations
grep "elapsed:" trace/performance/metrics.log | sort -t: -k4 -nr

# Check benchmarks
tail -n 50 trace/performance/benchmark.log
```

### 5. Monitor Rate Limiting
For API rate limit issues:
```bash
# Check rate limiter logs
tail -n 100 trace/monitoring/rate_limiter.log

# Check scraping monitor
tail -n 100 trace/monitoring/scraping.log
```

## Common Debugging Scenarios

### Scenario 1: Scraper Not Returning Data
```bash
# Step 1: Check scraper logs for the platform
tail -n 200 trace/scrapers/twitter.log

# Step 2: Look for API errors
grep -i "error\|fail" trace/scrapers/twitter.log

# Step 3: Check rate limiting
tail -n 50 trace/monitoring/rate_limiter.log | grep "twitter"

# Step 4: Check errors log
grep "TwitterScraper" trace/errors/errors.log
```

### Scenario 2: Data Processing Failure
```bash
# Step 1: Check what data was received
tail -n 100 trace/scrapers/general.log

# Step 2: Check normalizer logs
tail -n 200 trace/processing/normalizer.log

# Step 3: Look for validation errors
grep "validation\|invalid" trace/processing/*.log

# Step 4: Check exception details
tail -n 100 trace/errors/exceptions.log
```

### Scenario 3: Performance Degradation
```bash
# Step 1: Check performance metrics
tail -n 200 trace/performance/metrics.log

# Step 2: Find slowest operations
grep "Operation completed" trace/performance/metrics.log | \
  awk '{print $NF}' | sort -nr | head -20

# Step 3: Check if it's I/O related
tail -n 100 trace/storage/*.log

# Step 4: Check memory/resource issues
tail -n 100 trace/monitoring/health.log
```

### Scenario 4: Trend Detection Issues
```bash
# Step 1: Check trend detector logs
tail -n 200 trace/processing/trend_detector.log

# Step 2: Check input data quality
grep "data_quality" trace/monitoring/scraping.log

# Step 3: Check sentiment analyzer if relevant
tail -n 100 trace/processing/sentiment_analyzer.log
```

## Analyzing Logs with Common Tools

### Using grep for pattern matching
```bash
# Find all errors from a specific timeframe
grep "2025-11-16 10:3" trace/**/*.log | grep ERROR

# Find all logs related to a specific user or content ID
grep "user_id: 12345" trace/**/*.log

# Case-insensitive search
grep -i "rate limit" trace/**/*.log
```

### Using tail for real-time monitoring
```bash
# Watch logs in real-time
tail -f trace/main.log

# Watch multiple logs simultaneously
tail -f trace/scrapers/twitter.log trace/processing/normalizer.log

# Watch with filtering
tail -f trace/main.log | grep ERROR
```

### Using awk for data extraction
```bash
# Extract only timestamps and messages
awk -F' - ' '{print $1, $2}' trace/scrapers/twitter.log

# Count errors by type
grep ERROR trace/errors/errors.log | \
  awk -F': ' '{print $2}' | sort | uniq -c

# Average operation duration
grep "Operation completed" trace/performance/metrics.log | \
  awk '{print $NF}' | sed 's/s)//' | \
  awk '{sum+=$1; count++} END {print sum/count}'
```

### Using jq for JSON logs (if enabled)
```bash
# Parse JSON logs
cat trace/scrapers/twitter.log | jq '.'

# Filter by level
cat trace/main.log | jq 'select(.level=="ERROR")'

# Extract specific fields
cat trace/performance/metrics.log | jq '{operation: .extra.operation, duration: .extra.elapsed_seconds}'
```

## Log Retention and Cleanup

Logs older than 7 days are automatically cleaned up. To manually clean up logs:

```python
from scrapper.utils.logger import cleanup_old_logs

# Clean up logs older than 7 days
cleanup_old_logs(days_to_keep=7)

# Clean up logs older than 30 days
cleanup_old_logs(days_to_keep=30)
```

## Best Practices for Debugging

1. **Start with the timestamp**: Use the user's reported timestamp to narrow down logs
2. **Check errors first**: Always review `errors/errors.log` and `errors/exceptions.log` first
3. **Follow the data flow**: Trace from scraper → processing → feeds → storage
4. **Check context**: Look at logs before and after the error for context
5. **Use performance logs**: Identify bottlenecks using `performance/metrics.log`
6. **Cross-reference**: Compare logs across different components for the same operation
7. **Look for patterns**: Use grep and awk to identify recurring issues

## Programmatic Log Analysis

For complex debugging, you can write scripts to analyze logs:

```python
from pathlib import Path
import re
from datetime import datetime

def analyze_error_frequency(log_file: Path, time_window_hours: int = 24):
    """Analyze error frequency in the last N hours."""
    errors = []
    cutoff_time = datetime.now() - timedelta(hours=time_window_hours)

    with open(log_file, 'r') as f:
        for line in f:
            if 'ERROR' in line:
                # Extract timestamp and error type
                match = re.match(r'\[(.*?)\].*ERROR.*?(\w+Error)', line)
                if match:
                    timestamp_str, error_type = match.groups()
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    if timestamp >= cutoff_time:
                        errors.append((timestamp, error_type))

    # Count by error type
    from collections import Counter
    error_counts = Counter(error_type for _, error_type in errors)

    return error_counts

# Usage
error_counts = analyze_error_frequency(Path('trace/errors/errors.log'))
print(f"Errors in last 24 hours: {error_counts}")
```

## Tips for Effective Logging

When adding new features, ensure you:
1. Log at appropriate levels (DEBUG for details, INFO for flow, ERROR for failures)
2. Include relevant context (user_id, content_id, platform, etc.)
3. Use structured logging for machine-readable data
4. Log performance metrics for slow operations
5. Log API calls with parameters for debugging
6. Always log exceptions with full tracebacks

## Support

If you need help debugging an issue:
1. Identify the approximate timestamp of the issue
2. Collect relevant log files from the trace/ directory
3. Note any error messages or unexpected behavior
4. Use the debugging workflows above to narrow down the issue
5. Review the exception logs for stack traces

Remember: **All logs are in files, no console output**. This ensures you can always review what happened, even after the fact.

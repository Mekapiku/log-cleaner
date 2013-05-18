# Log Cleaner
## usage
```python
def parse_date(log):
    try:
        # YYYYMMDD
        date = datetime.datetime(int(log[0:4]), int(log[4:6]), int(log[6:8]))
        return date

    except ValueError:
        return None

day_count = 10
logs_max = 50

pattern =  re.compile(r'^[0-9]{8}.*$')
log_cleaner = LogCleaner("target_dir")

# clean logs
log_cleaner.clean(pattern, parse_date, day_count, logs_max)
```

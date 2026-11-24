```text
2026-11-24 09:12:03 INFO  request_id=7f31 action=overdue due=2026-11-20
2026-11-24 09:12:03 ERROR request_id=7f31 ValueError: time data '2026-11-20' does not match format '%d.%m.%Y'
Traceback (most recent call last):
  File "app.py", line 18, in <module>
    print(row["id"], days_overdue(row["due"]))
  File "app.py", line 12, in days_overdue
    return (today - parse_due(due)).days
  File "app.py", line 8, in parse_due
    return datetime.strptime(value, "%d.%m.%Y").date()
ValueError: time data '2026-11-20' does not match format '%d.%m.%Y'

2026-11-24 09:12:03 INFO  request_id=7f31 action=fallback result=0
2026-11-24 09:12:04 INFO  request_id=8a02 action=overdue due=2026-11-22
2026-11-24 09:12:04 ERROR request_id=8a02 ValueError: time data '2026-11-22' does not match format '%d.%m.%Y'
2026-11-24 09:12:04 INFO  request_id=8a02 action=fallback result=0
2026-11-24 09:13:10 INFO  request_id=9c14 action=list status=open count=3
`
```

---
name: deduplicate
track: bonus
kind: local_formatter
requires_env: []
inputs: [items]
outputs: [items, removed_count]
side_effect: false
---

Keeps the first item for each exactly matching, non-empty URL in input order.
Items with missing/empty URLs are preserved. URLs are not normalized; tracking
parameters are not removed. Invalid list/item/URL types return invalid_input.
No network access, file writes or confirmation required.

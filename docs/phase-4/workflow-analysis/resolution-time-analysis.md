# PR resolution-time distribution

WF-MET-009 measures elapsed UTC hours between PR creation and merge/closure, coded in the frozen JSONL. A separate read-only candidate-frame audit cross-checked all 27 coded durations against UTC timestamps within 0.11 hour for rounding. Eligible denominator is terminal PRs with both timestamps; **20/20 base** and, separately, **7/7 purposive discussion** qualify. Quartiles use linear interpolation at positions `(n-1) × p` on sorted values; IQR is Q3−Q1.

| Base segment | N | Min | Q1 | Median | Q3 | Max | IQR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All terminal base PRs | 20 | 0.0 | 136.3 | 167.25 | 744.0 | 5823.4 | 607.7 |
| Merged | 9 | 0.0 | 11.9 | 136.3 | 140.0 | 5823.4 | 128.1 |
| Closed without merge | 11 | 136.4 | 167.25 | 334.6 | 1050.25 | 2032.5 | 883.0 |
| Visible human interaction | 6 | 11.9 | 104.2 | 136.3 | 139.07 | 2032.5 | 34.87 |
| No visible interaction | 14 | 0.0 | 157.12 | 308.25 | 744.0 | 5823.4 | 586.88 |
| At least one coded exception | 12 | 11.9 | 163.58 | 333.65 | 897.12 | 2032.5 | 733.54 |
| No coded exception | 8 | 0.0 | 72.05 | 136.3 | 175.95 | 5823.4 | 103.9 |

The discussion sample separately has N=7, min 0.8, Q1 0.85, median 139.4, Q3 2032.45, max 2032.5 and IQR 2031.6 hours; its deliberate interaction selection precludes rate comparison. The base distribution has a long upper tail ([statys#39](https://github.com/gugarosa/statys/pull/39) at 5823.4 hours). Segment medians are **descriptive associations** in a small, repository-clustered sample and do not identify delay causes. Zero elapsed hours is a rounded valid recorded interval, not instantaneous human work. None of these durations is engineering time, productivity or time saved.

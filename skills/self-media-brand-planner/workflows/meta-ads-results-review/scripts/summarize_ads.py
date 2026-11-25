#!/usr/bin/env python3
"""Check one explicitly normalized, same-period ad-level comparison group."""
import csv
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

CONTEXT = ('date_start', 'date_stop', 'currency', 'timezone', 'objective',
           'attribution_setting', 'lead_event')
NUMBERS = ('spend', 'impressions', 'link_clicks', 'meta_leads')
REQUIRED = ('ad_id',) + CONTEXT + NUMBERS
UNKNOWN = {'tbc', 'unknown', 'none', 'n/a'}


def number(value, field):
    value = value.strip()
    if not value:
        return None
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f'{field}: invalid number') from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f'{field}: expected finite non-negative number')
    return result


def summarize(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError('missing or duplicate headers')
        missing = set(REQUIRED) - set(reader.fieldnames)
        if missing:
            raise ValueError('missing columns: ' + ', '.join(sorted(missing)))
        rows = list(reader)
    if not rows:
        return {'status': 'no_data', 'row_count': 0, 'totals': None, 'metrics': None}
    seen, context, values = set(), None, []
    for row in rows:
        if None in row or any(row.get(key) is None for key in REQUIRED):
            raise ValueError('malformed row')
        ad_id = row['ad_id'].strip()
        if not ad_id or ad_id in seen:
            raise ValueError('missing or duplicate ad_id; normalize report grain first')
        seen.add(ad_id)
        current = {key: row[key].strip() for key in CONTEXT}
        if any(not v for v in current.values()):
            raise ValueError('blank context; use TBC for unknown metadata')
        if date.fromisoformat(current['date_start']) > date.fromisoformat(current['date_stop']):
            raise ValueError('reversed date range')
        if context is not None and current != context:
            raise ValueError('mixed comparison context; split groups first')
        context = current
        values.append({key: number(row[key], key) for key in NUMBERS})
    totals = {}
    for key in NUMBERS:
        parts = [row[key] for row in values]
        totals[key] = None if any(v is None for v in parts) else sum(parts, Decimal(0))

    def ratio(numerator, denominator, scale=1):
        n, d = totals[numerator], totals[denominator]
        return None if n is None or d is None or d == 0 else n / d * scale

    unknown = [key for key, value in context.items() if value.lower() in UNKNOWN]
    return {
        'status': 'needs_review' if unknown else 'calculated',
        'row_count': len(rows), 'context': context, 'unknown_context': unknown,
        'missing_metrics': [key for key in NUMBERS if totals[key] is None],
        'totals': totals,
        'metrics': {'link_ctr_percent': ratio('link_clicks', 'impressions', 100),
                    'link_cpc': ratio('spend', 'link_clicks'),
                    'meta_cpl': ratio('spend', 'meta_leads')},
        'scope': 'arithmetic_only; mapping, completeness and attribution require review'
    }


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('usage: summarize_ads.py normalized.csv')
        print(json.dumps(summarize(sys.argv[1]), ensure_ascii=False, indent=2,
                         default=lambda value: str(value) if isinstance(value, Decimal) else value))
    except (ValueError, OSError, csv.Error) as exc:
        print(json.dumps({'status': 'invalid_input', 'error': str(exc)}, ensure_ascii=False))
        sys.exit(2)

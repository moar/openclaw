from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    root = Path(__file__).resolve().parent
    load_env(root / '.env')

    api_key = os.environ.get('GOOGLE_API_KEY')
    cse_id = os.environ.get('GOOGLE_CSE_ID')
    query = ' '.join(sys.argv[1:]).strip() or 'Portugal technology magazine site:.pt'

    if not api_key or not cse_id:
        print('Missing GOOGLE_API_KEY or GOOGLE_CSE_ID', file=sys.stderr)
        return 2

    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': 10,
    }
    url = 'https://www.googleapis.com/customsearch/v1?' + urlencode(params)
    try:
        with urlopen(url, timeout=20) as resp:
            data = json.load(resp)
    except Exception as exc:
        if hasattr(exc, 'read'):
            try:
                raw = exc.read().decode('utf-8', errors='replace')
            except Exception:
                raw = str(exc)
            print(raw)
        else:
            print(str(exc))
        return 1

    print(json.dumps({
        'query': query,
        'searchInformation': data.get('searchInformation', {}),
        'items': [
            {
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet'),
            }
            for item in data.get('items', [])
        ],
        'error': data.get('error'),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

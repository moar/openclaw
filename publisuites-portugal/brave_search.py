from __future__ import annotations

import gzip
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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
    api_key = os.environ.get('BRAVE_API_KEY')
    query = ' '.join(sys.argv[1:]).strip() or 'Portugal technology magazine site:.pt'
    if not api_key:
        print('Missing BRAVE_API_KEY', file=sys.stderr)
        return 2

    params = {
        'q': query,
        'count': 10,
        'search_lang': 'en',
        'country': 'pt',
    }
    url = 'https://api.search.brave.com/res/v1/web/search?' + urlencode(params)
    req = Request(url, headers={
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': api_key,
    })
    try:
        with urlopen(req, timeout=20) as resp:
            raw = resp.read()
            if resp.headers.get('Content-Encoding', '').lower() == 'gzip':
                raw = gzip.decompress(raw)
            data = json.loads(raw.decode('utf-8'))
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

    results = []
    for item in data.get('web', {}).get('results', []):
        results.append({
            'title': item.get('title'),
            'url': item.get('url'),
            'description': item.get('description'),
        })

    print(json.dumps({
        'query': query,
        'results': results,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

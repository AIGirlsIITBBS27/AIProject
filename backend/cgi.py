# Temporary shim for Python 3.13
import urllib.parse as _u

def parse_header(value):
    # googletrans expects parse_header() from cgi
    parts = value.split(';', 1)
    key = parts[0].strip().lower()
    pdict = {}
    if len(parts) == 2:
        pdict = dict(
            (k.strip().lower(), v.strip())
            for k, v in [p.split('=', 1) for p in parts[1].split(';') if '=' in p]
        )
    return key, pdict

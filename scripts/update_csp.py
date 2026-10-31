#!/usr/bin/env python3
"""Keep each dashboard's Content-Security-Policy in step with its inline code.

  python3 scripts/update_csp.py          add or refresh the policy in every page
  python3 scripts/update_csp.py --check  fail if a policy is missing or stale (CI)

A page's scripts stop running if their hash is not in its policy, so run this
after editing any inline <script>, which includes adding to DASHBOARDS.
"""
import base64
import hashlib
import pathlib
import re
import sys

DASHBOARDS = pathlib.Path(__file__).resolve().parent.parent / 'dashboards'

META = '<meta http-equiv="Content-Security-Policy" content="{}">\n'
META_RE = re.compile(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)">\n')
CHARSET_RE = re.compile(r'<meta charset[^>]*>\n', re.I)
SCRIPT_RE = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S)
STYLE_RE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.S)

# Starting policy for a page. Styles stay inline-friendly because most pages use
# style="..." attributes; the blocked network directives keep that low risk.
DEFAULT = ("default-src 'none'; script-src 'none'; style-src 'unsafe-inline'; "
           "img-src 'none'; font-src 'none'; connect-src 'none'; base-uri 'none'; "
           "form-action 'none'; object-src 'none'")

# The rule index.html adds to embedded pages. Only hash-based style-src needs it.
EMBED_STYLE = '#themes{display:none!important}'


def digest(text):
    sha = hashlib.sha256(text.encode('utf-8')).digest()
    return "'sha256-" + base64.b64encode(sha).decode() + "'"


def policy(html, current):
    csp = current or DEFAULT
    if not current and '<iframe' in html:
        csp += "; frame-src 'self'"
    scripts = ' '.join(digest(s) for s in SCRIPT_RE.findall(html)) or "'none'"
    csp = re.sub(r'script-src [^;]*', lambda _: 'script-src ' + scripts, csp)
    if "style-src 'sha256-" in csp:
        styles = ' '.join(digest(s) for s in STYLE_RE.findall(html) + [EMBED_STYLE])
        csp = re.sub(r'style-src [^;]*', lambda _: 'style-src ' + styles, csp)
    return csp


def updated(html):
    found = META_RE.search(html)
    if found:
        meta = META.format(policy(html, found.group(1)))
        return html[:found.start()] + meta + html[found.end():]
    charset = CHARSET_RE.search(html)
    if not charset:
        raise SystemExit('no <meta charset> to put the policy after')
    return html[:charset.end()] + META.format(policy(html, None)) + html[charset.end():]


def main():
    check = '--check' in sys.argv[1:]
    stale = []
    for path in sorted(DASHBOARDS.rglob('*.html')):
        html = path.read_text(encoding='utf-8')
        new = updated(html)
        if new != html:
            stale.append(path.relative_to(DASHBOARDS.parent))
            if not check:
                path.write_text(new, encoding='utf-8')
    for path in stale:
        print(f'{"stale" if check else "updated"}: {path}')
    if check and stale:
        print('Run python3 scripts/update_csp.py and commit the result.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

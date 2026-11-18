#!/usr/bin/env python3
"""Assemble the whole Learning Lab website in public/.

  python3 scripts/build_site.py                          download topic repos and build
  python3 scripts/build_site.py --local oracle=../learn-oracle
                                                         use a local folder for a topic instead

Steps:
1. Copy dashboards/ to public/.
2. For each topic repo in topics.json, copy its pages into public/<folder>/.
3. Add each topic's pages.json entries to the menu (DASHBOARDS) in public/index.html.
4. Refresh public/index.html's security policy, because step 3 changed its script.
5. Fail if any topic page's own security policy is stale, as the hub's check does.

Uses only the Python standard library and git.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import update_csp  # noqa: E402

PUBLIC = ROOT / 'public'
SKIP = {'.git', '.gitlab-ci.yml', '.gitignore', 'README.md', 'pages.json'}
ANCHOR = 'const DASHBOARDS = [\n'


def fetch(topic, local, work):
    """Return a folder holding the topic repo's files."""
    if topic['folder'] in local:
        return pathlib.Path(local[topic['folder']]).resolve()
    dest = work / topic['folder']
    subprocess.run(['git', 'clone', '--quiet', '--depth', '1', '--branch', topic.get('branch', 'main'),
                    topic['repo'], str(dest)], check=True)
    return dest


def main():
    local = dict(a.split('=', 1) for a in sys.argv[sys.argv.index('--local') + 1:]) if '--local' in sys.argv else {}
    topics = json.loads((ROOT / 'topics.json').read_text(encoding='utf-8'))

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    shutil.copytree(ROOT / 'dashboards', PUBLIC)

    entries, stale = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for topic in topics:
            src = fetch(topic, local, pathlib.Path(tmp))
            dest = PUBLIC / topic['folder']
            if dest.exists():
                raise SystemExit(f'{dest.relative_to(ROOT)} already exists in dashboards/; a topic repo owns it.')
            shutil.copytree(src, dest, ignore=lambda d, names: [n for n in names if n in SKIP or n == '.DS_Store'])
            for page in json.loads((src / 'pages.json').read_text(encoding='utf-8')):
                page['href'] = f"{topic['folder']}/{page['href']}"
                if not (PUBLIC / page['href']).is_file():
                    raise SystemExit(f"pages.json in {topic['folder']} lists a missing file: {page['href']}")
                entries.append(page)
            for path in sorted(dest.rglob('*.html')):
                html = path.read_text(encoding='utf-8')
                if update_csp.updated(html) != html:
                    stale.append(str(path.relative_to(PUBLIC)))
            print(f"added {topic['folder']}/ from {topic['repo'] if topic['folder'] not in local else src}")

    if stale:
        print('Stale security policy in a topic repo (run update_csp.py --root . there):')
        print('\n'.join('  ' + s for s in stale))
        return 1

    index = PUBLIC / 'index.html'
    html = index.read_text(encoding='utf-8')
    if html.count(ANCHOR) != 1:
        raise SystemExit('Could not find the DASHBOARDS list in index.html')
    block = ''.join('  ' + json.dumps(e, ensure_ascii=False) + ',\n' for e in entries)
    html = html.replace(ANCHOR, ANCHOR + block)
    index.write_text(update_csp.updated(html), encoding='utf-8')
    print(f'menu: {len(entries)} topic-repo pages added to index.html')
    return 0


if __name__ == '__main__':
    sys.exit(main())

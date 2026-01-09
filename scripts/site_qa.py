import os
from html.parser import HTMLParser
import json

SITE_ROOT = os.path.join(r"c:\Users\Jacob Jayme\iron-legacy", "_site")

class LinkImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []
        self.images = []
        self.lang_attr = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            href = attrs.get('href')
            if href:
                self.anchors.append({'href': href, 'attrs': attrs})
        if tag == 'img':
            src = attrs.get('src')
            if src:
                self.images.append(src)
        if tag == 'html' and self.lang_attr is None:
            self.lang_attr = attrs.get('lang')


def resolve_path(current_file, link):
    if link.startswith('mailto:') or link.startswith('tel:'):
        return None
    if link.startswith('#'):
        return None
    if link.startswith('http://') or link.startswith('https://'):
        return None
    link_clean = link.split('?')[0].split('#')[0]
    if link_clean.startswith('/'):
        candidate = os.path.join(SITE_ROOT, link_clean.lstrip('/'))
    else:
        candidate = os.path.join(os.path.dirname(current_file), link_clean)
    # Directory
    if os.path.isdir(candidate):
        candidate_index = os.path.join(candidate, 'index.html')
        return candidate_index if os.path.exists(candidate_index) else None
    if os.path.exists(candidate):
        return candidate
    if link_clean.endswith('/'):
        candidate_index = candidate + 'index.html'
        if os.path.exists(candidate_index):
            return candidate_index
    candidate_index = candidate + os.sep + 'index.html'
    if os.path.exists(candidate_index):
        return candidate_index
    if not os.path.splitext(candidate)[1]:
        if os.path.exists(candidate + '.html'):
            return candidate + '.html'
    return None

issues = {
    'broken_internal_links': [],
    'missing_images': [],
    'lang_mismatch': [],
    'language_toggle_issues': [],
    'menu_external_prefix_errors': [],
    'missing_hamburger_or_toggle': [],
}
js_issues = []

for root, dirs, files in os.walk(SITE_ROOT):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        relurl = os.path.relpath(path, SITE_ROOT)
        with open(path, 'r', encoding='utf-8') as fh:
            data = fh.read()
        parser = LinkImgParser()
        parser.feed(data)

        # Lang checks
        if os.path.normpath(root).startswith(os.path.normpath(os.path.join(SITE_ROOT, 'es'))):
            if parser.lang_attr != 'es':
                issues['lang_mismatch'].append({'file': relurl, 'found': parser.lang_attr, 'expected': 'es'})
        else:
            if parser.lang_attr and parser.lang_attr != 'en':
                issues['lang_mismatch'].append({'file': relurl, 'found': parser.lang_attr, 'expected': 'en'})

        # anchors
        for a in parser.anchors:
            href = a['href']
            if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            if href.startswith('http://') or href.startswith('https://'):
                if '/es/http' in href or '/es/https' in href:
                    issues['menu_external_prefix_errors'].append({'file': relurl, 'href': href})
                continue
            resolved = resolve_path(path, href)
            if resolved is None:
                issues['broken_internal_links'].append({'file': relurl, 'href': href})

        # images
        for img in parser.images:
            if img.startswith('http://') or img.startswith('https://') or img.startswith('data:'):
                continue
            resolved = resolve_path(path, img)
            if resolved is None:
                issues['missing_images'].append({'file': relurl, 'src': img})

        # language toggle checks
        if 'class="language-toggle"' not in data and 'id="language-toggle-button"' not in data:
            issues['missing_hamburger_or_toggle'].append({'file': relurl, 'reason': 'no language toggle found'})
        else:
            # find anchor with id language-toggle-button
            idx = data.find('id="language-toggle-button"')
            if idx != -1:
                # naive parse for href and data-target-lang
                snippet = data[idx-200:idx+200]
                ht = None
                dt = None
                # find href="..."
                import re
                m = re.search(r'href="([^"]+)"', snippet)
                if m:
                    ht = m.group(1)
                m2 = re.search(r'data-target-lang="([^"]+)"', snippet)
                if m2:
                    dt = m2.group(1)
                page_lang = 'es' if os.path.normpath(root).startswith(os.path.normpath(os.path.join(SITE_ROOT, 'es'))) else 'en'
                expected = 'es' if page_lang == 'en' else 'en'
                if dt and dt != expected:
                    issues['language_toggle_issues'].append({'file': relurl, 'found_target': dt, 'expected_target': expected})
                if ht:
                    if not (ht.startswith('http') or ht.startswith('#')):
                        if resolve_path(path, ht) is None:
                            issues['language_toggle_issues'].append({'file': relurl, 'href': ht})

# js scan
ASSETS_JS = os.path.join(r"c:\Users\Jacob Jayme\iron-legacy", 'assets', 'js')
for root, dirs, files in os.walk(ASSETS_JS):
    for f in files:
        if f.endswith('.js'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                txt = fh.read()
            if 'audioElement.play' in txt:
                js_issues.append({'file': os.path.relpath(p, SITE_ROOT), 'pattern': 'audioElement.play'})

report = { 'summary': {k: len(v) for k,v in issues.items()}, 'details': issues, 'js_issues': js_issues }
print(json.dumps(report, indent=2))

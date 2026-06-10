#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime, timezone

FEED_URL = 'https://library.caltech.edu/blogs/rss.xml?blogConfigId=1449'
ATOM_NS = 'http://www.w3.org/2005/Atom'

def t(name):
    return f'{{{ATOM_NS}}}{name}'

def strip_html(html):
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def first_image(html):
    if not html:
        return None
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    return m.group(1) if m else None

def make_excerpt(text, max_len=200):
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rfind(' ')
    return text[:cut if cut > 0 else max_len] + '...'

req = urllib.request.Request(
    FEED_URL,
    headers={'User-Agent': 'ContentBuddy/1.0 (Caltech Library)'}
)
with urllib.request.urlopen(req) as resp:
    xml_data = resp.read().decode('utf-8')

root = ET.fromstring(xml_data)

posts = []
for entry in root.findall(t('entry')):
    raw_id = entry.findtext(t('id'), '').strip()
    uuid = raw_id.replace('urn:uuid:', '')

    title = entry.findtext(t('title'), '').strip()
    date = entry.findtext(t('updated'), '').strip()

    author_el = entry.find(t('author'))
    author = author_el.findtext(t('name'), '').strip() if author_el is not None else ''

    link_el = entry.find(t('link'))
    link = link_el.get('href', '').strip() if link_el is not None else ''

    content_el = entry.find(t('content'))
    content_html = (content_el.text or '') if content_el is not None else ''

    image = first_image(content_html)
    excerpt = make_excerpt(strip_html(content_html))

    posts.append({
        'id': uuid,
        'title': title,
        'date': date,
        'author': author,
        'link': link,
        'image': image,
        'excerpt': excerpt,
    })

out = {
    'updated': datetime.now(timezone.utc).isoformat(),
    'posts': posts,
}

with open('posts.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f'Wrote {len(posts)} posts to posts.json')

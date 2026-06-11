#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import os
import shutil
import html
from datetime import datetime, timezone

FEED_URL = 'https://library.caltech.edu/blogs/rss.xml?blogConfigId=1449'
ATOM_NS = 'http://www.w3.org/2005/Atom'

def t(name):
    return f'{{{ATOM_NS}}}{name}'

def strip_html(raw):
    if not raw:
        return ''
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def first_image(raw):
    if not raw:
        return None
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', raw)
    return m.group(1) if m else None

def make_excerpt(text, max_len=200):
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rfind(' ')
    return text[:cut if cut > 0 else max_len] + '...'

def format_date(date_str):
    try:
        d = datetime.fromisoformat(date_str)
        return d.strftime(f'%B {d.day}, %Y')
    except Exception:
        return ''

def make_post_html(post):
    title     = html.escape(post['title'])
    excerpt   = html.escape(post['excerpt']) if post['excerpt'] else ''
    image     = post['image'] or ''
    link      = html.escape(post['link']) if post['link'] else ''
    meta_parts = [x for x in [html.escape(post['author']), format_date(post['date'])] if x]
    meta      = ' · '.join(meta_parts)

    img_html      = f'<img class="post-image" src="{html.escape(image)}" alt="">' if image else '<div class="placeholder-img"></div>'
    read_more_html = f'<a class="post-link" href="{link}" target="_blank" rel="noopener noreferrer">Read Full Post</a>' if link else ''
    meta_html     = f'<div class="post-meta">{meta}</div>' if meta else ''
    excerpt_html  = f'<p class="post-excerpt">{excerpt}</p>' if excerpt else ''
    og_image_tag  = f'<meta property="og:image" content="{html.escape(image)}">' if image else ''
    og_desc_tags  = f'<meta property="og:description" content="{excerpt}">\n    <meta name="description" content="{excerpt}">' if excerpt else ''
    canonical_tag = f'<link rel="canonical" href="{link}">' if link else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    {og_desc_tags}
    {og_image_tag}
    {canonical_tag}
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: Helvetica, Arial, sans-serif; background: #f5f5f5; color: #333; }}
        .page {{ max-width: 680px; margin: 2rem auto; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .post-image {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }}
        .post-body {{ padding: 2rem; }}
        .post-meta {{ font-size: 0.85rem; color: #888; margin-bottom: 0.75rem; }}
        .post-title {{ font-size: 1.6rem; font-weight: bold; line-height: 1.25; margin-bottom: 1rem; color: #111; }}
        .post-excerpt {{ font-size: 1rem; line-height: 1.65; color: #444; margin-bottom: 1.5rem; }}
        .post-link {{ display: inline-block; background: #19747d; color: white; text-decoration: none; padding: 0.6rem 1.25rem; border-radius: 4px; font-size: 0.95rem; font-weight: 600; }}
        .placeholder-img {{ width: 100%; aspect-ratio: 16/9; background: #e8eef2; }}
        .source-note {{ padding: 1rem 2rem; font-size: 0.75rem; color: #aaa; border-top: 1px solid #eee; text-align: center; }}
        .source-note a {{ color: #aaa; }}
    </style>
</head>
<body>
    <div class="page">
        {img_html}
        <div class="post-body">
            {meta_html}
            <h1 class="post-title">{title}</h1>
            {excerpt_html}
            {read_more_html}
        </div>
        <div class="source-note">Published by <a href="{link}" target="_blank" rel="noopener noreferrer">Caltech Library</a></div>
    </div>
</body>
</html>'''

# ── Fetch feed ──────────────────────────────────────────────────────────────
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
    uuid   = raw_id.replace('urn:uuid:', '')
    title  = entry.findtext(t('title'), '').strip()
    date   = entry.findtext(t('updated'), '').strip()

    author_el = entry.find(t('author'))
    author = author_el.findtext(t('name'), '').strip() if author_el is not None else ''

    link_el = entry.find(t('link'))
    link = link_el.get('href', '').strip() if link_el is not None else ''

    content_el   = entry.find(t('content'))
    content_html = (content_el.text or '') if content_el is not None else ''

    image  = first_image(content_html)
    excerpt = make_excerpt(strip_html(content_html))

    posts.append({
        'id': uuid, 'title': title, 'date': date,
        'author': author, 'link': link, 'image': image, 'excerpt': excerpt,
    })

# ── Write posts.json ─────────────────────────────────────────────────────────
out = {'posts': posts}
with open('posts.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# ── Generate static post pages ───────────────────────────────────────────────
posts_dir = 'posts'
if os.path.exists(posts_dir):
    shutil.rmtree(posts_dir)
os.makedirs(posts_dir)

for post in posts:
    path = os.path.join(posts_dir, f"{post['id']}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(make_post_html(post))

print(f'Wrote {len(posts)} posts to posts.json and posts/')

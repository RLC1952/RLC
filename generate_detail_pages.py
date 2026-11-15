import json
import os
import re
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ARCHIVE_FILE = Path('news_archive.json')
OUTPUT_DIR = Path('pages/news')
PLACEHOLDER_IMAGE = '../../assets/images/news-placeholder.svg'
CSS_VERSION = 15
COMPONENTS_VERSION = 3


def news_image_path(article, image):
    local = (image or {}).get('local', '')
    if not local:
        return PLACEHOLDER_IMAGE
    path = Path(local)
    return f'../../{local}' if path.exists() else PLACEHOLDER_IMAGE


def paragraphs(article):
    text = (article.get('content_text') or '').strip()
    if text:
        chunks = [chunk.strip() for chunk in re.split(r'\n{2,}|\r?\n', text) if chunk.strip()]
        body = ''.join(f'<p>{escape(chunk)}</p>' for chunk in chunks)
    else:
        html = article.get('content_html') or ''
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        body = f'<p>{escape(text)}</p>' if text else '<p>Zu diesem Beitrag liegt noch kein Text vor.</p>'

    links = article.get('links') or []
    for link in links:
        if not isinstance(link, dict):
            raise ValueError(f"Ungueltiger Link in News-Beitrag {article.get('id', '')}.")
        label = str(link.get('text') or '').strip()
        url = str(link.get('url') or '').strip()
        parsed_url = urlparse(url)
        is_site_path = url.startswith('/') and not url.startswith('//') and '\\' not in url
        is_web_url = parsed_url.scheme in {'http', 'https'} and bool(parsed_url.netloc)
        if not label or any(char.isspace() for char in url) or not (is_site_path or is_web_url):
            raise ValueError(f"Ungueltiger Link in News-Beitrag {article.get('id', '')}.")
        body += (
            f'<p><a class="subpage-link" href="{escape(url, quote=True)}" target="_blank" rel="noopener">'
            f'{escape(label)} <span class="material-icons-round" aria-hidden="true">open_in_new</span></a></p>'
        )
    return body


def image_markup(article):
    images = article.get('images') or []
    if not images:
        return f'<figure class="news-detail-figure"><img src="{PLACEHOLDER_IMAGE}" alt="" loading="eager" decoding="async"></figure>'

    first = images[0]
    main = news_image_path(article, first)
    main_markup = f'<figure class="news-detail-figure"><img src="{main}" alt="{escape(article.get("title", "Vereinsmeldung"))}" loading="eager" decoding="async"></figure>'

    extra = images[1:]
    if not extra:
        return main_markup

    extras = ''.join(
        f'<figure><img src="{news_image_path(article, image)}" alt="" loading="lazy" decoding="async"></figure>'
        for image in extra
    )
    return f'{main_markup}<div class="news-detail-gallery">{extras}</div>'


def page(article):
    title = article.get('title') or 'Vereinsmeldung'
    date = article.get('date') or 'Datum folgt'
    title_html = escape(title)
    date_html = escape(date)
    back = '<a href="../news.html" class="subpage-button subpage-button--secondary"><span class="material-icons-round" aria-hidden="true">arrow_back</span> Zurück zur Übersicht</a>'

    return f'''<!DOCTYPE html>
<html class="light" lang="de">
<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>{title_html} | RLC 1952</title>
    <link rel="icon" href="/favicon.ico" sizes="48x48" />
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="192x192" href="/assets/images/favicon/favicon-192.png" />
    <link rel="apple-touch-icon" href="/assets/images/favicon/apple-touch-icon.png" />
    <link href="../../assets/css/design-tokens.css" rel="stylesheet" />
    <link href="../../assets/css/shell.css" rel="stylesheet" />
    <link href="../../assets/css/subpages.css?v={CSS_VERSION}" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Lexend:wght@600;700;800;900&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com?plugins=forms,typography"></script>
    <script src="../../assets/js/components.js?v={COMPONENTS_VERSION}"></script>
</head>
<body class="subpage subpage-news-detail min-h-screen">
    <header data-shared-shell-placeholder></header>
    <main class="subpage-main">
        <div class="subpage-stack">
            <div class="news-detail-top-actions">{back}</div>
            <article class="subpage-surface news-detail-article">
                <header class="news-detail-article__header">
                    <span class="subpage-eyebrow">Aktuelles</span>
                    <h1 class="news-detail-title">{title_html}</h1>
                    <div class="subpage-meta-row">
                        <span class="subpage-meta"><span class="material-icons-round" aria-hidden="true">calendar_today</span><strong>{date_html}</strong></span>
                        <span class="subpage-meta"><span class="material-icons-round" aria-hidden="true">person</span><strong>RLC 1952</strong></span>
                    </div>
                </header>
                {image_markup(article)}
                <div class="news-detail-body">{paragraphs(article)}</div>
                <div class="subpage-actions">{back}</div>
            </article>
        </div>
    </main>
    <footer data-shared-footer-placeholder></footer>
</body>
</html>
'''


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    archive = json.loads(ARCHIVE_FILE.read_text(encoding='utf-8'))
    archive.sort(key=lambda item: int(item.get('id') or 0), reverse=True)
    for article in archive:
        article_id = article.get('id')
        if article_id:
            (OUTPUT_DIR / f'{article_id}.html').write_text(page(article), encoding='utf-8')
    print(f'Generated {len(archive)} detail pages.')


if __name__ == '__main__':
    main()

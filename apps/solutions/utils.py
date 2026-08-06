import re
from urllib.parse import parse_qs, urlparse


YOUTUBE_HOSTS = {
    'youtube.com',
    'm.youtube.com',
    'youtube-nocookie.com',
}
VIMEO_HOSTS = {
    'vimeo.com',
    'player.vimeo.com',
}


def normalize_video_embed_url(value):
    """Return a safe YouTube/Vimeo embed URL, or an empty string."""
    if not value:
        return ''

    parsed = urlparse(str(value).strip())
    host = parsed.netloc.lower().split(':', 1)[0]
    if host.startswith('www.'):
        host = host[4:]

    path_parts = [part for part in parsed.path.split('/') if part]
    video_id = ''

    if host == 'youtu.be':
        video_id = path_parts[0] if path_parts else ''
    elif host in YOUTUBE_HOSTS:
        if parsed.path.rstrip('/') == '/watch':
            video_id = parse_qs(parsed.query).get('v', [''])[0]
        elif len(path_parts) >= 2 and path_parts[0] in {'embed', 'shorts', 'live'}:
            video_id = path_parts[1]

    if video_id and re.fullmatch(r'[A-Za-z0-9_-]{6,20}', video_id):
        return f'https://www.youtube-nocookie.com/embed/{video_id}'

    if host in VIMEO_HOSTS:
        if path_parts and path_parts[0] == 'video' and len(path_parts) >= 2:
            video_id = path_parts[1]
        elif path_parts:
            video_id = path_parts[0]

        if video_id.isdigit():
            return f'https://player.vimeo.com/video/{video_id}'

    return ''

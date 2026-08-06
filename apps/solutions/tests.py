from django.test import SimpleTestCase

from apps.solutions.utils import normalize_video_embed_url


class SolutionVideoUrlTests(SimpleTestCase):
    def test_normalizes_supported_video_urls(self):
        cases = {
            'https://www.youtube.com/watch?v=nBadHnv3gy8':
                'https://www.youtube-nocookie.com/embed/nBadHnv3gy8',
            'https://youtu.be/nBadHnv3gy8':
                'https://www.youtube-nocookie.com/embed/nBadHnv3gy8',
            'https://www.youtube.com/shorts/nBadHnv3gy8':
                'https://www.youtube-nocookie.com/embed/nBadHnv3gy8',
            'https://www.youtube-nocookie.com/embed/nBadHnv3gy8':
                'https://www.youtube-nocookie.com/embed/nBadHnv3gy8',
            'https://vimeo.com/123456789':
                'https://player.vimeo.com/video/123456789',
        }

        for source_url, expected_url in cases.items():
            with self.subTest(source_url=source_url):
                self.assertEqual(
                    normalize_video_embed_url(source_url),
                    expected_url,
                )

    def test_rejects_unsupported_or_malformed_urls(self):
        for source_url in ('', 'https://example.com/video/123', 'not-a-url'):
            with self.subTest(source_url=source_url):
                self.assertEqual(normalize_video_embed_url(source_url), '')

# Create your tests here.

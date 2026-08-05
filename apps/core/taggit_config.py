from taggit.apps import TaggitAppConfig


class VietnameseTaggitAppConfig(TaggitAppConfig):
    """Tên hiển thị tiếng Việt cho Taggit trong Django Admin."""

    verbose_name = 'Thẻ bài viết'

    def ready(self):
        super().ready()
        from taggit.models import Tag

        Tag._meta.verbose_name = 'Thẻ'
        Tag._meta.verbose_name_plural = 'Thẻ'

class ActiveOnlyMixin:
    @property
    def is_active(self):
        return getattr(self, "status", None) == "published"
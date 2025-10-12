from django.db import models


class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2000)
    alias = models.CharField(max_length=30, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.alias} -> {self.original_url}"

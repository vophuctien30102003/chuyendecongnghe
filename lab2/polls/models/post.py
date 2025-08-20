from django.db import models
from django.utils.text import slugify
from .person import Person
from .category import Category

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:80]
            # ensure uniqueness fallback
            orig = base
            i = 1
            from .post import Post as PostModel  # local import to avoid circular at import time
            while base and PostModel.objects.filter(slug=base).exclude(pk=self.pk).exists():
                i += 1
                base = f"{orig}-{i}"[:80]
            self.slug = base
        super().save(*args, **kwargs)

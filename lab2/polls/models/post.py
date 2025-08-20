from django.db import models
from django.utils.text import slugify
from .person import Person
from .category import Category


class PostQuerySet(models.QuerySet):
    def recent(self, limit=5):
        return self.order_by('-created_at')[:limit]

    def by_category(self, category_name: str):
        return self.filter(category__name__iexact=category_name)

    def with_author_email(self):
        return self.select_related('author').values('title','author__email')


class PostManager(models.Manager.from_queryset(PostQuerySet)):
    def recent_posts(self, limit=5):
        return self.get_queryset().recent(limit=limit)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    objects = PostManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['author','created_at'], name='post_author_created_idx'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['author','title'], name='uniq_author_title'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:80]
            orig = base
            i = 1
            while base and Post.objects.filter(slug=base).exclude(pk=self.pk).exists():
                i += 1
                base = f"{orig}-{i}"[:80]
            self.slug = base
        super().save(*args, **kwargs)

from django.db import models
from django.db.models import Count, Q


class PersonQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='AC')

    def with_post_counts(self):
        return self.annotate(post_count=Count('post'))

    def search_name(self, term: str):
        return self.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))


class PersonManager(models.Manager.from_queryset(PersonQuerySet)):  # type: ignore
    def search(self, term: str):
        return self.get_queryset().search_name(term)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=2, choices=[('AC','Active'),('IN','Inactive'),('PE','Pending')], default='AC')
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PersonManager()  # custom manager with queryset methods

    class Meta:
        ordering = ['last_name', 'first_name','status']
        indexes = [
            models.Index(fields=['last_name','first_name'], name='person_name_idx'),
            models.Index(fields=['status'], name='person_status_idx'),
        ]
        constraints = [
            models.CheckConstraint(check=~models.Q(first_name=''), name='first_name_not_blank'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.test import TestCase
from django.db import connection
from django.utils import timezone
from .models import Person, Post, Category


class QuerysetTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.person1 = Person.objects.create(first_name='A', last_name='One', email='a1@example.com')
		cls.person2 = Person.objects.create(first_name='B', last_name='Two', email='b2@example.com', status='IN')
		cat = Category.objects.create(name='Django')
		for i in range(3):
			Post.objects.create(title=f'Post {i}', content='x', author=cls.person1, category=cat)
		Post.objects.create(title='Another', content='y', author=cls.person2, category=cat)

	def test_person_active_queryset(self):
		self.assertEqual(Person.objects.active().count(), 1)

	def test_person_with_post_counts(self):
		p = Person.objects.with_post_counts().get(pk=self.person1.pk)
		self.assertEqual(p.post_count, 3)

	def test_post_recent(self):
		rec = Post.objects.recent(limit=2)
		self.assertEqual(len(rec), 2)

	def test_post_by_category(self):
		self.assertEqual(Post.objects.by_category('django').count(), 4)

	def test_post_with_author_email(self):
		data = list(Post.objects.with_author_email())
		self.assertTrue(any('a1@example.com' in d['author__email'] for d in data))

	def test_sql_view_exists(self):
		with connection.cursor() as cur:
			cur.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='polls_post_counts';")
			self.assertIsNotNone(cur.fetchone())

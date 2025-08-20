from django.contrib import admin
from .models import Person, Category, Post, Question, Choice

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "email", "status", "created_at", "updated_at")
	list_filter = ("status",)
	search_fields = ("first_name", "last_name", "email")
	readonly_fields = ("created_at", "updated_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "description", "created_at")
	search_fields = ("name",)
	ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "category", "created_at", "updated_at")
	list_filter = ("category", "created_at")
	search_fields = ("title", "author__first_name", "author__last_name")
	prepopulated_fields = {"slug": ("title",)}
	autocomplete_fields = ("author", "category")
	date_hierarchy = "created_at"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ("question_text", "pub_date")
	search_fields = ("question_text",)
	date_hierarchy = "pub_date"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
	list_display = ("choice_text", "question", "votes")
	search_fields = ("choice_text", "question__question_text")
	autocomplete_fields = ("question",)


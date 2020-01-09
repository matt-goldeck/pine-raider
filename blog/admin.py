from markdownx.admin import MarkdownxModelAdmin

from django.contrib import admin

from blog.models import BlogPost, BlogImage, Quote

class BlogImageInline(admin.StackedInline):
	model = BlogImage
	extra = 0

@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
	inlines = [
		BlogImageInline, 
	]
	list_display = ('title', 'display_on_landing', 'created_at', 'updated_at',)
	list_filter = ('created_at', 'updated_at', 'display_on_landing',)
	search_fields = ('title',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
	list_filter = ('display_on_not_found', 'author_name')
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from blog.models import BlogPost, Quote

class BlogView(View):
	def get(self, request, *args, **kwargs):
		context = self._get_context(request)
		template_name = self._get_template_name(request)
		return render(request, template_name, context=context)

	def _get_context(self, request):
		context = {'quote':self._get_random_quote(display_on_not_found=True)}
		return context

	def _get_template_name(self, request):
		return 'exceptions/404.html'

	def _get_random_quote(self, display_on_not_found=False):
		return Quote.objects.filter(
			display_on_not_found=display_on_not_found).order_by('?').first()


class HomeView(BlogView):
	"""Homepage; landing posts + preview image urls"""
	def _get_context(self, request):
		context = {
			'posts': BlogPost.objects.public().filter(
				display_on_landing=True).order_by('-created_at').all(),
			'quote': self._get_random_quote()
		}

		return context

	def _get_template_name(self, request):
		return 'landing.html'


class PostView(BlogView):
	"""Specific post; post content and url to header image"""
	def _get_context(self, request):
		key = self.kwargs['pk']
		if key:
			try:
				blog_post = BlogPost.objects.get(pk=key)
				# Don't reveal secrets
				if not blog_post.display_publically:
					raise PermissionDenied

			except BlogPost.DoesNotExist:
				pass

		context = {
			'blog_post':blog_post,
			'quote': self._get_random_quote()
		}

		return context

	def _get_template_name(self, request):
		return 'blog_post.html'


class BlogLandingView(BlogView):
	"""View for the blog landing; display all posts, paginate"""
	def _get_context(self, request):
		blog_posts = BlogPost.objects.public().order_by('-created_at').all()
		paginator = Paginator(blog_posts, 5)

		page = request.GET.get('page')
		posts = paginator.get_page(page)

		context = {
			'posts':posts,
			'quote': self._get_random_quote()
		}

		return context

	def _get_template_name(self, request):
		return 'blog_landing.html'


class ForbiddenView(BlogView):
	def _get_template_name(self, request):
		return 'exceptions/401.html'

class ServerErrorView(BlogView):
	def _get_template_name(self, request):
		return 'exceptions/500.html'

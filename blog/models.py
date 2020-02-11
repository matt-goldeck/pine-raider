import os

from django.db import models

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from pineraider import settings


class BlogPostQuerySet(models.query.QuerySet):
    def public(self):
        return self.filter(display_publically=True)

    def private(self):
        return self.filter(display_publically=False)

class BlogPostManager(models.Manager):
    def get_query_set(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def public(self):
        return self.get_query_set().public()

    def private(self):
        return self.get_query_set().private()

class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    heading = models.CharField(max_length=256, default=None)
    summary = models.CharField(max_length=256, default=None)
    content = MarkdownxField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    display_on_landing = models.BooleanField(default=True, help_text="If toggled, will display this post on the landing page.")
    display_publically = models.BooleanField(default=True, help_text="If toggled, this article will be accessible to the public.")

    objects = BlogPostManager()

    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdownify(self.content)

    def get_header_url(self):
        try:
            header_img = self.images.order_by('created_at').first()
        except BlogImage.DoesNotExist:
            pass  # TODO: Set a default image if nothing exists

        return header_img.get_url()

    def get_str_date(self):
        return self.created_at.strftime("%B %-d %Y")


class BlogImage(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='images')

    def get_standard_image_name(instance, filename):
        if instance.pk:
            existing = BlogImage.objects.get(pk=instance.pk)
            return existing.image.name

        post = instance.blog_post
        degree = post.images.count()

        ext = filename.split('.')[-1]
        filename = "{post_key}-{degree}.{ext}".format(
            post_key=post.pk, 
            degree=degree, 
            ext=ext)

        return "blog_images/{}/{}".format(post.pk, filename)
    image = models.ImageField(upload_to=get_standard_image_name)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return self.image.url

class Quote(models.Model):
    text = models.CharField(max_length=256)
    author_name = models.CharField(max_length=256)

    display_on_not_found = models.BooleanField(default=False, help_text='Whether or not to display this quote on 404 pages.')

    def __str__(self):
        return "{} - {}".format(self.text, self.author_name)
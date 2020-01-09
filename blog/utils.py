import os, os.path

from django.conf import settings

def get_standard_image_name(instance, filename):
	"""Return new filename for a blog image in format"""
	post = instance.blog_post

	# Get count of all files currently related to this blog_post
	post_images = [name for name in os.listdir("{}/blog_images/".format(settings.MEDIA_ROOT))
				   if name.split('-')[0] == str(post.pk)]
	degree = len(post_images)

	ext = filename.split('.')[-1]
	filename = "{post_key}-{degree}.{ext}".format(
		post_key=post.pk, 
		degree=degree, 
		ext=ext)

	return os.path.join('blog_images/', filename)
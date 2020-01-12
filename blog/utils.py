import boto3

from django.conf import settings

def get_standard_image_name(instance, filename):
	"""Return new filename for a blog image in format"""
	post = instance.blog_post
	degree = post.images.count()

	ext = filename.split('.')[-1]
	filename = "{post_key}-{degree}.{ext}".format(
		post_key=post.pk, 
		degree=degree, 
		ext=ext)

	return "blog_images/{}/{}".format(post.pk, filename)
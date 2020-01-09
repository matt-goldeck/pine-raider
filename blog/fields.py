class BlogImageField(models.ImageField):

	def pre_save(self, model_instance, add):
    	file = super(models.FileField, self).pre_save(model_instance, add)
		
		if file and not file._committed:
			ext = file.name.split('.')[-1]
			file.save('{0}.{1}'.format(model_instance.pk, file, save=False))

		return file
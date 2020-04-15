from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	return new_slug +' - '+ str(int(time()))

class Post(models.Model):
	title = models.CharField(max_length=150, db_index=True)
	slug = models.SlugField(max_length=150, blank = True, unique=True)
	tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
	body = models.TextField(blank=True, db_index=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	like = models.IntegerField(default=0)
	

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug':self.slug})

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug':self.slug})


	def __str__(self):
		return str(self.title)


class Tag(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)

	def __str__(self):
		return '{}'.format(self.title)

	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug':self.slug})

	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug':self.slug})

class Comment(models.Model):
	text = models.TextField()
	post = models.ForeignKey('Post', null=True, on_delete=models.CASCADE, related_name='comment')

	def __str__(self):
		return '{}'.format(self.post)





		
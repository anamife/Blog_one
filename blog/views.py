from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View
from .models import Post, Tag, Comment
from .utils import ObjectDetailMixing
from .forms import TagForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist


def posts_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/index.html', {'posts':posts})


class PostDetail(ObjectDetailMixing, View):
	model = Post
	template = 'blog/post_detail.html'



class PostUpdate(LoginRequiredMixin, View):
	raise_exception = True
	def get(self, request, slug):
		post = Post.objects.get(slug__iexact=slug)
		bound_form = PostForm(instance=post)
		return render(request, 'blog/post_update.html', {'form':bound_form,'post':post})

	def post(self, request, slug):
		post = Post.objects.get(slug__iexact=slug)
		bound_form=PostForm(request.POST, instance=post)
		
		if bound_form.is_valid():
	 		new_post = bound_form.save()
	 		return redirect(new_post)

		return render(request, 'blog/post_update.html', {'form':bound_form,'post':post})

def tags_list(request):
	tags = Tag.objects.all()
	return render(request, 'blog/tags_list.html', {'tags':tags})


class TagDetail(ObjectDetailMixing, View):
	model = Tag
	template = 'blog/tag_detail.html'
	

class TagCreate(LoginRequiredMixin, View):
	raise_exception = True
	
	def get(self, request):
		form = TagForm()
		return render(request, 'blog/tag_create.html', {'form':form})


	def post(self, request):
		bound_form=TagForm(request.POST)

		if bound_form.is_valid():
			new_tag = bound_form.save()
			return redirect(new_tag)

		return render(request, 'blog/tag_create.html', {'form':bound_form})

class TagUpdate(LoginRequiredMixin, View):
	raise_exception = True
	def get(self, request, slug):
		tag = Tag.objects.get(slug__iexact=slug)
		bound_form = TagForm(instance=tag)
		return render(request, 'blog/tag_update.html', {'form':bound_form,'tag':tag})

	def post(self, request, slug):
		tag = Tag.objects.get(slug__iexact=slug)
		bound_form=TagForm(request.POST, instance=tag)
		
		if bound_form.is_valid():
	 		new_tag = bound_form.save()
	 		return redirect(new_tag)

		return render(request, 'blog/tag_update.html', {'form':bound_form,'tag':tag})

class PostCreate(LoginRequiredMixin, View):
	raise_exception = True
	def get(self, request): 
		form = PostForm()
		return render(request, 'blog/post_create.html', {'form': form})

	def post(self, request):
	 	bound_form=PostForm(request.POST)

	 	if bound_form.is_valid():
	 		new_post = bound_form.save()
	 		return redirect(new_post)

	 	return render(request, 'blog/post_create.html', {'form':bound_form})

class TagDelete(LoginRequiredMixin, View):
	raise_exception = True
	def get(self, request, slug):
		tag = Tag.objects.get(slug__iexact=slug)
		return render(request, 'blog/tag_delete.html', {'tag':tag})

	def post(self, request, slug):
		tag = Tag.objects.get(slug__iexact=slug)
		tag.delete()
		return redirect(reverse('tags_list_url'))

class PostDelete(LoginRequiredMixin, View):
	raise_exception = True
	def get(self, request, slug):
		post = Post.objects.get(slug__iexact=slug)
		return render(request, 'blog/post_delete.html', {'post':post})

	def post(self, request, slug):
		post = Post.objects.get(slug__iexact=slug)
		post.delete()
		return redirect(reverse('posts_list_url'))

def add_like(request, slug):
	try:
		post = Post.objects.get(slug__iexact=slug)
		post.like += 1
		post.save()
	except ObjectDoesNotExist:
		raise Http404
	return redirect('/')



#def account_list(request):
#	return render(request, 'blog/account_list.html')


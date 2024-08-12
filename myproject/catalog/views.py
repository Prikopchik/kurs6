from django.shortcuts import redirect, render, get_object_or_404

from .forms import ProductForm 
from .models import Product
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django import forms
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import BlogPost
from django.utils.text import slugify
from .forms import BlogPostForm

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class ContactView(FormView):
    template_name = 'catalog/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        print(f"Name: {form.cleaned_data['name']}, Email: {form.cleaned_data['email']}, Message: {form.cleaned_data['message']}")
        return super().form_valid(form)

class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'object_list'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    success_url = '/products/'

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10 

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(is_published=True) 

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        blog_post = super().get_object(queryset)
        blog_post.view_count += 1
        blog_post.save(update_fields=['view_count']) 
        return blog_post

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'catalog/blogpost_form.html'
    fields = ['title', 'slug', 'content', 'preview_image', 'is_published']

    def form_valid(self, form):
        blog_post = form.save(commit=False)
        blog_post.slug = slugify(blog_post.title)
        blog_post.save()
        return super().form_valid(form)

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'catalog/blogpost_form.html'
    fields = ['title', 'slug', 'content', 'preview_image', 'is_published']

    def get_success_url(self):
        return reverse('blogpost_detail', args=[self.object.pk])

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
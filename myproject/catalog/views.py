from django.shortcuts import redirect, render, get_object_or_404

from .forms import ContactForm, ProductForm , VersionForm , BlogPostForm
from .models import Product , BlogPost , Version
from django.views.generic import ListView , UpdateView, DeleteView ,TemplateView, DetailView
from django.views.generic.edit import CreateView , FormView
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

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

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_with_versions = []

        for product in context['products']:
            try:
                current_version = product.versions.get(is_current=True)
            except Version.DoesNotExist:
                current_version = None
            
            products_with_versions.append({
                'product': product,
                'current_version': current_version
            })

        context['products_with_versions'] = products_with_versions
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/product_version_form.html'
    success_url = reverse_lazy('product_version_list')

class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/product_version_form.html'
    success_url = reverse_lazy('product_version_list')

class VersionListView(ListView):
    model = Version
    template_name = 'catalog/product_version_list.html'
    context_object_name = 'product_versions'

class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'catalog/product_version_confirm_delete.html'
    success_url = reverse_lazy('product_version_list')
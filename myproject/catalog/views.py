from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContactForm, ProductForm, VersionForm, BlogPostForm
from .models import Product, BlogPost, Version
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .services import get_products_by_category


class HomeView(TemplateView):
    template_name = 'home.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        print(
            f"Name: {form.clean_name['name']}, Email: {form.cleaned_data['email']}, Message: {form.cleaned_data['message']}")        
        return super().form_valid(form)


class IndexView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'object_list'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        blog_post = super().get_object(queryset)
        blog_post.view_count += 1
        blog_post.save(update_fields=['view_count'])
        return blog_post


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'
    fields = ['title', 'slug', 'content', 'preview_image', 'is_published']

    def form_valid(self, form):
        blog_post = form.save(commit=False)
        blog_post.slug = slugify(blog_post.title)
        blog_post.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'
    fields = ['title', 'slug', 'content', 'preview_image', 'is_published']

    def get_success_url(self):
        return reverse('blogpost_detail', args=[self.object.pk])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog_list')


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_with_versions = []

        for product in context['products']:
            try:
                current_version = product.version.get(is_current=True)
            except Version.DoesNotExist:
                current_version = None

            products_with_versions.append({
                'product': product,
                'current_version': current_version
            })

        context['products_with_versions'] = products_with_versions
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def create_product(request):
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.owner = request.user
                product.save()
                return redirect('product_list')
        else:
            form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this product.")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete_product(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.owner != request.user and not request.user.has_perm('app.delete_product'):
            raise PermissionDenied("You do not have permission to delete this product.")
        product.delete()
        return redirect('product_list')


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'product_version_form.html'
    success_url = reverse_lazy('product_version_list')


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'product_version_form.html'
    success_url = reverse_lazy('product_version_list')


class VersionListView(ListView):
    model = Version
    template_name = 'product_version_list.html'
    context_object_name = 'product_versions'


class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'product_version_confirm_delete.html'
    success_url = reverse_lazy('product_version_list')


class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_unpublish.html'
    fields = []  
    success_url = reverse_lazy('product_list')
    permission_required = 'catalog.can_unpublish_product' 

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def form_valid(self, form):
        product = form.save(commit=False)
        product.is_published = False
        product.save()
        return super().form_valid(form)

class ProductEditDescriptionView(PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.can_edit_description'
    template_name = 'product_form.html'
    fields = ['description']


class ProductEditCategoryView(PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.can_edit_category'
    template_name = 'product_form.html'
    fields = ['category']


def products_by_category(request, category_id):
    products = get_products_by_category(category_id)
    return render(request, 'catalog/products_by_category.html', {'products': products})
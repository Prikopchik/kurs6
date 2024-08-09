from django.shortcuts import redirect, render, get_object_or_404

from .forms import ProductForm 
from .models import Product
from django.core.paginator import Paginator

def home(request):
    return render(request, 'catalog/home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Name: {name}, Email: {email}, Message: {message}")
    return render(request, 'catalog/contact.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    context = {
        'product': product,
    }
    
    return render(request, 'catalog/product_detail.html', context)

def index_view(request):
    products = Product.objects.all()

    context = {'object_list': products}

    return render(request, 'catalog/index.html', context)

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {'object': product}

    return render(request, 'catalog/product_detail.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
       form = ProductForm()
    
    return render(request, 'catalog/create_product.html', {'form': form})

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 10) 

    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {'page_obj': page_obj})
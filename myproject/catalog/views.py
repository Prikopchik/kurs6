from django.shortcuts import render, get_object_or_404
from .models import Product

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
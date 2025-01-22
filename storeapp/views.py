from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product

# Create your views here.

def home(request):
    trending_products = Product.objects.filter(trending=1)
    context = {"trending_products": trending_products}
    return render(request, 'store/home.html',context)


def collections(request):
    """
    Fetch and display all active categories.
    """
    categories = Category.objects.filter(status=0)  # Fetch only categories with status 0 (active)
    context = {'categories': categories}
    return render(request, "store/collections.html", context)



def collectionview(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products=Product.objects.filter(category__slug=slug)
        category_name=Category.objects.filter(slug=slug).first()
        context={"products":products,'category_name':category_name}
        return render(request,"store/products/home.html",context)
    else:
        messages.warning(request,"No Such Category Found!")
        return redirect('collections')


def productview(request,prod_slug,cate_slug):
    if Category.objects.filter(slug=cate_slug,status=0).exists():
        if Product.objects.filter(slug=prod_slug,status=0).exists():
            products=Product.objects.filter(slug=prod_slug,status=0).first()
            context={'products':products}
        else:
            messages.error(request,"No such product found!")
            return redirect("collections")
    else:
        messages.error(request,"No such category found!")
        return redirect("collections")

    return render(request,"store/products/view.html",context)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Fetch all products
class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()  # Fetch all products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# Fetch product details by ID
class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)  # Fetch product by primary key
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

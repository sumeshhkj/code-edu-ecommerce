from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product

# Create your views here.

def home(request):
    """
    Render the homepage.
    """
    return render(request, 'store/home.html')


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



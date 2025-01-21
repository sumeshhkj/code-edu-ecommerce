from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from storeapp.models import Product, Wishlist


# Display the user's wishlist
@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, "store/wishlist.html", context)


# Add product to the user's wishlist
def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                prod_id = int(request.POST.get('product_id'))
                product_check = Product.objects.get(id=prod_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'No such product found...!'})

            # Check if the product is already in the wishlist
            if Wishlist.objects.filter(user=request.user, product_id=prod_id).exists():
                return JsonResponse({'status': 'Product already in wishlist'})

            # Add to the wishlist
            Wishlist.objects.create(user=request.user, product_id=prod_id)
            return JsonResponse({'status': 'Product added to wishlist'})

        else:
            return JsonResponse({'status': 'Login to continue...!'})
    return redirect('/')


# Remove product from the user's wishlist
def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                prod_id = int(request.POST.get('product_id'))
                wishlist_item = Wishlist.objects.get(user=request.user, product_id=prod_id)
                wishlist_item.delete()
                return JsonResponse({'status': 'Product removed from wishlist'})
            except Wishlist.DoesNotExist:
                return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status': 'Login to continue'})

    return redirect('/')

from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from storeapp.models import Product, Cart, Wishlist, OrderItem, Order, Profile
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
import random


@login_required(login_url="loginpage")
def index(request):
    """
    Displays the checkout page with cart items and user profile details.
    """
    # Ensure cart items are valid
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            item.delete()  # Corrected the delete call

    # Calculate total price for the cart items
    cartitems = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.product_qty for item in cartitems)

    # Retrieve user profile or initialize an empty one
    userprofile = Profile.objects.filter(user=request.user).first()

    context = {'cartitems': cartitems, 'total_price': total_price, 'userprofile': userprofile}
    return render(request, "store/checkout.html", context)


@login_required(login_url="loginpage")
def placeorder(request):
    """
    Handles order placement and ensures user details and order details are saved.
    """
    if request.method == 'POST':
        try:
            currentuser = User.objects.get(id=request.user.id)

            # Save user first name and last name if not already set
            if not currentuser.first_name:
                currentuser.first_name = request.POST.get('firstname')
                currentuser.last_name = request.POST.get('lastname')
                currentuser.save()

            # Check and create Profile if it doesn't exist
            userprofile, created = Profile.objects.get_or_create(user=request.user)
            userprofile.phone = request.POST.get('Phone')
            userprofile.address = request.POST.get('Address')
            userprofile.city = request.POST.get('City')
            userprofile.state = request.POST.get('State')
            userprofile.country = request.POST.get('Country')
            userprofile.pincode = request.POST.get('PinCode')

            # Validate pincode
            if not userprofile.pincode:
                messages.error(request, "Pincode is required.")
                return redirect('checkout')

            userprofile.save()

            # Retrieve payment ID
            payment_id = request.POST.get('payment_id', None)  # Get payment_id from the form

            # Create new order
            neworder = Order(
                user=request.user,
                fname=request.POST.get('firstname'),
                lname=request.POST.get('lastname'),
                email=request.POST.get('email'),
                phone=request.POST.get('Phone'),
                address=request.POST.get('Address'),
                city=request.POST.get('City'),
                state=request.POST.get('State'),
                country=request.POST.get('Country'),
                pincode=request.POST.get('PinCode'),
                payment_mode=request.POST.get('payment_mode'),
                payment_id=payment_id,  # Pass the payment_id here
            )

            # Calculate total price
            cart = Cart.objects.filter(user=request.user)
            cart_total_price = sum(item.product.selling_price * item.product_qty for item in cart)
            neworder.total_price = cart_total_price

            # Generate unique tracking number
            trackno = 'Eapp' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = 'Eapp' + str(random.randint(1111111, 9999999))
            neworder.tracking_no = trackno

            neworder.save()

            # Create OrderItems and reduce product stock
            for item in cart:
                OrderItem.objects.create(
                    order=neworder,
                    product=item.product,
                    price=item.product.selling_price,
                    quantity=item.product_qty
                )

                # Decrease product quantity
                item.product.quantity -= item.product_qty
                item.product.save()

            # Clear user cart
            Cart.objects.filter(user=request.user).delete()

            messages.success(request, "Your order has been placed successfully")

            # Handle payment response
            payMode = request.POST.get('payment_mode')
            if payMode == "Paid by Razorpay":
                # Handle Razorpay payment (example: pass payment ID from Razorpay)
                return JsonResponse({'status': 'Your order has been placed successfully'})

            return redirect('orderview', t_no=neworder.tracking_no)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('checkout')

    return redirect('checkout')


@login_required(login_url='loginpage')
def razorpaycheck(request):
    """
    Handles Razorpay payment check by calculating total cart price.
    """
    try:
        cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.product_qty for item in cart)

        return JsonResponse({'total_price': total_price})

    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {str(e)}"})

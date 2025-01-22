from django.urls import path
from . import views
from django.conf import settings
from storeapp.controller import authview, cart, wishlist, checkout, order
from django.conf.urls.static import static
from .views import ProductListView, ProductDetailView

app_name = 'storeapp'

urlpatterns = [
    # Home and Collections
    path('', views.home, name='home'),
    path('collection', views.collections, name='collections'),
    path('collections/<str:slug>', views.collectionview, name='collectionview'),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name='productview'),

    # Authentication
    path('register/', authview.register, name='register'),
    path('login/', authview.loginpage, name='loginpage'),
    path('logout/', authview.logoutpage, name='logout'),

    # Cart related paths
    path('add-to-cart', cart.addtocart, name='add-to-cart'),
    path('cart', cart.viewcart, name='cart'),
    path('update-cart', cart.updatecart, name='update_cart'),
    path('delete-cart-item', cart.deletecartitem, name='delete-cart-item'),

    # Wishlist related paths
    path('wishlist', wishlist.index, name='wishlist'),
    path('add-to-wishlist', wishlist.addtowishlist, name='add_to_wishlist'),  # Fixed the URL path here
    path('delete-wishlist-item', wishlist.deletewishlistitem, name='delete_wishlist_item'),

    # Checkout and order
    path('checkout', checkout.index, name="checkout"),
    path('place-order', checkout.placeorder, name='placeorder'),
    path('proceed-to-pay/', checkout.razorpaycheck, name='proceed-to-pay'),
    path('order/', order.order_view, name='order'),
    path('view-order/<str:t_no>/', order.view_order, name='orderview'),

    #API
    path('api/products/', ProductListView.as_view(), name='product-list'),  # Get all products
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Get product by ID

]

# Serving static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

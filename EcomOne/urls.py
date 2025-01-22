from django.contrib import admin
from django.urls import path, include
from storeapp import views
from django.conf import settings
from django.conf.urls.static import static
from storeapp.controller import authview, cart, wishlist, checkout, order
from storeapp.views import ProductListView, ProductDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('storeapp/', include('storeapp.urls')),
    path('', views.home, name='home'),  # Root URL mapped to the home view
    path('collection', views.collections, name='collections'),
    path('collections/<str:slug>', views.collectionview, name='collectionview'),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name='productview'),

    path('register/', authview.register, name='register'),
    path('login/', authview.loginpage, name='loginpage'),
    path('logout/', authview.logoutpage, name='logout'),

    path('add-to-cart/', cart.addtocart, name='add-to-cart'),
    path('cart/', cart.viewcart, name='cart'),
    path('update-cart/', cart.updatecart, name='update-cart'),
    path('delete-cart-item/', cart.deletecartitem, name='delete-cart-item'),

    # Wishlist URLs
    path('wishlist/', wishlist.index, name='wishlist'),
    path('add-to-wishlist/', wishlist.addtowishlist, name='add-to-wishlist'),
    path('delete-wishlist-item/', wishlist.deletewishlistitem, name='delete-wishlist-item'),

    # Checkout URLs
    path('checkout/', checkout.index, name="checkout"),
    path('place-order/', checkout.placeorder, name='placeorder'),
    path('proceed-to-pay/', checkout.razorpaycheck, name='proceed-to-pay'),

    # Order URLs
    path('order/', order.order_view, name='order'),
    path('view-order/<str:t_no>/', order.view_order, name='orderview'),

    # API
    path('api/products/', ProductListView.as_view(), name='product-list'),  # Get all products
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Get product by ID
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

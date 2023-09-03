from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from store.controller import authview,cart,wishlist,checkout,order

urlpatterns = [
    path('', views.home, name='home'),
    path('collections', views.collections, name='collections'),
    path('collections/<str:slug>', views.collectionsview, name='collectionsview'),
    path('collections/<str:cate_slug>/<str:prod_slug>/<int:prod_id>', views.productview, name='productview'),
    path('accounts/signup', authview.register,name='register'),
    path('accounts/login', authview.loginPage ,name='login'),
    path('accounts/logout', authview.logoutPage ,name='logout'),
    
    path('add-to-cart',cart.addToCart,name='addToCart'),
    path('update-cart',cart.updateCart,name='updateCart'),
    path('delete-cart-item',cart.deleteCartItem,name='deleteCartitem'),
    path('cart',cart.viewCart,name='cart'),

    path('wishlist',wishlist.index,name='wishlist'),
    path('add-to-wishlist',wishlist.addToWishlist,name='addtowishlist'),
    path('delete-wishlist-item',wishlist.deleteWishlistItem,name='deletewishlistitem'),

    path('checkout',checkout.index,name='checkout'),
    path('place-order',checkout.placeorder,name='placeorder'),

    path('proceed-to-pay',checkout.razoPayCheck),
    path('my-orders',order.index,name='myorders'),
    path('view-order/<str:t_no>',order.vieworder,name="orderview")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)   
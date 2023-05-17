from store.models import Product,Cart,Wishlist
from django.shortcuts import redirect,render
from django.http.response import JsonResponse
from django.contrib import messages

def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    # for item in rawcart:
    #     if item.product_qty > item.product.quantity:
    #         Cart.objects.delete(id=item.id) 
    # cartitems = Cart.objects.filter(user=request.user)
    # total_price = 0
    # for item in cartitems:
    #     total_price = total_price + item.selling_price * item.product_qty
    # context = {'cartitems':cartitems,'total_price':total_price}
    return render(request,"store/checkout.html")
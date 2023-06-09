from store.models import Cart,Order,OrderItem,Product
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.contrib import messages
import random

@login_required(login_url='login')
def index(request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id) 
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty
    context = {'cart' : cart,'cartitems' : cartitems,'total_price' : total_price}
    return render(request,"store/checkout.html",context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone_no = request.POST.get('phone_no')
        neworder.address = request.POST.get('address')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.city = request.POST.get('city')

        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty
        
        neworder.total_price = cart_total_price

        track_no = 'TRACK'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no = track_no) is None:
            track_no = 'TRACK'+str(random.randint(1111111,9999999))
        
        neworder.tracking_no = track_no
        neworder.save()

        neworderitems = Cart.objects.filter(user = request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty
            )

            # To decrease the product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        # To clear user cart
        Cart.objects.filter(user=request.user).delete()

        messages.success(request,"Your Order Has been Placed Successfully ")
    
    return redirect('/')

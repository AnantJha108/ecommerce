from store.models import Cart,Order,OrderItem,Product,Profile,Coupon
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import random

@login_required(login_url='login')
def index(request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id) 
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    total_shipping_price = 0
    delivery_charge = 49
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty
        total_shipping_price = total_price + delivery_charge

    userProfile = Profile.objects.filter(user=request.user).first()

    context = {'cart' : cart,'cartitems' : cartitems,'total_price' : total_price , 'total_shipping_price' : total_shipping_price , 'userProfile' : userProfile}
    return render(request,"store/checkout.html",context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        currentUser = User.objects.filter(id=request.user.id).first()
        if not currentUser.first_name:
            currentUser.first_name = request.POST.get('fname')
            currentUser.last_name = request.POST.get('lname')
            currentUser.email = request.POST.get('email')
            currentUser.save()

        if not Profile.objects.filter(user=request.user.id):
            userProfile = Profile()
            userProfile.user = request.user
            userProfile.phone_no = request.POST.get('phone_no')
            userProfile.address = request.POST.get('address')
            userProfile.country = request.POST.get('country')
            userProfile.pincode = request.POST.get('pincode')
            userProfile.city = request.POST.get('city')
            userProfile.save()

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
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        for item in cart:
            if(item.product.selling_price >= 499):
                total_price = total_price + item.product.selling_price * item.product_qty
            else:
                total_price = (total_price + item.product.selling_price * item.product_qty ) + 49
        
        neworder.total_price = total_price

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

        messages.success(request,"Your Order Has been Placed Successfully")
        paymode = request.POST.get('payment_mode')
        if(paymode == 'Paid by Razorpay'):
            return JsonResponse({'status':'Your order has been Placed Successfully'})
    return redirect('/')

@login_required(login_url='login')
def razoPayCheck(request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
            delivery_charge = 49
            total_price = 0
            if(item.product.selling_price >= 499):
                total_price = total_price + item.product.selling_price * item.product_qty
            else:
                total_price = (total_price + item.product.selling_price * item.product_qty ) + delivery_charge
    return JsonResponse({
        'total_shipping_price' :  total_price
    })

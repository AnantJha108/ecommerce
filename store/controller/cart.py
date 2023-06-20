from django.http.response import JsonResponse
from django.shortcuts import redirect,render
from store.models import Product,Cart
from django.contrib import messages

def addToCart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({'status':'Product Already in Cart '})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user = request.user,product_id=prod_id,product_qty = prod_qty)
                        return JsonResponse({'status':'Product Added To Cart '})
                    else:
                        return JsonResponse({'status':"Only " + str(product_check.quantity) + " Quantity Available"})
            else:
                return JsonResponse({'status':'No such category found '})
        else:
            return JsonResponse({'status':'Login To Continue...'})
    return redirect('/')

def viewCart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitems = Cart.objects.filter(user=request.user)
        total_price = 0
        total_shipping_price = 0
        delivery_charge = 49
        for item in cartitems:
            total_price = total_price + item.product.selling_price * item.product_qty
            total_shipping_price = total_price + delivery_charge
        context = {'cart':cart,'cartitems':cartitems,'total_price':total_price,'total_shipping_price':total_shipping_price}
        return render(request,"store/cart.html",context)
    else:
        messages.success(request,"Login Please")
        return redirect('login')
    
def updateCart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id,user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':'Updated Successfully'})
    return redirect('/')

def deleteCartItem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status':'Cart Item Deleted'})
    return redirect('/')


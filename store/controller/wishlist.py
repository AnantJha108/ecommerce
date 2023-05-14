from store.models import Product,Cart,Wishlist
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse


@login_required(login_url='login')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context={'wishlist':wishlist}
    return render(request,"store/wishlist.html",context)

def addToWishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user,product_id=prod_id)):
                    return JsonResponse({'status':"Product Already in Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user,product_id=prod_id)
                    return JsonResponse({'status':'Product added to wishlist'})
            else:
                return JsonResponse({'status':'No such Product Found'})
        else:
            return JsonResponse({'status':'Login To Continue'})
    return redirect('/')       

def deleteWishlistItem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(Wishlist.objects.filter(user=request.user,product_id=prod_id)):
            wishlistitem = Wishlist.objects.get(product_id=prod_id,user=request.user)
            wishlistitem.delete()
        return JsonResponse({'status':'Wishlist Item Deleted'})
    return redirect('/')

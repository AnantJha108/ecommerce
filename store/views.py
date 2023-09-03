from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Category,Product,Wishlist
from django.http.response import JsonResponse

# Create your views here.
def home(request):
    category = Category.objects.all()
    products = Product.objects.all()
    context =  {'category':category,'products' : products}
    return render(request,'store/index.html',context)


def collections(request):
    category = Category.objects.all()
    product = Product.objects.all()
    context = {'category':category,'products' : product}
    return render(request,"store/collection.html",context)

def collectionsview(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products = Product.objects.filter(category__slug=slug)
        category_name = Category.objects.filter(slug=slug).first()
        context = {'products':products,'category_name':category_name}
        return render(request,"store/products/index.html",context)
    else:
        messages.warning(request,"No such category Found")
        return redirect('collections')
    
def productview(request,cate_slug,prod_slug,prod_id):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            products=Product.objects.filter(slug=prod_slug,status=0).first
            wishlist = Wishlist.objects.filter(user=request.user, product_id=prod_id).exists()
            context={'products':products,'wishlist':wishlist}
        else:
            messages.error(request,"No such product is found")
            return redirect('collections')
    else:
        messages.error(request,"No such category is found")
        return redirect('collections')
    return render(request,"store/products/view.html",context)



from store.models import Order,OrderItem
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders' : orders}
    return render(request,"store/orders/index.html",context=context)

@login_required(login_url='login')
def vieworder(request,t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orders = OrderItem.objects.filter(order=order)
    context = {'order' : order,'orders' : orders}
    return render(request,"store/orders/view.html",context=context)

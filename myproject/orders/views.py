from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Address
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Checkout page
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum([item.total_price() for item in items])
    return render(request, 'checkout.html', {'items': items, 'total': total})

# Place order
@login_required
def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        total = sum([item.total_price() for item in items])
        address = Address.objects.create(
            user=request.user,
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            postal_code=request.POST['postal_code'],
            country=request.POST['country'],
            phone=request.POST['phone'],
        )
        order = Order.objects.create(user=request.user, address=address, total_price=total)
        for item in items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            item.product.stock -= item.quantity
            item.product.save()
        items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_history')
    return redirect('checkout')

# Order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

# Order tracking
@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_tracking.html', {'order': order})

# Order detail
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'items': items})

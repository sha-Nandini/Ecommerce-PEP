from .models import Wishlist
from django.contrib.auth.decorators import login_required
# Wishlist page
@login_required
def wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, 'wishlist.html', {'products': products})

# Add to wishlist
@login_required
def add_to_wishlist(request, product_id):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.add(product)
    return JsonResponse({'status': 'success'})

# Remove from wishlist
@login_required
def remove_from_wishlist(request, product_id):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    return JsonResponse({'status': 'success'})
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

# @login_required
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)

#     CartItem.objects.get_or_create(
#     cart=cart,
#     product=product

#     )

#     if not created:
#         cart_item = CartItem.objects.get(cart=cart, product=product)
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('view_cart')


@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum([item.total_price() for item in items])

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


@login_required
def remove_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('view_cart')

# @login_required
# def add_to_cart(request, product_id):

#     product = get_object_or_404(Product, id=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)

#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product
#     )

#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return JsonResponse({
#         "status": "success",
#         "quantity": cart_item.quantity
#     })

from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Calculate total cart count
        cart_count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))

        return JsonResponse({
            "status": "success",
            "cart_count": cart_count
        })

    return JsonResponse({"status": "error"})
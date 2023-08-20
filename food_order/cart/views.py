from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart,CartItem
from food.models import Dish


@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        "cart":cart,
        "cart_items":cart_items
    }
    return render(request,"cart/view_cart.html",context)

@login_required
def add_to_cart(request,dish_id):
    dish = get_object_or_404(Dish,pk=dish_id)
    cart = Cart.objects.filter(user=request.user).first()

    # Check if the dish is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, dish=dish)
    
    if not item_created:
        # If the dish is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    
    cart.total_price += dish.price
    cart.save()
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if cart_item.cart.user == request.user:
        cart = cart_item.cart
        dish_price = cart_item.dish.price * cart_item.quantity
        
        # Update the cart's total price
        cart.total_price -= dish_price
        cart.save()
        
        # Delete the cart item
        cart_item.delete()

    
    return redirect('view_cart')



@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if cart_item.cart.user == request.user:
        new_quantity = int(request.POST.get(str(cart_item_id), 0))
        
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            
            # Update cart total manually
            cart = cart_item.cart
            cart_items = cart.cartitem_set.all()
            cart.total_price = sum(item.dish.price * item.quantity for item in cart_items)
            cart.save()
        else:
            cart_item.delete()
    
    return redirect('view_cart')
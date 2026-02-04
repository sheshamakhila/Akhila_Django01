from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import CartItem, Product
from .forms import CheckoutForm
from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'Ecommerce/home.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    cart_item.quantity = cart_item.quantity + 1 if not created else 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()

    elif action == 'decrease':
        cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    return redirect('cart_view')

# def update_cart_quantity(request, item_id):
#     cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
#     action = request.POST.get('action')
#
#     if action == 'increase':
#         cart_item.quantity += 1
#
#     elif action == 'decrease' and cart_item.quantity > 1:
#         cart_item.quantity -= 1
#
#     cart_item.save()
#     return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(Decimal(item.product.price) * item.quantity for item in cart_items)

    final_total, discount = calculate_discount(request.user, total)

    return render(request, 'Ecommerce/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'final_total': final_total,
        'discount_rate': int(discount * 100),
    })

def calculate_discount(user=None, total_amount=Decimal('0.00'), dob=None):
    """
    Calculate discount and final total.
    Priority:
      1) If dob provided (or user.profile.date_of_birth exists) and it's the current month -> 10% discount
      2) Else if total_amount >= 10000 -> 5% discount
    """
    discount = Decimal('0.00')
    now = datetime.now()

    # Use provided dob if available, otherwise try to get from user's profile
    if dob is None and user is not None:
        profile = getattr(user, 'profile', None)
        dob = getattr(profile, 'date_of_birth', None)

    if dob and dob.month == now.month:
        discount = Decimal('0.10')
    elif total_amount >= Decimal('10000'):
        discount = Decimal('0.05')

    final_total = total_amount * (Decimal('1.00') - discount)
    return round(final_total, 2), discount

@login_required
def checkout(request):
    form = CheckoutForm(request.POST or None)
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
    # initial values (use profile if present)
    initial_final_total, initial_applied_discount = calculate_discount(request.user, total)
    final_total = initial_final_total
    applied_discount = initial_applied_discount

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        # compute discount using provided DOB if available (form dob takes precedence)
        final_total, applied_discount = calculate_discount(request.user, total, dob=data.get('dob'))

        context = {
            'name': data['full_name'],
            'address_line1': data['address_line1'],
            'address_line2': data['address_line2'],
            'landmark': data['landmark'],
            'city': data['city'],
            'state': data['state'],
            'pin_code': data['pin_code'],
            'country': data['country'],
            'payment_method': data['payment_method'],
            'emi_duration': data['emi_duration'] if data['payment_method'] == 'emi' else None,
            'original_total': total,
            'discount_rate': int(applied_discount * 100),
            'final_total': final_total,
            'form': form,
        }

        # 🎉 Clear user's cart after successful checkout
        cart_items.delete()
        return render(request, 'Ecommerce/thank_you.html', context)

    return render(request, 'Ecommerce/checkout.html', {
        'original_total': total,
        'discount_rate': int(applied_discount * 100),
        'final_total': final_total,
        'form': form,
    })

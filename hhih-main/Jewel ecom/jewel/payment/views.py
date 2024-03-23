
# views.py
@csrf_protect
@login_required(login_url='signin')
def checkout(request):
    user_addresses = Address.objects.filter(user=request.user)
    user_cart = Cart.objects.get(user=request.user)
    applicable_coupons = []
    discounted_total = None

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        selected_address = Address.objects.get(id=selected_address_id)
        selected_coupon_code = request.POST.get('coupon_code', None)

        # Check if the cart has items before creating the order
        if user_cart.items.exists():
            order_amount = int(user_cart.total_cart_value() * 100)  # Convert to paise

            # Apply coupon discount if a coupon is selected
            if selected_coupon_code:
                coupon = Coupon.objects.filter(
                    code=selected_coupon_code,
                    is_active=True,
                    valid_from__lte=timezone.now(),
                    valid_until__gte=timezone.now(),
                    minimum_purchase_amount__lte=user_cart.total_cart_value()
                ).first()
                if coupon:
                    order_amount /= 100  # Convert back to the original currency unit (INR)
                    discounted_total = coupon.calculate_discounted_total(
                        coupon.discount_type,
                        order_amount,
                        coupon.discount_amount,
                        coupon.discount_percentage
                        )

        # Update the order_amount with the discounted_total
                    original_total_value =order_amount   
                    order_amount = max(0, discounted_total * 100)  # Convert to paise

        # Set the discounted total in the correct unit (INR)
                    discounted_total = Decimal(discounted_total)

            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            razorpay_order = razorpay_client.order.create({
                'amount': order_amount,
                'currency': 'INR',
                'receipt': f'order_{user_cart.id}',
            })
            razorpay_order_id = razorpay_order['id']

            # Create a new order
            new_order = Order.objects.create(user=request.user, address=selected_address, razorpay_order_id=razorpay_order_id,original_total_value=original_total_value, discounted_total=discounted_total)

            # Copy items from the user's cart to the order
            for cart_item in user_cart.items.all():
                OrderItem.objects.create(
                    order=new_order,
                    product=cart_item.product,
                    size=cart_item.size,
                    quantity=cart_item.quantity
                )

            # Clear the user's cart after creating the order
            user_cart.items.all().delete()

            # Redirect to the order successful page with order ID
            return redirect('payment_page', order_id=new_order.id)

        else:
            messages.warning(request, "Your cart is empty. Add items before checking out.")

    # Get applicable coupons for the user
    applicable_coupons = Coupon.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_until__gte=timezone.now(),
        minimum_purchase_amount__lte=user_cart.total_cart_value()
    )

    context = {
        'user_addresses': user_addresses,
        'user_cart': user_cart,
        'applicable_coupons': applicable_coupons,
        'discounted_total': discounted_total,
    }

    return render(request, 'user/order/checkout.html', context)

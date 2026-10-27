from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate

from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)

from .forms import CustomerRegistrationForm


# =========================================================
# HOME
# SEARCH + CATEGORY + PRICE + AVAILABILITY + FEATURED
# =========================================================

def home(request):

    all_products = Product.objects.all().select_related("category")

    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    ).select_related("category")

    # =====================================================
    # SEARCH
    # =====================================================

    search_query = request.GET.get("search", "").strip()

    if search_query:
        all_products = all_products.filter(
            name__icontains=search_query
        )

    # =====================================================
    # CATEGORY
    # =====================================================

    category = request.GET.get("category", "").strip()

    if category:
        all_products = all_products.filter(
            category__name__iexact=category
        )

    # =====================================================
    # MIN PRICE
    # =====================================================

    min_price = request.GET.get("min_price", "").strip()

    if min_price:
        try:
            min_price_decimal = Decimal(min_price)

            all_products = all_products.filter(
                price__gte=min_price_decimal
            )

        except (ValueError, TypeError):
            min_price = ""

    # =====================================================
    # MAX PRICE
    # =====================================================

    max_price = request.GET.get("max_price", "").strip()

    if max_price:
        try:
            max_price_decimal = Decimal(max_price)

            all_products = all_products.filter(
                price__lte=max_price_decimal
            )

        except (ValueError, TypeError):
            max_price = ""

    # =====================================================
    # AVAILABILITY
    # =====================================================

    availability = request.GET.get(
        "availability",
        ""
    ).strip()

    if availability == "available":

        all_products = all_products.filter(
            is_available=True
        )

    elif availability == "unavailable":

        all_products = all_products.filter(
            is_available=False
        )

    # =====================================================
    # FEATURED
    # =====================================================

    featured_only = request.GET.get(
        "featured",
        ""
    ).strip()

    if featured_only == "yes":

        all_products = all_products.filter(
            is_featured=True
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        "featured_products": featured_products,
        "all_products": all_products,
        "filtered_products": all_products,

        "search_query": search_query,
        "selected_category": category,

        "min_price": min_price,
        "max_price": max_price,

        "selected_availability": availability,
        "featured_only": featured_only,
    }

    return render(
        request,
        "bakery/home.html",
        context
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        "bakery/product_detail.html",
        {
            "product": product
        }
    )


# =========================================================
# CUSTOMER REGISTRATION
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = CustomerRegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("home")

    else:

        form = CustomerRegistrationForm()

    return render(
        request,
        "bakery/register.html",
        {
            "form": form
        }
    )


# =========================================================
# CUSTOMER LOGIN
# =========================================================

def customer_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("home")

        return render(
            request,
            "bakery/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "bakery/login.html"
    )


# =========================================================
# CUSTOMER LOGOUT
# =========================================================

def customer_logout(request):

    logout(request)

    return redirect("home")


# =========================================================
# CUSTOMER ACCOUNT
# =========================================================

def account(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(
        request,
        "bakery/account.html"
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:

        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# =========================================================
# CART PAGE
# =========================================================

def cart(request):

    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "product"
    )

    total = cart.total_price()

    return render(
        request,
        "bakery/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total": total,
        }
    )


# =========================================================
# INCREASE QUANTITY
# =========================================================

def increase_quantity(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

def decrease_quantity(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    else:

        cart_item.delete()

    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):

    if not request.user.is_authenticated:
        return redirect("login")

    # =====================================================
    # GET USER CART
    # =====================================================

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "product"
    )

    # =====================================================
    # EMPTY CART
    # =====================================================

    if not cart_items.exists():
        return redirect("cart")

    # =====================================================
    # TOTAL
    # =====================================================

    total = cart.total_price()

    # =====================================================
    # POST - PLACE ORDER
    # =====================================================

    if request.method == "POST":

        # =================================================
        # CUSTOMER DETAILS
        # IMPORTANT:
        # checkout.html uses full_name
        # =================================================

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        # =================================================
        # PAYMENT METHOD
        # =================================================

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        ).strip()

        # =================================================
        # VALIDATION
        # =================================================

        if not full_name:

            return render(
                request,
                "bakery/checkout.html",
                {
                    "cart": cart,
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter your full name.",
                }
            )

        if not phone:

            return render(
                request,
                "bakery/checkout.html",
                {
                    "cart": cart,
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter your phone number.",
                }
            )

        if not address:

            return render(
                request,
                "bakery/checkout.html",
                {
                    "cart": cart,
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter your delivery address.",
                }
            )

        if not city:

            return render(
                request,
                "bakery/checkout.html",
                {
                    "cart": cart,
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter your city.",
                }
            )

        if not pincode:

            return render(
                request,
                "bakery/checkout.html",
                {
                    "cart": cart,
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter your pincode.",
                }
            )

        # =================================================
        # PAYMENT METHOD VALIDATION
        # =================================================

        if payment_method not in [
            "COD",
            "ONLINE"
        ]:

            payment_method = "COD"

        # =================================================
        # PAYMENT STATUS
        # =================================================

        # COD:
        # Payment will be collected later.

        # ONLINE:
        # Real payment gateway is not connected yet,
        # so status remains PENDING.

        payment_status = "PENDING"

        # =================================================
        # CREATE ORDER
        # =================================================

        order = Order.objects.create(

            user=request.user,

            full_name=full_name,

            phone=phone,

            address=address,

            city=city,

            pincode=pincode,

            total_amount=total,

            payment_method=payment_method,

            payment_status=payment_status,

            status="PENDING",
        )

        # =================================================
        # CREATE ORDER ITEMS
        # =================================================

        for cart_item in cart_items:

            OrderItem.objects.create(

                order=order,

                product=cart_item.product,

                quantity=cart_item.quantity,

                price=cart_item.product.price,
            )

        # =================================================
        # CLEAR CART
        # =================================================

        cart.items.all().delete()

        # =================================================
        # ORDER CONFIRMATION
        # =================================================

        return redirect(
            "order_confirmation",
            order_id=order.id
        )

    # =====================================================
    # GET - CHECKOUT PAGE
    # =====================================================

    return render(
        request,
        "bakery/checkout.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total": total,
        }
    )


# =========================================================
# ORDER CONFIRMATION
# =========================================================

def order_confirmation(request, order_id):

    if not request.user.is_authenticated:
        return redirect("login")

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "bakery/order_confirmation.html",
        {
            "order": order
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

def my_orders(request):

    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items__product"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "bakery/my_orders.html",
        {
            "orders": orders
        }
    )


# =========================================================
# ORDER DETAILS
# =========================================================

def order_detail(request, order_id):

    if not request.user.is_authenticated:
        return redirect("login")

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "bakery/order_detail.html",
        {
            "order": order
        }
    )
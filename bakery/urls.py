from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # PRODUCT
    # =====================================================

    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),


    # =====================================================
    # ACCOUNT
    # =====================================================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.customer_login,
        name="login"
    ),

    path(
        "logout/",
        views.customer_logout,
        name="logout"
    ),

    path(
        "account/",
        views.account,
        name="account"
    ),


    # =====================================================
    # CART
    # =====================================================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/increase/<int:item_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    path(
        "cart/decrease/<int:item_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),

    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),


    # =====================================================
    # CHECKOUT
    # =====================================================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =====================================================
    # ORDER CONFIRMATION
    # =====================================================

    path(
        "order-confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order_confirmation"
    ),


    # =====================================================
    # MY ORDERS
    # =====================================================

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),


    # =====================================================
    # ORDER DETAILS
    # =====================================================

    path(
        "order-detail/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

]
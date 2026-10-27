from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "description",
    )

    search_fields = (
        "name",
    )


# =========================================================
# PRODUCT ADMIN
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "is_available",
        "is_featured",
    )

    list_filter = (
        "category",
        "is_available",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
    )


# =========================================================
# CART ADMIN
# =========================================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "created_at",
        "total",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    def total(self, obj):
        return obj.total_price()

    total.short_description = "Total Price"


# =========================================================
# CART ITEM ADMIN
# =========================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        "total",
    )

    search_fields = (
        "product__name",
        "cart__user__username",
    )

    def total(self, obj):
        return obj.total_price()

    total.short_description = "Total Price"


# =========================================================
# ORDER ADMIN
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "user__username",
        "user__email",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# ORDER ITEM ADMIN
# =========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "total",
    )

    search_fields = (
        "product__name",
        "order__full_name",
    )

    def total(self, obj):
        return obj.total_price()

    total.short_description = "Total Price"


# =========================================================
# USER ADMIN
# =========================================================

# Django already registers User by default.
# We unregister it first so we can register it with UserAdmin.

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
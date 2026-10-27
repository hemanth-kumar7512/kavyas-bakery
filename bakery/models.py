from django.db import models
from django.contrib.auth.models import User


# =========================================================
# CATEGORY
# =========================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT
# =========================================================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    # =====================================================
    # AVAILABILITY
    # =====================================================

    is_available = models.BooleanField(
        default=True
    )

    # =====================================================
    # FEATURED
    # =====================================================

    is_featured = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name


# =========================================================
# CART
# =========================================================

class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_price(self):

        return sum(
            item.total_price()
            for item in self.items.all()
        )


# =========================================================
# CART ITEM
# =========================================================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):

        return f"{self.product.name} x {self.quantity}"

    def total_price(self):

        return self.product.price * self.quantity


# =========================================================
# ORDER
# =========================================================

class Order(models.Model):

    # =====================================================
    # ORDER STATUS
    # =====================================================

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("PREPARING", "Preparing"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    # =====================================================
    # PAYMENT METHOD
    # =====================================================

    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    # =====================================================
    # PAYMENT STATUS
    # =====================================================

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
    ]

    # =====================================================
    # CUSTOMER
    # =====================================================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # =====================================================
    # DELIVERY DETAILS
    # =====================================================

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    # =====================================================
    # ORDER TOTAL
    # =====================================================

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # =====================================================
    # PAYMENT METHOD
    # =====================================================

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    # =====================================================
    # PAYMENT STATUS
    # =====================================================

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    # =====================================================
    # ORDER STATUS
    # =====================================================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    # =====================================================
    # CREATED DATE
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    def __str__(self):

        return f"Order #{self.id} - {self.user.username}"


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def total_price(self):

        return self.price * self.quantity

    def __str__(self):

        return f"{self.product.name} x {self.quantity}"
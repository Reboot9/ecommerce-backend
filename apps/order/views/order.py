"""
This module contains handlers for the order app.
"""
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.base.pagination import PaginationCommon
from apps.order.models.order import Order
from apps.order.serializers.order import OrderSerializer
from apps.payment.services import Payment


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with order."""

    http_method_names = ["get", "post", "patch", "head", "options", "trace"]
    serializer_class = OrderSerializer
    pagination_class = PaginationCommon

    def get_permissions(self):
        """Set permissions based on the action."""
        if self.action in ["list", "retrieve"]:
            # Allow access only to authenticated users for listing and retrieving orders.
            return [permissions.IsAuthenticated()]
        elif self.action in ["patch"]:
            return [permissions.IsAdminUser()]
        else:
            # Allow any user to perform other actions.
            return [permissions.AllowAny()]

    def get_queryset(self):
        """Get orders based on the user's email."""
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Order.objects.all()
            return Order.objects.filter(email=user.email)
        else:
            # return an empty queryset if user is not authenticated
            return Order.objects.none()

    def get_object(self):
        """
        Retrieve a single order based on the user and order ID.
        """
        user = self.request.user
        order_id = self.kwargs.get("pk")

        if not isinstance(user, AnonymousUser):
            # If the user is authenticated, retrieve the order based on the user's email
            return get_object_or_404(Order, email=user.email, pk=order_id)
        else:
            # If the user is not authenticated, retrieve the order based on the email
            # provided in the order data

            # Note that this condition won't work because of get_permissions() method.
            order_email = self.request.data.get("email")
            if not order_email:
                raise ValidationError("Email is required for unauthenticated requests.")
            return get_object_or_404(Order, email=order_email, pk=order_id)

    def create(self, request, *args, **kwargs):
        """Handle creating a new order."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def pay(self, request, pk):
        """
        Initiate payment for a specific order.

        :param request: HTTP request object.
        :param pk: Primary key of the order.
        :return: Response with payment URL.
        """
        order_instance = self.get_object()
        cost = str(order_instance.total_order_price)
        order_id = str(order_instance.id)

        liqpay = Payment()
        payment_response = liqpay.generate_new_url_for_pay(order_id, cost)

        return Response(payment_response)

    @action(detail=False, methods=["GET"])
    def callback(self, request):
        """
        Receive payment status callback and update order status accordingly.

        :param request: HTTP request object.
        :return: Response confirming payment status update.
        """
        order_id = request.query_params.get("order_id")
        if not order_id:
            return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # receive payment status from payment gateway
        liqpay = Payment()
        response = liqpay.get_order_status_from_liqpay(order_id)

        if response and response.get("result") == "ok":
            order_instance = get_object_or_404(Order, pk=order_id)
            order_instance.is_paid = True
            order_instance.status = Order.OrderStatusChoices.PROCESSING
            order_instance.save()

            serializer = OrderSerializer(order_instance)
            return Response(
                {"message": "Payment was successful.", "order": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Payment status not received or invalid."},
            status=status.HTTP_400_BAD_REQUEST,
        )

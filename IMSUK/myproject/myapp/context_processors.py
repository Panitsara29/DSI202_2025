from .models import CartItem, Notification

def cart_item_count(request):
    if request.user.is_authenticated:
        total_qty = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
        return {'cart_item_count': total_qty}
    return {'cart_item_count': 0}

def notification_unread_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notification_unread_count': count}
    return {'notification_unread_count': 0}

from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        total_qty = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
        return {'cart_item_count': total_qty}
    return {'cart_item_count': 0}

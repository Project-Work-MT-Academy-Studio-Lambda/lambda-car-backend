from domain.refueling import Refueling
from uuid import UUID

def refueling_to_dynamodb_item(refueling: Refueling) -> dict:
    return {
        'id': str(refueling.id),
        'trip_id': str(refueling.trip_id),
        'cart_number': refueling.cart_number,
        'liter_price': refueling.liter_price,
        'liters': refueling.liters,
        'receipt_photo': refueling.receipt_photo,
    }

def dynamodb_item_to_refueling(item: dict) -> Refueling:
    return Refueling(
        id=UUID(item['id']),
        trip_id=UUID(item['trip_id']),
        cart_number=item['cart_number'],
        liter_price=item['liter_price'],
        liters=item['liters'],
        receipt_photo=item['receipt_photo']
    )
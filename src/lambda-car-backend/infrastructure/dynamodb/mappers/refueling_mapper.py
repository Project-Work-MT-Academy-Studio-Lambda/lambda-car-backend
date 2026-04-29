from domain.refueling import Refueling
from uuid import UUID

def refueling_to_item(refueling: Refueling) -> dict:
    return {
        'id': str(refueling.id),
        'car_id': str(refueling.car_id),
        'card_number': refueling.card_number,
        'liter_price': refueling.liter_price,
        'liters': refueling.liters,
        'receipt_photo': refueling.receipt_photo,
    }

def item_to_refueling(item: dict) -> Refueling:
    return Refueling(
        id=UUID(item['id']),
        car_id=UUID(item['car_id']),
        card_number=item['card_number'],
        liter_price=item['liter_price'],
        liters=item['liters'],
        receipt_photo=item['receipt_photo']
    )
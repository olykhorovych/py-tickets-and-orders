from django.db import transaction

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order(user=user)
    if date:
        order.created_at = date

    order.save()

    tickets = [
        Ticket(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        ) for ticket in tickets
    ]
    for ticket in tickets:
        ticket.save()

    return order


def get_orders(username: str | None = None) -> list[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.select_related(
            "user").filter(user__username=username)
    return queryset

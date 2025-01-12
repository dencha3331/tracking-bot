__all__ = (
    "command_router",
    "message_delete_router",
    "payments_router",
)

from handlers.message_delete_handlers import message_delete_router
from handlers.commands import command_router
from handlers.payment_handlers import payments_router

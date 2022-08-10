from enum import Enum

class OrderStatusValues(str, Enum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    IN_PROCESS = "In process"
    DELIVERED = "Delivered"
    COMPLETED = "Completed"
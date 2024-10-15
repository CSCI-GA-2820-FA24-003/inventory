"""
Test Factory to make fake objects for testing
"""

import factory
from service.models import Inventory, Condition


class InventoryFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Inventory

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    quantity = factory.Sequence(lambda n: n)
    restock_level = factory.LazyAttribute(lambda obj: int(obj.quantity * 0.2))
    condition = factory.Iterator(Condition)

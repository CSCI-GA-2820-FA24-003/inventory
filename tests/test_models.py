######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Inventory Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Inventory, DataValidationError, db
from .factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  INVENTORY   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestInventory(TestCase):
    """Test Cases for Inventory Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_inventory(self):
        """It should create a Inventory"""
        inventory = InventoryFactory()
        inventory.create()
        self.assertIsNotNone(inventory.id)
        found = Inventory.all()
        self.assertEqual(len(found), 1)
        data = Inventory.find(inventory.id)
        self.assertEqual(data.name, inventory.name)
        self.assertEqual(data.quantity, inventory.quantity)
        self.assertEqual(data.restock_level, inventory.restock_level)
        self.assertEqual(data.condition, inventory.condition)

    # Todo: Add your test cases here...


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestInventory):
    """Inventory Model Query Tests"""

    def test_find_inventory(self):
        """It should Find a Inventory by ID"""
        inventories = InventoryFactory.create_batch(5)
        for inventory in inventories:
            inventory.create()
        logging.debug(inventories)
        # make sure they got saved
        self.assertEqual(len(Inventory.all()), 5)
        # find the 2nd inventory in the list
        inventory = Inventory.find(inventories[1].id)
        self.assertIsNot(inventory, None)
        self.assertEqual(inventory.id, inventories[1].id)
        self.assertEqual(inventory.name, inventories[1].name)
        self.assertEqual(inventory.quantity, inventories[1].quantity)
        self.assertEqual(inventory.condition, inventories[1].condition)
        self.assertEqual(inventory.restock_level, inventories[1].restock_level)

    def test_find_by_restock_level(self):
        """It should Find Inventories by Restock Level"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        restock_level = inventories[0].restock_level
        count = len([inventory for inventory in inventories if inventory.restock_level == restock_level])
        found = Inventory.find_by_restock_level(restock_level)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.restock_level, restock_level)

    def test_find_by_name(self):
        """It should Find a Inventory by Name"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        name = inventories[0].name
        count = len([inventory for inventory in inventories if inventory.name == name])
        found = Inventory.find_by_name(name)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.name, name)

    def test_find_by_quantity(self):
        """It should Find Inventories by Quantity"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        quantity = inventories[0].quantity
        count = len([inventory for inventory in inventories if inventory.quantity == quantity])
        found = Inventory.find_by_quantity(quantity)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.quantity, quantity)

    def test_find_by_condition(self):
        """It should Find Inventories by Condition"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        condition = inventories[0].condition
        count = len([inventory for inventory in inventories if inventory.condition == condition])
        found = Inventory.find_by_condition(condition)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.condition, condition)
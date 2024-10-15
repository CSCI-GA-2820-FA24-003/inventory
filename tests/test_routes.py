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
TestInventory API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from unittest.mock import patch, MagicMock
from wsgi import app
from service.common import status
from service.models import db, Inventory, DataValidationError
from .factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/inventories"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Inventory REST API Service")
        self.assertEqual(data["version"], "1.0")

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_inventory(self):
        """It should Create a new Inventory"""
        test_inventory = InventoryFactory()
        logging.debug("Test Inventory: %s", test_inventory.serialize())
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_inventory = response.get_json()
        self.assertEqual(new_inventory["name"], test_inventory.name)
        self.assertEqual(new_inventory["quantity"], test_inventory.quantity)
        self.assertEqual(new_inventory["restock_level"], test_inventory.restock_level)
        self.assertEqual(new_inventory["condition"], test_inventory.condition.name)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_inventory = response.get_json()
        self.assertEqual(new_inventory["name"], test_inventory.name)
        self.assertEqual(new_inventory["quantity"], test_inventory.quantity)
        self.assertEqual(new_inventory["restock_level"], test_inventory.restock_level)
        self.assertEqual(new_inventory["condition"], test_inventory.condition.name)

    def test_get_inventory(self):
        """It should Get a single Inventory"""
        # get the id of a inventory
        test_inventory = self._create_inventories(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_inventory.name)

    def test_get_inventory_not_found(self):
        """It should not Get a Inventory thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_inventory_list(self):
        """It should Get a list of inventories"""
        self._create_inventories(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_by_name(self):
        """It should Query Inventory by name"""
        inventories = self._create_inventories(5)
        test_name = inventories[0].name
        name_count = len([inventory for inventory in inventories if inventory.name == test_name])
        response = self.client.get(
            BASE_URL, query_string=f"name={test_name}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for inventory in data:
            self.assertEqual(inventory["name"], test_name)

    def test_query_by_quantity(self):
        """It should Query Inventories by Category"""
        inventories = self._create_inventories(10)
        test_quantity = inventories[0].quantity
        quantity_inventories = [inventory for inventory in inventories if inventory.quantity == test_quantity]
        response = self.client.get(
            BASE_URL,
            query_string=f"quantity={test_quantity}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(quantity_inventories))
        # check the data just to be sure
        for inventory in data:
            self.assertEqual(inventory["quantity"], test_quantity)

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_inventory(self):
        """It should Update an existing Inventory"""
        # create a inventory to update
        test_inventory = InventoryFactory()
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the inventory
        new_inventory = response.get_json()
        logging.debug(new_inventory)
        new_inventory["quantity"] = new_inventory["quantity"] + 100
        temp = new_inventory["quantity"]
        response = self.client.put(
            f"{BASE_URL}/{new_inventory['id']}", json=new_inventory
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_inventory = response.get_json()
        self.assertEqual(updated_inventory["quantity"], temp)

    def test_wrong_media(self):
        """It test how the system handle wrong media type request"""
        test_inventory = InventoryFactory()
        response = self.client.post(BASE_URL, data=test_inventory.serialize())   # send as form type
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_unknown_method(self):
        """It test how the system handle a request with unexpected method"""
        test_inventory = InventoryFactory()
        json = test_inventory.serialize()
        json["unknown"] = "unknown"
        response = self.client.post(BASE_URL, json=json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    ############################################################
    # Utility function to bulk create inventories
    ############################################################
    def _create_inventories(self, count: int = 1) -> list:
        """Factory method to create inventories in bulk"""
        inventories = []
        for _ in range(count):
            test_inventory = InventoryFactory()
            response = self.client.post(BASE_URL, json=test_inventory.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test inventory"
            )
            new_inventory = response.get_json()
            test_inventory.id = new_inventory["id"]
            inventories.append(test_inventory)
        return inventories


class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a Inventory id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_internal_error(self):
        """It test that there is something wrong on server side"""
        response = self.client.get("/error_test")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    ######################################################################
    #  T E S T   M O C K S
    ######################################################################

    @patch('service.routes.Inventory.find_by_name')
    def test_bad_request(self, bad_request_mock):
        """It should return a Bad Request error from Find By Name"""
        bad_request_mock.side_effect = DataValidationError()
        response = self.client.get(BASE_URL, query_string='name=fido')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('service.routes.Inventory.find_by_name')
    def test_mock_search_data(self, pet_find_mock):
        """It should showing how to mock data"""
        pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
        response = self.client.get(BASE_URL, query_string='name=fido')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

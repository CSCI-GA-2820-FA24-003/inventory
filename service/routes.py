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
Inventory Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Inventory

Paths:
------
GET / - Displays a UI for Selenium testing
GET /inventories - Returns a list of all Inventories
GET /inventories/{inventory_id} - Returns the Inventory with the given ID
GET /health - Performs a health check to ensure the server is running properly
GET /error_test - Triggers a server internal error for testing purposes
POST /inventories - Creates a new Inventory record in the database
PUT /inventories/{inventory_id} - Updates an Inventory record with the given ID
PUT /inventories/{inventory_id}/start_restock - Starts the restocking process for the Inventory
PUT /inventories/{inventory_id}/stop_restock - Stops the restocking process for the Inventory
DELETE /inventories/{inventory_id} - Deletes an Inventory record with the given ID
"""
# pylint: disable=cyclic-import
from flask import jsonify, abort
from flask import current_app as app  # Import Flask application
from flask_restx import Resource, fields, reqparse
from service.models import Inventory, Condition
from service.common import status  # HTTP Status Codes
from . import api


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


# Define model so that docs reflect what can be passed in
create_model = api.model(
    "Inventory",
    {
        "name": fields.String(
            required=False,
            description="The name of the Inventory item",
        ),
        "quantity": fields.Integer(
            required=True,
            description="The quantity of the Inventory item",
        ),
        "restock_level": fields.Integer(
            required=True,
            description="The restock level of the Inventory item",
        ),
        # pylint: disable=protected-access
        "condition": fields.String(
            required=True,
            description="The condition of the Inventory item (New, Open Box, Used)",
            enum=Condition._member_names_,
        ),
        "restocking_available": fields.Boolean(
            required=True,
            description="The availability of the Inventory item",
        ),
    },
)

inventory_model = api.inherit(
    "InventoryModel",
    create_model,
    {
        "id": fields.String(
            readOnly=True,
            description="The unique id assigned internally by the service",
        )
    },
)

# query string argumnets
inventory_args = reqparse.RequestParser()
inventory_args.add_argument(
    "name", type=str, location="args", required=False, help="List inventories by name"
)
inventory_args.add_argument(
    "quantity",
    type=int,
    location="args",
    required=False,
    help="List inventories by quantity",
)
inventory_args.add_argument(
    "restock_level",
    type=int,
    location="args",
    required=False,
    help="List inventories by restock level",
)
inventory_args.add_argument(
    "condition",
    type=str,
    location="args",
    required=False,
    choices=Condition._member_names_,
    help="List inventories by condition",
)
inventory_args.add_argument(
    "restocking_available",
    type=str,
    location="args",
    required=False,
    help="List inventories by restocking availability",
)


######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
#  PATH: /inventories
######################################################################
@api.route("/inventories")
class InventoryCollection(Resource):
    """Handles all interactions with collections of Inventories"""

    # ------------------------------------------------------------------
    # LIST ALL INVENTORIES
    # ------------------------------------------------------------------
    @api.doc("list_inventories")
    @api.expect(inventory_args, validate=True)
    @api.marshal_list_with(inventory_model)
    def get(self):
        """Returns all of the Inventories"""
        app.logger.info("Request to list Inventories...")
        inventories = []
        args = inventory_args.parse_args()
        if args["name"]:
            app.logger.info("Filtering by name: %s", args["name"])
            inventories = Inventory.find_by_name(args["name"])
        elif args["quantity"]:
            app.logger.info("Filtering by quantity: %s", args["quantity"])
            quantity = int(args["quantity"])
            inventories = Inventory.find_by_quantity(quantity)
        elif args["restock_level"]:
            app.logger.info("Filtering by restock level: %s", args["restock_level"])
            restock_level = int(args["restock_level"])
            inventories = Inventory.find_by_restock_level(restock_level)
        elif args["condition"]:
            app.logger.info("Filtering by condition: %s", args["condition"])
            condition_enum = Condition(args["condition"].upper())
            inventories = Inventory.find_by_condition(condition_enum)
        elif args["restocking_available"]:
            app.logger.info(
                "Filtering by restocking availability: %s", args["restocking_available"]
            )
            restocking_available = args["restocking_available"].lower() in [
                "true",
                "yes",
                "1",
            ]
            inventories = Inventory.find_by_restocking_available(restocking_available)
        else:
            app.logger.info("Finding all inventories")
            inventories = Inventory.all()

        results = [inventory.serialize() for inventory in inventories]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # CREATE A NEW INVENTORY
    # ------------------------------------------------------------------
    @api.doc("create_inventories")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(inventory_model, code=201)
    def post(self):
        """
        Creates an Inventory
        This endpoint will create an Inventory based the data in the body that is posted
        """
        app.logger.info("Request to Create an Inventory")
        inventory = Inventory()
        app.logger.debug("Payload = %s", api.payload)
        app.logger.info(api.payload)
        inventory.deserialize(api.payload)
        inventory.create()
        app.logger.info("Inventory with new id [%s] created!", inventory.id)
        app.logger.info(inventory.serialize())
        location_url = api.url_for(
            InventoryResource, inventory_id=inventory.id, _external=True
        )
        return (
            inventory.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )


######################################################################
#  PATH: /inventories/{id}
######################################################################
@api.route("/inventories/<inventory_id>")
@api.param("inventory_id", "The Inventory identifier")
class InventoryResource(Resource):
    """
    InventoryResource class

    Allows the manipulation of a single Inventory
    GET /inventories/{inventory_id} - Returns the Inventory with given id
    PUT /inventories/{inventory_id} - updates a Inventory record with given id
    DELETE /inventories/{inventory_id} - deletes a Inventory record with given id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN INVENTORY
    # ------------------------------------------------------------------
    @api.doc("get_inventories")
    @api.response(404, "Inventory not found")
    @api.marshal_with(inventory_model)
    def get(self, inventory_id):
        """
        Retrieve a single Inventory

        This endpoint will return an Inventory based on its id
        """
        app.logger.info("Request to Retrieve an inventory with id [%s]", inventory_id)
        inventory = Inventory.find(inventory_id)
        if not inventory:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' was not found.",
            )
        return inventory.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING INVENTORY
    # ------------------------------------------------------------------
    @api.doc("update_inventories")
    @api.response(404, "Inventory not found")
    @api.response(400, "The posted Inventory data was not valid")
    @api.expect(inventory_model)
    @api.marshal_with(inventory_model)
    def put(self, inventory_id):
        """
        Update an Inventory

        This endpoint will update a Inventory based the body that is posted
        """
        app.logger.info("Request to Update an inventory with id [%s]", inventory_id)
        inventory = Inventory.find(inventory_id)
        if not inventory:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' not found.",
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        inventory.deserialize(data)
        inventory.id = inventory_id
        inventory.update()
        return inventory.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN INVENTORY
    # ------------------------------------------------------------------
    @api.doc("delete_inventories")
    @api.response(204, "Inventory deleted")
    def delete(self, inventory_id):
        """
        Delete an Inventory

        This endpoint will delete an Inventory based the id specified in the path
        """
        app.logger.info("Request to Delete an inventory with id [%s]", inventory_id)
        inventory = Inventory.find(inventory_id)
        if inventory:
            inventory.delete()
            app.logger.info("Inventory with id [%s] was deleted", inventory_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventories/<inventory_id>/start_restock
######################################################################
@api.route("/inventories/<int:inventory_id>/start_restock")
@api.param("inventory_id", "The Inventory identifier")
class InventoryStartRestock(Resource):
    """Handles the start restocking process for a single Inventory"""

    @api.doc("start_restock_inventories")
    @api.response(404, "Inventory not found")
    @api.response(409, "Inventory is not available for restocking")
    @api.marshal_with(inventory_model, code=200)
    def put(self, inventory_id):
        """
        Start Restocking an Inventory

        This endpoint marks the inventory as being restocked, making it unavailable.
        """
        app.logger.info(
            "Request to start restocking inventory with id: %d", inventory_id
        )

        # Attempt to find the Inventory and abort if not found
        inventory = Inventory.find(inventory_id)
        if not inventory:
            app.logger.warning("Inventory with id '%d' not found.", inventory_id)
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' was not found.",
            )

        # You can only restock inventory that is available
        if not inventory.restocking_available:
            app.logger.warning(
                "Inventory with id '%d' is not available for restocking.", inventory_id
            )
            abort(
                status.HTTP_409_CONFLICT,
                f"Inventory with id '{inventory_id}' is not available.",
            )

        # Execute restocking logic (currently setting to unavailable)
        inventory.restocking_available = False
        inventory.update()

        app.logger.info("Inventory with ID: %d has started restocking.", inventory_id)
        return inventory.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /inventories/<inventory_id>/stop_restock
######################################################################
@api.route("/inventories/<int:inventory_id>/stop_restock")
@api.param("inventory_id", "The Inventory identifier")
class InventoryStopRestock(Resource):
    """Handles the stop restocking process for a single Inventory"""

    @api.doc("stop_restock_inventories")
    @api.response(404, "Inventory not found")
    @api.response(409, "Inventory is already available")
    @api.marshal_with(inventory_model, code=200)
    def put(self, inventory_id):
        """
        Stop Restocking an Inventory

        This endpoint marks the inventory as available after restocking.
        """
        app.logger.info(
            "Request to stop restocking inventory with id: %d", inventory_id
        )

        # Attempt to find the Inventory and abort if not found
        inventory = Inventory.find(inventory_id)
        if not inventory:
            app.logger.warning("Inventory with id '%d' not found.", inventory_id)
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' was not found.",
            )

        # You can only stop restocking if the inventory is currently not available
        if inventory.restocking_available:
            app.logger.warning(
                "Inventory with id '%d' is already available.", inventory_id
            )
            abort(
                status.HTTP_409_CONFLICT,
                f"Inventory with id '{inventory_id}' is already available.",
            )

        # Execute logic to finish restocking (currently setting to available)
        inventory.restocking_available = True
        inventory.update()

        app.logger.info("Inventory with ID: %d has finished restocking.", inventory_id)
        return inventory.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /error_test
######################################################################
@api.route("/error_test")
class ErrorTest(Resource):
    """Endpoint to test server internal errors"""

    @api.doc("error_test")
    @api.response(500, "Internal Server Error")
    def get(self):
        """
        Test Server Internal Error

        This endpoint will directly return a HTTP 500 error to simulate a server-side issue.
        """
        app.logger.info("Request to trigger an internal server error.")
        abort(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Internal Server Error",
        )

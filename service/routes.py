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
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Inventory, Condition
from service.common import status  # HTTP Status Codes


######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


######################################################################
# GET INDEX
######################################################################
# @app.route("/")
# def index():
#     """Root URL response"""
#     app.logger.info("Request for Root URL")
#     return (
#         jsonify(
#             name="Inventory REST API Service",
#             version="1.0",
#             paths={
#                 "create_inventory": {
#                     "method": "POST",
#                     "url": url_for("create_inventory", _external=True),
#                 },
#                 "get_inventories": {
#                     "method": "GET",
#                     "url": url_for("get_inventories", inventory_id=0, _external=True),
#                 },
#                 "list_inventories": {
#                     "method": "GET",
#                     "url": url_for("list_inventories", _external=True),
#                 },
#                 "update_inventories": {
#                     "method": "PUT",
#                     "url": url_for(
#                         "update_inventories", inventory_id=0, _external=True
#                     ),
#                 },
#                 "delete_inventories": {
#                     "method": "DELETE",
#                     "url": url_for(
#                         "delete_inventories", inventory_id=0, _external=True
#                     ),
#                 },
#             },
#         ),
#         status.HTTP_200_OK,
#     )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE AN INVENTORY
######################################################################
@app.route("/inventories", methods=["POST"])
def create_inventory():
    """
    Create an inventory
    This endpoint will create an Inventory based the data in the body that is posted
    """
    app.logger.info("Request to Create a Inventory...")
    check_content_type("application/json")

    inventory = Inventory()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    inventory.deserialize(data)

    # Save the new Inventory to the database
    inventory.create()
    app.logger.info("Inventory with new id [%s] saved!", inventory.id)

    # Return the location of the new Inventory

    location_url = url_for("get_inventories", inventory_id=inventory.id, _external=True)
    return (
        jsonify(inventory.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# READ AN INVENTORY
######################################################################
@app.route("/inventories/<int:inventory_id>", methods=["GET"])
def get_inventories(inventory_id):
    """
    Read an inventory
    This endpoint will read an Inventory based on the inventory_id.
    """
    app.logger.info("Request to Retrieve a inventory with id [%s]", inventory_id)

    # Attempt to find the inventory and abort if not found
    inventory = Inventory.find(inventory_id)
    if not inventory:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Inventory item with id '{inventory_id}' was not found.",
        )

    app.logger.info("Returning inventory item: %s", inventory.name)
    return jsonify(inventory.serialize()), status.HTTP_200_OK


def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# LIST ALL INVENTORIES
######################################################################
@app.route("/inventories", methods=["GET"])
def list_inventories():
    """Returns all of the Inventories"""
    app.logger.info("Request for inventory list")

    inventories = []

    # Parse any arguments from the query string
    quantity = request.args.get("quantity")
    name = request.args.get("name")
    restock_level = request.args.get("restock_level")
    condition = request.args.get("condition")

    if quantity:
        app.logger.info("Find by quantity: %s", quantity)
        quantity = int(quantity)
        inventories = Inventory.find_by_quantity(quantity)
    elif name:
        app.logger.info("Find by name: %s", name)
        inventories = Inventory.find_by_name(name)
    elif restock_level:
        app.logger.info("Find by restock_level: %s", restock_level)
        restock_level = int(restock_level)
        inventories = Inventory.find_by_restock_level(restock_level)
    elif condition:
        app.logger.info("Find by condition: %s", condition)
        # create enum from string
        inventories = Inventory.find_by_condition(Condition[condition.upper()])
    else:
        app.logger.info("Find all")
        inventories = Inventory.all()

    results = [inventory.serialize() for inventory in inventories]
    app.logger.info("Returning %d inventories", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING INVENTORY
######################################################################
@app.route("/inventories/<int:inventory_id>", methods=["PUT"])
def update_inventories(inventory_id):
    """
    Update a Inventory

    This endpoint will update a Inventory based the body that is posted
    """
    app.logger.info("Request to Update a inventory with id [%s]", inventory_id)
    check_content_type("application/json")

    # Attempt to find the Inventory and abort if not found
    inventory = Inventory.find(inventory_id)
    if not inventory:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Inventory with id '{inventory_id}' was not found.",
        )

    # Update the Inventory with the new data
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    inventory.deserialize(data)

    # Save the updates to the database
    inventory.update()

    app.logger.info("Inventory with ID: %d updated.", inventory.id)
    return jsonify(inventory.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN EXISTING INVENTORY
######################################################################
@app.route("/inventories/<int:inventory_id>", methods=["DELETE"])
def delete_inventories(inventory_id):
    """
    Delete an inventory

    This endpoint will delete an existing inventory based its inventory_id
    """
    app.logger.info("Request to Delete an Inventory with id [%s]", inventory_id)

    # Find the inventory
    inventory = Inventory.find(inventory_id)
    # If inventory exists, delete it
    if inventory:
        inventory.delete()
        app.logger.info(
            "Inventory with id [%s] as been successfully deleted.", inventory_id
        )
    else:
        app.logger.info("Inventory with id [%s] not found", inventory_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# Start to restock an inventory
######################################################################
@app.route("/inventories/<int:inventory_id>/start_restock", methods=["PUT"])
def restock_inventories(inventory_id):
    """Restocking an inventory makes it unavailable"""
    app.logger.info("Request to restock an inventory with id: %d", inventory_id)

    # Attempt to find the Inventory and abort if not found
    inventory = Inventory.find(inventory_id)
    if not inventory:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Inventory with id '{inventory_id}' was not found.",
        )

    # you can only restock inventory that are available
    if not inventory.restocking_available:
        abort(
            status.HTTP_409_CONFLICT,
            f"Inventory with id '{inventory_id}' is not available.",
        )

    # At this point you would execute code to restock the inventory
    # For the moment, we will just set them to unavailable

    inventory.restocking_available = False
    inventory.update()

    app.logger.info("Inventory with ID: %d has been started restocking.", inventory_id)
    return inventory.serialize(), status.HTTP_200_OK


######################################################################
# TEST SERVER INTERNAL ERROR
######################################################################
@app.route("/error_test", methods=["GET"])
def error_test():
    """
    TEST SERVER INTERNAL ERROR

    This endpoint will directly return a HTTP code 500, indicating something wrong on server side.
    """
    abort(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Internal Server Error",
    )

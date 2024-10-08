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
from service.models import Inventory
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Inventory REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Todo: Place your REST API code here ...

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

@app.route("/inventory", methods=["POST"])
def create_inventories():
    app.logger.info("Request to Create inventory...")
    check_content_type("application/json")

    inventory = Inventory()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    inventory.deserialize(data)

    # Save the new inventory to the database
    inventory.create()
    app.logger.info("inventory with new id [%s] saved!", inventory.id)

    # Return the location of the new inventory
    location_url = url_for("get_inventory", product_id=inventory.id, _external=True)
    return jsonify(inventory.serialize()), status.HTTP_201_CREATED, {"Location": location_url}

@app.route("/inventory/<int:product_id>", methods=["GET"])
def get_inventory(product_id):
    app.logger.info("Request to Retrieve a inventory with id [%s]", product_id)

    # Attempt to find the inventory and abort if not found
    inventory = Inventory.find(product_id)
    if not inventory:
        abort(status.HTTP_404_NOT_FOUND, f"Inventory item with id '{product_id}' was not found.")

    app.logger.info("Returning inventory item: %s", inventory.name)
    return jsonify(inventory.serialize()), status.HTTP_200_OK
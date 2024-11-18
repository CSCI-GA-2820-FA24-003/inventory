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
Inventory Steps

Steps file for Inventory.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from compare3 import expect
from behave import given  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

WAIT_TIMEOUT = 60


@given('the following inventories')
def step_impl(context):
    """ Delete all Inventories and load new ones """

    # Get a list all of the inventories
    rest_endpoint = f"{context.base_url}/inventories"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    expect(context.resp.status_code).equal_to(HTTP_200_OK)
    # and delete them one by one
    for inventory in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{inventory['id']}", timeout=WAIT_TIMEOUT)
        expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)

    # load the database with new inventories
    for row in context.table:
        payload = {
            "name": row['name'],
            "quantity": row['quantity'],
            "restock_level": row['restock level'],
            "condition": row['condition'],
            "restocking_available": row['restocking available'] in ["True", "true", "1"],
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)

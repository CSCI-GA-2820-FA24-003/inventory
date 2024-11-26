"""
Models for Inventory

All of the models are stored in this module
"""

import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Condition(Enum):
    """Enumeration of valid inventory item conditions"""

    NEW = "NEW"
    OPEN_BOX = "OPEN_BOX"
    USED = "USED"


class Inventory(db.Model):
    """
    Class that represents an Inventory
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    restock_level = db.Column(db.Integer, nullable=False)
    condition = db.Column(
        db.Enum(Condition), nullable=False, server_default=(Condition.NEW.name)
    )
    restocking_available = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return f"<Inventory {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Inventory to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Inventory to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Inventory from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Inventory into a dictionary"""
        inventory = {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "restock_level": self.restock_level,
            "condition": self.condition.name,
            "restocking_available": self.restocking_available,
        }
        return inventory

    def deserialize(self, data):
        """
        Deserializes a Inventory from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.quantity = data["quantity"]
            self.restock_level = data["restock_level"]
            self.condition = Condition[
                data["condition"].upper()
            ]  # create enum from string
            self.restocking_available = data["restocking_available"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Inventory: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Inventory: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Inventories in the database"""
        logger.info("Processing all Inventories")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Inventory by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Inventories with the given name

        Args:
            name (string): the name of the Inventories you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_quantity(cls, quantity: int) -> list:
        """Returns all of the Inventories at a given quantity

        :param quantity: the quantity of the Inventories you want to match
        :type quantity: int

        :return: a collection of Inventories of that quantity
        :rtype: list

        """
        logger.info("Processing quantity query for %s ...", quantity)
        return cls.query.filter(cls.quantity == quantity)

    @classmethod
    def find_by_restock_level(cls, restock_level: int) -> list:
        """Returns all Inventories by their restock_level

        :param restock_level: the restock_level of the Inventories you want to match
        :type restock_level: int

        :return: a collection of Inventories of that restock_level
        :rtype: list

        """
        if not isinstance(restock_level, int):
            raise TypeError("Invalid restock_level, must be of type int")
        logger.info("Processing restock_level query for %s ...", restock_level)
        return cls.query.filter(cls.restock_level == restock_level)

    @classmethod
    def find_by_condition(cls, condition: Condition = Condition.NEW) -> list:
        """Returns all Inventories by their Condition

        :param condition: values are ['NEW', 'OPEN_BOX', 'USED']
        :type condition: enum

        :return: a collection of inventories of that condition
        :rtype: list

        """
        if not isinstance(condition, Condition):
            raise TypeError("Invalid condition, must be type Condition")
        logger.info("Processing condition query for %s ...", condition.name)
        return cls.query.filter(cls.condition == condition)

    @classmethod
    def find_by_restocking_available(cls, restocking_available: bool) -> list:
        """Returns all Inventories by their Condition

        :param restocking_available: false for the item that is restocking, true for the item that is not restocking
        :type restocking_available: bool

        :return: a collection of inventories of that restocking_available
        :rtype: list

        """
        if not isinstance(restocking_available, bool):
            raise TypeError("Invalid restocking_available, must be type bool")
        logger.info(
            "Processing restocking_available query for %s ...", restocking_available
        )
        return cls.query.filter(cls.restocking_available == restocking_available)

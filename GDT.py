"""
    GDT
    ~~~

    Stands for "GeoData Thing". It's middleware for a database and a geolocated
    data type.
"""

import dataset
import datetime
from dateutil import relativedelta

class GDT():
    def __init__(self, database, datatype, latlong1=[0, 0], latlong2=[0, 0]):
        """
        Constructor for the GDT data type

       :param database: (required) Location of the database to use.
       :param datatype: (required) The datatype of the GeoData we are using.
                        This will also be the table name.
       :param latlong1: (optional) A latitude and longitude pair representing
                        the southwest corner of a box you want to track. (optional)
       :param latlong2: (optional) A latitude and longitude pair representing
                        the northeast corner of a box you want to track. (optional)
        """

        self._database = dataset.connect(database)
        self._table = self._database[datatype].table

        if type(latlong1) is not list and type(latlong2) is not list:
            raise TypeError("latlong1 and latlong2 must be lists")

        if len(latlong1) is not 2 and len(latlong2) is not 2:
            raise ValueError("latlong1 and latlong2 must be lists of exactly 2 numbers")

        for element in latlong1:
            if (type(element) is not float) and (type(element) is not int):
                raise TypeError("All elements in latlong1 must be a number")

        for element in latlong2:
            if (type(element) is not float) and (type(element) is not int):
                raise TypeError("All elements in latlong2 must be a number")

        self._latlong1, self._latlong2 = latlong1, latlong2

    @property
    def latlong1(self):
        """ The coordinate pair that represents the southwest corner of the bounding box """
        return self._latlong1

    @latlong1.setter
    def latlong1(self, value):
        if type(value) is not list:
            raise TypeError("latlong1 must be a list")

        if len(value) is not 2:
            raise ValueError("latlong1 must be a list of exactly 2 numbers")

        for element in value:
            if (type(element) is not float) and (type(element) is not int):
                raise TypeError("All elements in latlong1 must be a number")

        self._latlong1 = value

    @property
    def latlong2(self):
        """ The coordinate pair that represents the southwest corner of the bounding box """
        return self._latlong2

    @latlong2.setter
    def latlong1(self, value):
        if type(value) is not list:
            raise TypeError("latlong2 must be a list")

        if len(value) is not 2:
            raise ValueError("latlong2 must be a list of exactly 2 numbers")

        for element in value:
            if (type(element) is not float) and (type(element) is not int):
                raise TypeError("All elements in latlong2 must be a number")

        self._latlong2 = value

    def insert(self, item):
        """
        Inserts a new item into the database

       :param item: (required) A dictionary of the values you want to insert.
                    This will automatically create the schema of the table for
                    you, based upon the keys of the dictionary.
        """

        self._table.insert(item)

    def insert_many(self, items):
        """
        Inserts many items into the database

        :param items: (optional) An array of dicts that you want to insert.
                      This will be much faster than iterating over insert.
        """

        self._table.insert_many(items)

    def find(self):
        """
        Finds all items based upon the bounding box defined in the constructor
        """

        statement = "select * from {0} where longitude between {1} and {2} and latitude between {3} and {4}"
        statement = statement.format(self._table.name, self._latlong1[0],
                self._latlong2[0], self._latlong1[1], self._latlong2[1])

        return self._database.query(statement)

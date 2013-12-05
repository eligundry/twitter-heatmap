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

        :database => Location of the database to use.
        :datatype => The datatype of the GeoData we are using. This will also
                     be the table name.
        :latlong1 => A latitude and longitude pair representing the southwest
                     corner of a box you want to track. (optional)
        :latlong2 => A latitude and longitude pair representing the northeast
                     corner of a box you want to track. (optional)
        """

        self.database = dataset.connect(database)
        self.table = self.database[datatype]

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

        self.latlong1, self.latlong2 = latlong1, latlong2

    def insert(self, item):
        """
        Inserts a new item into the database

        :item => A dictionary of the values you want to insert. This will
                 automatically create the schema of the table for you, based
                 upon the keys of the dictionary.
        """

        self.table.insert(item)

    def find_by_freshness(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
        """
        Finds one or more items based how recently it was inserted

        :years => How many years back you want to search back
        :months => How many months back you want to search back
        :days => How many days back you want to search back
        :hours => How many hours back you want to search back
        :minutes => How many minutes back you want to search back
        :seconds => How many seconds back you want to search back
        """

        # First, let's calculate the relative time we want to search for
        start = datetime.datetime.now()
        end = start - dateutil.relativedelta(years=years, months=months,
                days=days, hours=hours, minutes=minutes, seconds=seconds)

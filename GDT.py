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
    def __init__(self, database, datatype):
        """
        Constructor for the GDT data type

        :database => Location of the database to use
        :datatype => The datatype of the GeoData we are using. This will also
                     be the table name.
        """

        self.database = dataset.connect(database)
        self.table = self.database[datatype]

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

"""
    GDT
    ~~~

    Stands for "GeoData Thing". It's middleware for a database and a geolocated
    data type.
"""

import dataset

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

        :item => A dictionary of the values you want to insert
        """

        self.table.insert(item)

# --------------------------------------------------------------------------- #
#                                                                             #
#                           Core Imports                                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from config.configuration import DEBUG, DISPLAY, NAME, IP, PORT, THREADED
from flaskfactory import FlaskFactory as Factory
from sql import mysql

# --------------------------------------------------------------------------- #
#                                                                             #
#                       Default Configuration                                 #
#                                                                             #
# --------------------------------------------------------------------------- #
app = Factory.create(NAME, DISPLAY, IP, PORT, DEBUG, THREADED)
app.sql = mysql.Connection()

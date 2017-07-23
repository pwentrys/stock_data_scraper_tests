# --------------------------------------------------------------------------- #
#                                                                             #
#                           Core Imports                                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from config.configuration import DEBUG, NAME, IP, PORT, THREADED
from flaskfactory import FlaskFactory as Factory

# --------------------------------------------------------------------------- #
#                                                                             #
#                       Default Configuration                                 #
#                                                                             #
# --------------------------------------------------------------------------- #
app = Factory.create(NAME, IP, PORT, DEBUG, THREADED)

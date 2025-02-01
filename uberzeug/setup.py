import configparser
import logging
import os
import socket

from uberzeug.utils.constants import *
from uberzeug.persistence.databasesession import DatabaseSession

# Read the configuration file.
config = configparser.ConfigParser()
config.read(CONFIGFILE)

# Extract the necessary information from the configuration file.
datafolder = config["DEFAULT"]["waybillfolder"]
database_file = config["DEFAULT"]["database"]
logfile = config["DEFAULT"]["logfile"]

# Create the necessary folders for the application.
if not os.path.exists(datafolder):
    os.makedirs(datafolder)

# Create the database file by instantiate the class.
DatabaseSession(database_file)

# Create the logfile with an initial message.
logging.basicConfig(filename=logfile, encoding='utf-8',
                    format="%(levelname)s: %(asctime)s %(message)s",
                    datefmt="%Y.%m.%d %H:%M:%S", level=logging.INFO)
logging.info(f"Überzeug setup started by {socket.gethostname()}")
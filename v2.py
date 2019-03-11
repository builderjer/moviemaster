from datetime import datetime
from mycroft.core import MycroftSkill, intent_file_handler
from mycroft.util.format import pronounce_number, nice_date, nice_number
from mycroft.util.log import LOG

__author__ = "builderjer@github.com"
__version__ = "0.2.0"

LOGGER = LOG(__name__)

class Tmdb(MycroftSkill):
    def __init__(self):
        """A Mycroft skill to access the free TMDb api from https://www.themoviedb.org/"""
        super(Tmdb, self).__init__(name="Tmdb")
        self._movieID = None
        self._

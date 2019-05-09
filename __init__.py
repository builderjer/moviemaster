from datetime import datetime
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.format import pronounce_number, nice_date, nice_number
from mycroft.util.log import LOG

import tmdbv3api

__author__ = "builderjer@github.com"
__version__ = "0.2.0"

LOGGER = LOG(__name__)

TMDB = {
		"tmdb": tmdbv3api.TMDb(),
		"collection": tmdbv3api.Collection(),
		"company": tmdbv3api.Company(),
		"configuration": tmdbv3api.Configuration(),
		"discover": tmdbv3api.Discover(),
		"genre": tmdbv3api.Genre(),
		"movie": tmdbv3api.Movie(),
		"person": tmdbv3api.Person(),
		"season": tmdbv3api.Season(),
		"tv": tmdbv3api.TV()
		}

class MovieMaster(MycroftSkill):
	def __init__(self):
		"""A Mycroft skill to access the free TMDb api from https://www.themoviedb.org/"""
		super(MovieMaster, self).__init__(name="MovieMaster")
		self._api = None
		self._movieID = None
		self._movieDetails = None
		self._movieGenres = None
		self._tvID = None
		self._tvDetails = None
		self._tvGenres = None
	
	def initialize(self):
		""" This sets some variables that do not change during the execution of the script"""
		
		# An API key is required for this to work.  See the README.md for more info
		self.api = self.settings.get("apiv3")
		if self.api is not "" or self.api is not None:
			try:
				TMDB["tmdb"].api_key = self.api
			except Exception as e:
				self.LOGGER.info(e)
				self.api = None
		else:
			self.speak("You must get an API key to use this skill")
			
		# Set the language 
		TMDB["tmdb"].language = self.lang
		
		# Get the genres of the movies and tv shows
		self.movieGenres = TMDB["genre"].movie_list()
		self.tvGenres = TMDB["genre"].tv_list()
	
	@property
	def api(self):
		return self._api

	@api.setter
	def api(self, apiNum):
		self._api = apiNum
	
	@property
	def movieID(self):
		return self._movieID
	
	@movieID.setter
	def movieID(self, movie):
		self._movieID = TMDB["movie"].search(movie)[:1][0].id
	
	@property
	def movieGenres(self):
		return self._movieGenres
	
	@movieGenres.setter
	def movieGenres(self, movie_list):
		self._movieGenres = movie_list
	
	@property
	def tvGenres(self):
		return self._tvGenres
	
	@tvGenres.setter
	def tvGenres(self, tv_list):
		self._tvGenres = tv_list
	
	@property
	def movieDetails(self):
		return self._movieDetails
	
	@movieDetails.setter
	def movieDetails(self, movie):
		try:
			self._movieDetails = TMDB["movie"].details(self.movieID)
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})
	
	@intent_file_handler("movie.description.intent")
	def handle_movie_description(self, message):
		movie = message.data.get("movie")
		if self.movieDetails.title.lower() != movie:
			self.movieDetails = self.movieID(movie)

def create_skill():
	return MovieMaster()

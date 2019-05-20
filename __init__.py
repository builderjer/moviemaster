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
		self._movieDetails = None
		self._movieGenres = None
		self._popularMovies = None
		self._tvID = None
		self._tvDetails = None
		self._tvGenres = None
	
	
	def initialize(self):
		""" This sets some variables that do not change during the execution of the script"""
		
		# An API key is required for this to work.  See the README.md for more info
		self.api = self.settings.get("apiv3")
		if self.api == "" or self.api == None:
		#if self.settings.get("apiv3") == "" or self.settings.get(:
			self.speak_dialog("no.api", {})
		else:
			# Set the api key
			TMDB["tmdb"].api_key = self.api
			# Set the language 
			TMDB["tmdb"].language = self.lang
			
			# Get the genres of the movies and tv shows
			self.movieGenres = TMDB["genre"].movie_list()
			self.tvGenres = TMDB["genre"].tv_list()
		self.settings.set_changed_callback(self.on_settings_changed)

	
	def on_settings_changed(self):
		if self.settings.get("apiv3") is not "":
			LOGGER.info("got a api")
			self.api = self.settings.get("apiv3")
		else:
			LOGGER.info("no damn api")
	
	@property
	def api(self):
		return self._api

	@api.setter
	def api(self, apiNum):
		self._api = apiNum
	
	@property
	def movieGenres(self):
		return self._movieGenres
	
	@movieGenres.setter
	def movieGenres(self, movie_list):
		self._movieGenres = movie_list
	
	@property
	def popularMovies(self):
		#self._popularMovies = TMDB["movie"].popular()[:search_depth]
		return self._popularMovies
	
	@popularMovies.setter
	def popularMovies(self, search_depth):
		self._popularMovies = TMDB["movie"].popular()[:search_depth]
		
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
		self._movieDetails = TMDB["movie"].details(TMDB["movie"].search(movie)[:1][0].id)
	
	@intent_file_handler("movie.description.intent")
	def handle_movie_description(self, message):
		""" Gets the long version of the requested movie.
		"""
		movie = message.data.get("movie")
		LOGGER.info(self.api)
		try:
			self.movieDetails = movie
			if self.movieDetails.overview is not "":
				self.speak_dialog("movie.description", {"movie": movie})
				for sentence in self.movieDetails.overview.split(". "):
					self.speak(sentence)
			else:
				self.speak_dialog("no.info", {"movie": movie})
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})

	@intent_file_handler("movie.information.intent")
	def handle_movie_information(self, message):
		""" Gets the short version and adds the TagLine for good measure.
		"""
		movie = message.data.get("movie")
		try:
			self.movieDetails = movie
			self.speak_dialog("movie.info.response", {"movie": self.movieDetails.title, "year": nice_date(datetime.strptime(self.movieDetails.release_date.replace("-", " "), "%Y %m %d")), "budget": self.movieDetails.budget})
			self.speak(self.movieDetails.tagline)
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})
		except tmdbv3api.exceptions.TMDbException:
			self.speak_dialog("no.api", {})
	
	@intent_file_handler("movie.year.intent")
	def handle_movie_year(self, message):
		""" Gets the year the movie was released.
		"""
		movie = message.data.get("movie")
		try:
			self.movieDetails = movie
			self.speak_dialog("movie.year", {"movie": self.movieDetails.title, "year": self.movieDetails.release_date})
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})
	
	@intent_file_handler("movie.cast.intent")
	def handle_movie_cast(self, message):
		""" Gets the cast of the requested movie.
		
		The search_depth setting is avaliable at home.mycroft.ai
		"""
		movie = message.data.get("movie")
		try:
			self.movieDetails = movie
			cast = self.movieDetails.casts["cast"][:self.settings.get("search_depth")]
			# Create a list to store the cast to be included in the dialog
			actorList = ""
			# Get the last actor in the list so that the dialog can say it properly
			lastInList = cast.pop()
			lastActor = " {} as {}".format(lastInList["name"], lastInList["character"])
			# Format the rest of the list for the dialog
			for person in cast:
				actor = " {} as {},".format(person["name"], person["character"])
				# Add the formated sentence to the actor list
				actorList = actorList + actor
			self.speak_dialog("movie.cast", {"movie": movie, "actorlist": actorList, "lastactor": lastActor})
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})
	
	@intent_file_handler("movie.production.intent")
	def handle_movie_production(self, message):
		""" Gets the production companies that made the movie.
		
		The search_depth setting is avaliable at home.mycroft.ai
		"""
		movie = message.data.get("movie")
		try:
			self.movieDetails = movie
			companyList = self.movieDetails.production_companies[:self.settings.get("search_depth")]
			# If there is only one production company, say the dialog differently
			if len(companyList) == 1:
				self.speak_dialog("movie.production.single", {"movie": movie, "company": companyList[0]["name"]})
			# If there is more, get the last in the list and set up the dialog
			if len(companyList) > 1:
				companies = ""
				lastCompany = companyList.pop()["name"]
				for company in companyList:
					companies = companies + company["name"] + ", "
				self.speak_dialog("movie.production.multiple", {"companies": companies, "movie": movie, "lastcompany": lastCompany})
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})
	
	@intent_file_handler("movie.genres.intent")
	def handle_movie_genre(self, message):
		""" Gets the genres of the movie.
		
		The search_depth setting is avaliable at home.mycroft.ai
		"""
		movie = message.data.get("movie")
		try:
			self.movieDetails = movie
			genreList = self.movieDetails.genres[:self.settings.get("search_depth")]
			# Set up dialog AGAIN just like above.  Is there a better way?
			if len(genreList) == 1:
				self.speak_dialog("movie.genre.single", {"movie": movie, "genre": genreList[0]["name"]})
			if len(genreList) > 1:
				genreDialog = ""
				lastGenre = genreList.pop()["name"]
				for genre in genreList:
					genreDialog = genreDialog + genre["name"] + ", "
				self.speak_dialog("movie.genre.multiple", {"genrelist": genreDialog, "genrelistlast": lastGenre})
		except IndexError:
			self.speak_dialog("no.info", {"movie": movie})
	
	@intent_file_handler("movie.runtime.intent")
	def handle_movie_length(self, message):
		""" Gets the runtime of the searched movie.
		"""
		movie = message.data.get("movie")
		try:
			self.movieDetails = movie
			self.speak_dialog("movie.runtime", {"movie": movie, "runtime": self.movieDetails.runtime})
		except IndexError:
			self.speak_dialog("no.info.general", {})
	
	@intent_file_handler("movie.popular.intent")
	def handle_popular_movies(self, message):
		""" Gets the daily popular movies.
		
		The list changes daily, and are not just recent movies.
		
		The search_depth setting is avaliable at home.mycroft.ai
		"""
		try:
			self.popularMovies = self.settings.get("search_depth")
			# Lets see...I think we will set up the dialog again.
			lastMovie = self.popularMovies.pop().title
			popularDialog = ""
			for movie in self.popularMovies:
				if popularDialog == "":
					popularDialog = movie.title
				else:
					popularDialog = popularDialog + ", " + movie.title
			popularDialog = popularDialog + " and {}".format(lastMovie)
			self.speak_dialog("movie.popular", {"popularlist": popularDialog})
		except IndexError:
			self.speak_dialog("no.info.general", {})
	
	@intent_file_handler("movie.top.intent")
	def handle_top_movies(self, message):
		""" Gets the top rated movies of the day.
		The list changes daily, and are not just recent movies.
		
		The search_depth setting is avaliable at home.mycroft.ai
		"""
		pass
		
def create_skill():
	return MovieMaster()

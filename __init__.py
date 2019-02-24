from datetime import datetime

from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.log import getLogger
from mycroft.util.parse import extract_number
from mycroft.util.format import pronounce_number, nice_date, nice_number

from adapt.intent import IntentBuilder

import tmdbv3api

__author__ = "builderjer@github.com"

LOGGER = getLogger(__name__)

# tmdbv3api has several files so we will access them with a dictionary
TMDB = {
		"tmdb": tmdbv3api.TMDb(),
		#"collection": tmdbv3api.Collection(),
		#"company": tmdbv3api.Company(),
		#"configuration": tmdbv3api.Configuration(),
		#"discover": tmdbv3api.Discover(),
		#"genre": tmdbv3api.Genre(),
		"movie": tmdbv3api.Movie()
		#"person": tmdbv3api.Person(),
		#"season": tmdbv3api.Season(),
		#"tv": tmdbv3api.TV()
		}


class Tmdb(MycroftSkill):
	def __init__(self):
		super(Tmdb, self).__init__(name="Tmdb")
		self.movieID = None
		self.movieDetails = None
	
	def initialize(self):
		TMDB["tmdb"].api_key = self.settings.get("apiv3")
		TMDB["tmdb"].language = self.lang
		#TMDB["tmdb"].language = self.settings.get("language")
		
##################
# Movie Section
##################

# Movie Details

	def getMovieDetails(self, movie):
		self.resetMovieDetails()
		self.movieID = TMDB["movie"].search(movie)[:1][0].id
		self.movieDetails = TMDB["movie"].details(self.movieID)
		
	def resetMovieDetails(self):
		self.movieID = None
		self.movieDetails = None
		
	def checkRepeatMovie(self, movie):
		if self.movieDetails and self.movieDetails.title.lower() == movie:
			return True
		return False
	
	def parseDate(self, date):
		date = date.replace("-", " ")
		date = datetime.strptime(date, "%Y %m %d")
		return nice_date(date)
	
	def getDate(self):
		return nice_date(datetime.strptime(self.movieDetails.release_date.replace("-", " "), "%Y %m %d"))
	
	def getCast(self):
		depth = self.settings.get("cast_depth")
		return self.movieDetails.casts['cast'][:depth]
		# TODO: Do I need to parse this further here?
	
	def getBudget(self):
		return pronounce_number(self.movieDetails.budget)
	
	def getRevenue(self):
		return pronounce_number(self.movieDetails.revenue)
	
	def getProductionCo(self):
		depth = self.settings.get("pro_co_depth")
		return self.movieDetails.production_companies[:depth]
	
	def getRuntime(self):
		return (nice_number(self.movieDetails.runtime) + " minutes")
	
	def getOverview(self):
		return self.movieDetails.overview
	
	def getTagline(self):
		return self.movieDetails.tagline
	
	def getGenres(self):
		depth = self.settings.get("genre_depth")
		return self.movieDetails.genres[:depth]
	
	@intent_file_handler("movie.information.intent")
	def handle_movie_information(self, message):
		movie = message.data.get("movie")
		if not self.checkRepeatMovie(movie):
			try:
				self.getMovieDetails(movie)
			except IndexError:
				pass
		try:
			self.speak_dialog("movie.info.response", {"movie": self.movieDetails.title, "year": self.getDate(), "budget": self.getBudget()})
			self.speak(self.getTagline())
		except AttributeError:
			self.speak_dialog("no.info", {"movie": movie})
		
	@intent_file_handler("movie.year.intent")
	def handle_movie_year(self, message):
		movie = message.data.get("movie")
		if not self.checkRepeatMovie(movie):
			try:
				self.getMovieDetails(movie)
			except IndexError:
				pass
			
		try:
			movie = self.movieDetails.title
			release_date = self.getDate()
			self.speak_dialog("movie.year", {"movie": movie, "year": release_date})
						
		except AttributeError:
				self.speak_dialog("no.info", {"movie": movie})

	@intent_file_handler("movie.description.intent")
	def handle_movie_description(self, message):
		movie = message.data.get("movie")
		if not self.checkRepeatMovie(movie):
			try:
				self.getMovieDetails(movie)
			except IndexError:
				pass
		try:
			overview = self.movieDetails.overview
			self.speak_dialog("movie.description", {"movie": movie, "overview": overview})
		except AttributeError:
			self.speak_dialog("no.info", {"movie": movie})
			
	@intent_file_handler("movie.cast.intent")
	def handle_movie_cast(self, message):
		movie = message.data.get("movie")
		if not self.checkRepeatMovie(movie):
			try:
				self.getMovieDetails(movie)
			except IndexError:
				pass
		try:
			cast = self.getCast()
			self.speak_dialog("movie.cast", {"movie": movie})
			dialog = ""
			for actor in cast:
				act = " {} as {},".format(actor['name'], actor['character'])
				dialog = dialog + act
			self.speak(dialog)
		except AttributeError:
			self.speak_dialog("no.info", {"movie": movie})
				
	@intent_file_handler("movie.production.intent")
	def handle_movie_production(self, message):
		movie = message.data.get("movie")
		if not self.checkRepeatMovie(movie):
			try:
				self.getMovieDetails(movie)
			except IndexError:
				pass
		try:
			company = self.getProductionCo()
			noOfCo = len(company)
			if noOfCo == 1:
			
				self.speak_dialog("movie.production.single", {"movie": movie, "company": company[0]["name"]})
			if noOfCo > 1:
				companies = ""
				for c in company:
					companies = companies + c["name"] + ", "
				self.speak_dialog("movie.production.multiple", {"companies": companies, "movie": movie})
		except AttributeError:
			self.speak_dialog("no.info", {"movie": movie})
					
	@intent_file_handler("movie.genres.intent")
	def handle_movie_genre(self, message):
		movie = message.data.get("movie")
		if not self.checkRepeatMovie(movie):
			try:
				self.getMovieDetails(movie)
			except IndexError:
				pass
		try:
			genres = self.getGenres()
			noOfGenres = len(genres)
			if noOfGenres == 1:
				self.speak_dialog("movie.genre.single", {"movie": movie, "genre": genres[0]["name"]})
			if noOfGenres > 1:
				genreList = ""
				for g in genres:
					genreList = genreList + g["name"] + ", "
				self.speak_dialog("movie.genre.multiple", {"genrelist": genreList})
		except AttributeError:
			self.speak_dialog("no.info", {"movie": movie})
			
def create_skill():
	return Tmdb()


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
        TMDB["tmdb"].api_key = self.settings.get("v3api")
        TMDB["tmdb"].language = self.settings.get("language")
        
##################
# Movie Section
##################

# Movie Details

    def getMovieDetails(self, movie):
        self.resetMovieDetails()
        #LOGGER.info(movie)
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
    
    def getCast(self, depth=4):
        cast = self.movieDetails.casts['cast'][:depth]
        #LOGGER.info(cast)
        # TODO: Do I need to parse this further here?
        return cast
    
    def getBudget(self):
        return nice_number(self.movieDetails.budget)
    
    def getRevenue(self):
        return nice_number(self.movieDetails.revenue)
    
    def getProductionCo(self, depth=4):
        return self.movieDetails.production_companies[:depth]
    
    def getRuntime(self):
        return (nice_number(self.movieDetails.runtime) + " minutes")
    
    def getOverview(self):
        return self.movieDetails.overview
    
    def getTagline(self):
        return self.movieDetails.tagline
    
    def getGenres(self, depth=4):
        return self.movieDetails.genres[:depth]
    
    @intent_file_handler("movie.information.intent")
    def handle_movie_information(self, message):
        movie = message.data.get("movie")
        if not self.checkRepeatMovie(movie):
            self.getMovieDetails(movie)
        self.speak_dialog("movie.info.response", {"movie": self.movieDetails.title, "year": self.getDate(), "budget": self.getBudget()})
        self.speak(self.getTagline())
        
    @intent_file_handler("movie.year.intent")
    def handle_movie_year(self, message):
        movie = message.data.get("movie")
        if not self.checkRepeatMovie(movie):
            self.getMovieDetails(movie)
        movie = self.movieDetails.title
        release_date = self.movieDetails.release_date
        self.speak_dialog("movie.year", {"movie": movie, "year": release_date})
        
    @intent_file_handler("movie.description.intent")
    def handle_movie_description(self, message):
        movie = message.data.get("movie")
        if self.checkRepeatMovie(movie):
            overview = self.movieDetails.overview
        else:
            self.getMovieDetails(movie)
            overview = self.movieDetails.overview
        if overview:
            self.speak_dialog("movie.description", {"movie": movie, "overview": overview})
        else:
            self.speak_dialog("no.info.dialog", {"movie": movie})
            
    @intent_file_handler("movie.cast.intent")
    def handle_movie_cast(self, message):
        movie = message.data.get("movie")
        if self.checkRepeatMovie(movie):
            cast = self.getCast()
        else:
            self.getMovieDetails(movie)
            cast = self.getCast()
        dialog = "The following people play in the movie {}.".format(movie)
        for actor in cast:
            act = " {} as {},".format(actor['name'], actor['character'])
            dialog = dialog + act
        self.speak(dialog)
                
    @intent_file_handler("movie.production.intent")
    def handle_movie_production(self, message):
        movie = message.data.get("movie")
        if self.checkRepeatMovie(movie):
            company = self.getProductionCo()
        else:
            self.getMovieDetails(movie)
            company = self.getProductionCo()
        if len(company) == 1:
            dialog = "The production company {} produced the movie {}.".format(company[0]["name"], movie)
        if len(company) > 1:
            dialog = "The following companies produced the movie {}. ".format(movie)
            for comp in company:
                dialog = dialog + comp["name"] + ", "
        if len(company) < 1:
            dialog = "There is no information on the production companies who made the movie {}.".format(movie)
        self.speak(dialog)
        
    @intent_file_handler("movie.genres.intent")
    def handle_movie_genre(self, message):
        movie = message.data.get("movie")
        if not self.checkRepeatMovie(movie):
            self.getMovieDetails(movie)
        genres = self.getGenres()
        if len(genres) > 1:
            dialog = "The movie {} can be concidered a ".format(movie)
            for g in genres:
                dialog = dialog + g["name"] + " movie, "
        if len(genres) < 1:
            dialog = "I have no genre information on the movie {}".format(movie)
        if len(genres) == 1:
            dialog = "The movie {} is concidered a {} movie".format(movie, genres[0]["name"])
        self.speak(dialog)

def create_skill():
    return Tmdb()


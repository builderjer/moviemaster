from datetime import datetime
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.format import pronounce_number, nice_date, nice_number
import tmdbv3api

__author__ = "builderjer@github.com"

LOGGER = getLogger(__name__)

# tmdbv3api has several files so we will access them with a dictionary
TMDB = {
        "tmdb": tmdbv3api.TMDb(),
        # "collection": tmdbv3api.Collection(),
        # "company": tmdbv3api.Company(),
        # "configuration": tmdbv3api.Configuration(),
        "discover": tmdbv3api.Discover(),
        # "genre": tmdbv3api.Genre(),
        "movie": tmdbv3api.Movie()
        # "person": tmdbv3api.Person(),
        # "season": tmdbv3api.Season(),
        # "tv": tmdbv3api.TV()
        }


class Tmdb(MycroftSkill):
    def __init__(self):
        super(Tmdb, self).__init__(name="Tmdb")
        self.movieID = None
        self.movieDetails = None

    def initialize(self):
        TMDB["tmdb"].api_key = self.settings.get("apiv3")
        TMDB["tmdb"].language = self.lang

##################
# Movie Section
##################

    def getMovieDetails(self, movie):
        self.resetMovieDetails()
        self.movieID = TMDB["movie"].search(movie)[:1][0].id
        self.movieDetails = TMDB["movie"].details(self.movieID)

    def resetMovieDetails(self):
        self.movieID = None
        self.movieDetails = None

    def checkMovie(self, movie):
        if self.movieDetails and self.movieDetails.title.lower() == movie:
            return True
        else:
            try:
                self.getMovieDetails(movie)
                return True
            except IndexError:
                self.resetMovieDetails()
            return False

    def getMovieDate(self):
        return nice_date(datetime.strptime(self.movieDetails.release_date.replace("-", " "), "%Y %m %d"))

    def getMovieCast(self):
        depth = self.settings.get("cast_depth")
        return self.movieDetails.casts['cast'][:depth]

    def getMovieBudget(self):
        return pronounce_number(self.movieDetails.budget)

    def getMovieRevenue(self):
        return pronounce_number(self.movieDetails.revenue)

    def getMovieProductionCo(self):
        depth = self.settings.get("pro_co_depth")
        return self.movieDetails.production_companies[:depth]

    def getMovieRuntime(self):
        return nice_number(self.movieDetails.runtime)

    def getMovieOverview(self):
        return self.movieDetails.overview

    def getMovieTagline(self):
        return self.movieDetails.tagline

    def getMovieGenres(self):
        depth = self.settings.get("genre_depth")
        return self.movieDetails.genres[:depth]

    @intent_file_handler("movie.information.intent")
    def handle_movie_information(self, message):
        movie = message.data.get("movie")
        if self.checkMovie(movie):
            self.speak_dialog("movie.info.response", {"movie": self.movieDetails.title, "year": self.getMovieDate(), "budget": self.getMovieBudget()})
            self.speak(self.getMovieTagline())
        else:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.year.intent")
    def handle_movie_year(self, message):
        movie = message.data.get("movie")
        if self.checkMovie(movie):
            movie = self.movieDetails.title
            release_date = self.getMovieDate()
            self.speak_dialog("movie.year", {"movie": movie, "year": release_date})
        else:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.description.intent")
    def handle_movie_description(self, message):
        movie = message.data.get("movie")
        if self.checkMovie(movie):
            overview = self.movieDetails.overview
            if overview is '':
                self.speak_dialog("no.info", {"movie": movie})
                return
            self.speak_dialog("movie.description", {"movie": movie})
            for sentence in overview.split('. '):
                self.speak(sentence, wait=True)
        else:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.cast.intent")
    def handle_movie_cast(self, message):
        movie = message.data.get("movie")
        if self.checkMovie(movie):
            cast = self.getMovieCast()
            actorList = ""
            last = cast.pop()
            lastActor = " {} as {}".format(last['name'], last['character'])
            for actor in cast:
                act = " {} as {},".format(actor['name'], actor['character'])
                actorList = actorList + act
            self.speak_dialog("movie.cast", {"movie": movie, "actorlist": actorList, "lastactor": lastActor})
        else:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.production.intent")
    def handle_movie_production(self, message):
        movie = message.data.get("movie")
        if self.checkMovie(movie):
            company = self.getMovieProductionCo()
            noOfCo = len(company)
            if noOfCo == 1:
                self.speak_dialog("movie.production.single", {"movie": movie, "company": company[0]["name"]})
            if noOfCo > 1:
                companies = ""
                lastCompany = company.pop()["name"]
                for c in company:
                    companies = companies + c["name"] + ", "
                self.speak_dialog("movie.production.multiple", {"companies": companies, "movie": movie, "lastcompany": lastCompany})
        else:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.genres.intent")
    def handle_movie_genre(self, message):
        if self.checkMovie(movie):
            genres = self.getMovieGenres()
            noOfGenres = len(genres)
            if noOfGenres == 1:
                self.speak_dialog("movie.genre.single", {"movie": movie, "genre": genres[0]["name"]})
            if noOfGenres > 1:
                genreList = ""
                genreListLast = genres.pop()["name"]
                for g in genres:
                    genreList = genreList + g["name"] + ", "
                self.speak_dialog("movie.genre.multiple", {"genrelist": genreList, "genrelistlast": genreListLast})
        else:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.runtime.intent")
    def handle_movie_length(self, message):
        movie = message.data.get("movie")
        if self.checkMovie(movie):
            runtime = self.getMovieRuntime()
            self.speak_dialog("movie.runtime", {"movie": movie, "runtime": runtime})
        else:
            self.speak_dialog("no.info", {"movie": movie})

##################
# Discover Section
##################

    def getGenreMovies(self, genre):
        # TODO: Put depth settings in home.ai?
        depth = self.settings.get("search_depth")
        genreID = None
        for g in self.movieGenres["movies"]:
            if genre == g.name.lower():
                genreID = g.id
                return TMDB["discover"].discover_movies({"sort_by": "popularity.desc", "with_genres": genreID})[:depth]
        return False

    @intent_file_handler("genre.movie.search.intent")
    def handle_genre_movie_search(self, message):
        genre = message.data.get("genre")
        goodGenre = self.getGenreMovies(genre)
        if goodGenre:
            self.speak_dialog("genre.movie.search", {"genre": genre})
            for g in goodGenre:
                self.speak(g.title)
        else:
            self.speak_dialog("bad.genre.catagory", {"genre": genre})


def create_skill():
    return Tmdb()

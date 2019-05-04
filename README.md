# <img src='PrimaryLogo_Green.png' width='50' style='vertical-align:bottom'/> TMDB
Find information about movies, TV shows, actors and production details.

## About
This skill uses tmdbv3api avaliable on GitHub at [tmdbv3api](https://github.com/AnthonyBloomer/tmdbv3api.git)
This product uses the TMDb API but is not endorsed or certified by TMDb.  Information avaliable at [TMDb](https://www.themoviedb.org/)
Easily find information, such as a description, or cast from a movie or tv show with your voice.

## Examples
 - "What is the movie _______ about?"
 - "Tell me about the movie _______"
 - "Who plays in the movie _______?"
 - "What genres does the flick _______ belong to?"
 - "Look for information on the movie _______."
 - "What company made the movie _______?"
 - "When was the movie _______ made?"

## Installation
Installation should be pretty much effortless.

### use msm to install
msm should install the depencencies automatically

```
mycroft-msm install https://github.com/builderjer/tmdb-skill.git
```

### manual install
install tmdbv3api through pip
```
pip install tmdbv3api
```
change into your skills directory and clone from repository
on linux
```
cd /opt/mycroft/skills/
git clone https://github.com/builderjer/tmdb-skill.git 
```

* Go to https://www.themoviedb.org/account/signup
  * Signing up is free
* Get API key from https://www.themoviedb.org/settings/api
  * You will get a v.3 key and a v.4 key
  * We will use the v.3 for this version
* Fill out API key on https://home.mycrof.ai
* Ask a question about a movie
  * "Hey Mycroft, tell me about the movie Monty Python and the Holy Grail"
  * Listen to the awesome responce!!

## Category
**Entertainment**

## Tags
#TMDB
#Movies
#TVshows
#actors

## ToDo
Keep checking for more updates.

## Credits
builderjer@github.com

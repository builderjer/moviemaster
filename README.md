# <img src='PrimaryLogo_Green.png' width='50' style='vertical-align:bottom'/> MOVIEMASTER
Find information about movies, TV shows, actors and production details.

# **Development Version - Not always working**

## About

Easily find information, such as a description, or cast from a movie or tv show with your voice.

## Examples
 - "What is the movie _______ about?"
 - "Tell me about the movie _______"
 - "Who plays in the movie _______?"
 - "What genres does the flick _______ belong to?"
 - "Look for information on the movie _______."
 - "What company made the movie _______?"
 - "When was the movie _______ made?"
 - "Do you have info on the film _______?"
 - "What are popular movies playing now?"
 - "What films do you recommend like _______?"
 - "How long is the movie _______?"
 - "What are the highest rated movies out?

## Installation
Installation should be pretty much effortless.

A free API key is **REQUIRED** for this skill to work

* Signup [here](https://www.themoviedb.org/account/signup) for a FREE account

* Get API key [here](https://www.themoviedb.org/settings/api)
  * You will get a v.3 key and a v.4 key
  * We will use the v.3 for this version **REMEMBER THIS, YOU WILL NEED IT**

### Use mycroft-msm to install automatically
Enter the following command into your terminal

```
mycroft-msm install https://github.com/builderjer/tmdb-skill.git
```

msm should install the dependcencies automatically
If not, you can manually install from pip with the command

```
pip install tmdbv3api
```

### Manual Installation
Install the dependcencies with the above command

Change into your skills directory and clone from repository
on linux or picroft (not tested on Windows)

```
cd /opt/mycroft/skills/
git clone https://github.com/builderjer/moviemaster.git 
```

### After Installation

* Fill out API key on https://home.mycroft.ai
* Ask a question about a movie
  * "Hey Mycroft, tell me about the movie Monty Python and the Holy Grail"
  * Listen to the awesome responce!!

## Category
**Entertainment**

## Tags
#TMDB
#Movies
#Actors
#Mark I

## ToDo
Keep checking for more updates.

## Credits
This skill uses tmdbv3api avaliable on GitHub at [tmdbv3api](https://github.com/AnthonyBloomer/tmdbv3api.git)

It also uses the TMDb API but is not endorsed or certified by TMDb.  Information avaliable at [TMDb](https://www.themoviedb.org/)

builderjer@github.com

# <img src='PrimaryLogo_Green.png' width='50' style='vertical-align:bottom'/> Movie Master
Find information about movies, actors and production details.

## About

Easily find information about a movie with your voice.

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

### Install with your voice
"Hey Mycroft, install Movie Master"

Movie Master should install automatically

### Use mycroft-msm to install automatically
Enter the following command into your terminal

```
mycroft-msm install https://github.com/builderjer/moviemaster.git
```

msm should install the dependcencies automatically

### Manual Installation
Install the dependcencies

```
pip install tmdbv3api
```

Change into your skills directory and clone from repository
on linux or picroft (not tested on Windows)

```
cd /opt/mycroft/skills/
git clone https://github.com/builderjer/moviemaster.git 
```

### After Installation

* Ask a question about a movie
  * "Hey Mycroft, tell me about the movie Monty Python and the Holy Grail"
  * Listen to the awesome response!!

If you are experiencing to much usage and the skill is returning errors, you may enter your own API key

* Signup [here](https://www.themoviedb.org/account/signup) for a FREE account

* Get API key [here](https://www.themoviedb.org/settings/api)
	* You will get a v.3 key and a v.4 key
	* We will use the v.3 for this version **REMEMBER THIS, YOU WILL NEED IT**
	* Enter your new v.3 API key at [Mycroft Skill Settings Page](https://account.mycroft.ai/skills)

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

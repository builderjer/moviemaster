# <img src='PrimaryLogo_Green.png' width='50' style='vertical-align:bottom'/> tmdb-skill
Gets information about lots of movies from tmdb - www.themoviedb.org

## Getting Started
This skill requires you to have a FREE api key from www.themoviedb.org
* Sign up for a free account here https://www.themoviedb.org/account/signup
* And get an api key here 

## Prerequisites
This skill uses the awesome free api wrapper tmdbv3api 
The skill should install this its self with the requirements.txt file, but if not,
It is located here https://anthonybloomer.github.io/tmdbv3api/ and can be installed with pip

## Description
Uses the tmdb api to call information about movies, actors, production companies and such.

## Examples
 - "What is the movie _______ about?"
 - "Tell me about the movie _______"
 - "Who plays in the movie _______?"
 - "What genres does the flick _______ belong to?"
 - "Look for information on the movie _______."
 - "What company made the movie _______?"
 - "When was the movie _______ made?"

## Instalation
use msm to install

```
mycroft-msm install https://github.com/builderjer/tmdb-skill.git
```

or install manually

```
cd /opt/mycroft/skills
git clone https>://github.com/builderjer/tmdb-skill.git 
cd tmdb-skill
pip install requirements.txt
```

* Fill out API key on https://home.mycrof.ai

## ToDo
There are several other parts provided by the tmdb api.  While this skill allows movie information, eventually it will include the other api capabilities.  Keep checking the dev branch for updates.

## Credits
builderjer@github.com

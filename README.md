# Bot ENERGY_PROVIDER

## Description

Project-Documentation: https://prjctr.notion.site/Project-Documentation-e76144f00f414035a0fe428a1e25d763
Game platform: https://python-beginning.prjctr.com/

A bot is a web server that implements eight endpoints so that the platform can communicate with the bot and bot controls agents (units of the game).
The game is a campaign between two bot implementations, **blue** and **red** teams, and the condition for winning is gaining a strategic advantage in energy units over the opponent.

There are two active types of agents in the game: 
1) active (only the one factory and any number of engineers), 
2) passive (4 types of power-plants, assembled in a factory, built by engineers in a suitable location to produce energy units).

The bot stores information about its agents and enemy agents using **variables** (simulating a database).
It also stores data about the map, based on which the bot makes a decision to build a certain type of power-plants.

The bot code includes **main.py** (eight endpoints with POST, PATCH, GET and DELETE requests) and **utils.py** (with auxiliary functions).

The bot code is writen using **flask** (Flask, Response, jsonify, request) and **random**(for relocating engineer).

The bot code is undergoing clean code verification (by **Flake8** and **mypy**).

The bot code is stored on a GitHub repository. To start a new game, you need to specify the SHA (id) of the commit with the version of the bot that should play for a specific team.

## Contributors

Anna Lysokhmara

## Local development

You need to have Python 3.10 or higher.

- Create a new virtual environment `python -m venv ./venv` and activate it
- Install packages `pip install -r requirements.txt`
- Run the code python main.py

To run linting checks locally, you may also do:

- Install linters `pip install flake8 mypy`
- To run code linting: `flake8 .`
- To run type checker `mypy .`

# Bot ENERGY_PROVIDER

## Description

Project-Documentation: https://prjctr.notion.site/Project-Documentation-e76144f00f414035a0fe428a1e25d763

Game platform: https://python-beginning.prjctr.com/

A bot is a _web server_ game platform communicate with. It implements eight endpoints and controls agents of own team.
The game is a campaign between two bot implementations, _blue_ and _red_ teams, and the condition for winning is gaining a strategic advantage in energy units over the opponent.

There are two types of agents in the game: 
1) active (only the one FACTORY and any number of ENGINEER_BOTs), 
2) passive (4 types of POWER_PLANTS, assembled in a factory, built by engineers in a suitable location to produce energy units).

The bot stores information about its agents and enemy agents using _variables_ (simulating a database).
It also stores data about the map, based on which the bot makes a decision to build a certain type of power-plants.

The bot code includes [main.py]() (eight endpoints with **POST**, **PATCH**, **GET** and **DELETE** requests) and [utils.py]() (with auxiliary functions).

The bot code is writen using **flask** _(Flask, Response, jsonify, request)_ and **random** _(for relocating engineer)_.

The bot code is undergoing _clean code verification_ (by **Flake8** and **mypy**).

The bot code is stored on a GitHub repository. Starting a new game is possible with the SHA (id) of the commit with the version of the bot.

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

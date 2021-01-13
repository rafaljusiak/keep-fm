# keep-fm

[![Coverage Status](https://coveralls.io/repos/github/rafaljusiak/keep-fm/badge.svg)](https://coveralls.io/github/rafaljusiak/keep-fm)
[![Build Status](https://travis-ci.com/rafaljusiak/keep-fm.svg?branch=master)](https://travis-ci.com/rafaljusiak/keep-fm)

Unofficial tool created to save your scrobbles data from https://last.fm locally, and to give opportunity to work with your data.
**Commercial usage is PROHIBITED** - you can **ONLY** use it for **personal** and **non-public** purpose.
In other words - this web application **can't be hosted on the internet** and you can **ONLY scrap data from YOUR account**.
The user, not the author of the code, is responsible for any illegal use.

## Idea
Last.fm is a great service, that I use since 2006. 
I had 3 different accounts (one created after another) and when I started to use Spotify in around 2014, I was annoyed with all the `- Remastered 2005` and `- Radio Edit` annotations that were ruining my scrobbles and rankings.

I wanted to have some option to get a cumulative stats of all of my past accounts, **and** to unify scrobbled track names, to have a real information about my top tracks. 

## Features
- Save your scrobbles data in the local database 
- Create combined rankings for more than one user accounts
- Unify and clear track names (for example: remove `- Remastered` from the scrobbled song name)

## How-to
1. Make sure you have installed `Docker` and `docker-compose`.
2. If you don't have already installed `invoke` - install it with `pip install invoke` command.
3a. Setup solution with `invoke initial-setup` command.
3b. At one step you will be asked for your credentials (username, email and password) - you don't need to use the same as your last.fm credentials. 
4. Execute `invoke start` to run application.
5. Login to admin dashboard at `http://127.0.0.1:8000/admin` and configure your account.
6. When your account is ready - run `invoke update-data <your_last_fm_user_name>` to start fetching your scrobbles from last.fm.

### Alpha/in progress features
- Associate scrobbled tracks with Spotify URLs.

### Planned features 
- REST API.
- Better GUI.
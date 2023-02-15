# GALP

GALP is an application for managing football games and tournaments that can be used to play tournaments in virtual games like FIFA.

## Authors

- [@JakubPiecha](https://github.com/JakubPiecha)

## Demo

![ezgif com-gif-maker](https://user-images.githubusercontent.com/114153071/218771693-968ad7b0-2d90-4487-af60-c4fbec4f439d.gif)



## Running Tests

To run tests, run the following command

```bash
  pytest
```
## Tests
![Zrzut ekranu z 2023-02-14 12-01-42](https://user-images.githubusercontent.com/114153071/218734607-b9cdecae-7cbc-476d-bd89-9a58a8274e7e.jpg)

## Usage

* Creating games
* Adding teams
* Entering competition results
* Automatic scheduling (two types)
* Automatic creation of a table based on entered match results.
* Assigning players to teams. A player may only play for one team in selected competitions.
* Only the tournament owner can add scores and edit matches
* Only the team owner or competition owner can edit the team and add players to the team

## Technologies Used

- python 3.10
- Django==4.1.3

## Installation

 Clone the repository

```bash
git clone git@github.com:JakubPiecha/GALP.git
```
or if you don't have ssh 

```bash
git clone https://github.com/JakubPiecha/GALP.git
```

- Create virtual environment to install dependencies and activate it:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DJ_SECRET_KEY`

`DJ_DEBUG`

`DATABASE_URL`

`DJ_SU_USERNAME`

`DJ_SU_PASSWORD`

`DJ_GROUP_TEAM_OWNER`

`DJ_GROUP_COMPETITION_OWNER`


```bash
python manage.py loaddata ./fixtures/data.json
```

You can load sample data into the database

```bash
python manage.py loaddata ./fixtures/data.json
```
Start app

```bash
python manage.py runserver
```
## Features

- adding more stats
- add a more intuitive UI

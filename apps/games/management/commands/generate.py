import requests
import random
import datetime
from typing import Any, Optional
from django.core.management import BaseCommand
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError

from games.models import (
    Genre,
    Game,
    Company
)


class Command(BaseCommand):
    """Command for generate data for Database."""

    def genre_list(self)-> None:
        _genres_pattern: set[str] = {
            "одиночная игра",
            "мультиплеер",
            'песочница',
            'выживание',
            'зомби',
            'аниме',
            'визуальная новелла',
            'экономика',
            'психоделика',
            'баттл рояль',
            'файтинг',
            'реализм',
            'война',
            'стелс',
            'строительство',
            'VR',
            'симульятор',
            'открытый мир',
            'кино',
            'какашка'
        }   
        gn:str
        for gn in _genres_pattern:
            try:
                Genre.objects.create(
                    name=gn
                )
            except IntegrityError as e:
                print("genre add error")

    def company_list(self)-> None:
        _companys_pattern: set[str] = {
            "EA game",
            "GGG",
            'BSG',
            'Blizzard',
            'crytak',
            'ubisoft',
            'Valv',
            'Wargaming',
            'activision',
            'bandai namco'
        } 
        cn:str
        for cn in _companys_pattern:
            ye = random.randint(1999,2023)
            me = random.randint(1,12)
            de = random.randint(1,25)
            he = random.randint(0,23)
            mi = random.randint(1,60)
            try:
                Company.objects.create(
                    name=cn,
                    datetime_created = datetime.datetime(
                        year = ye,
                        month = me,
                        day = de,
                        hour = he,
                        minute = mi
                        )
                )
            except IntegrityError as e:
                print("company add error")

    
    def create_games(self) -> None:
        headers: dict[str, str] = {
           	"X-RapidAPI-Key": "e9787699e5msha3778afc026c592p16a8f6jsn526ef30a2127",
	        "X-RapidAPI-Host": "cheapshark-game-deals.p.rapidapi.com"
        }
        querystring: dict[str, str] = {
            "lowerPrice":"0",
            "steamRating":"0",
            "desc":"0",
            "output":"json",
            "steamworks":"0",
            "sortBy":"Deal Rating",
            "AAA":"0",
            "pageSize":"500",
            "exact":"0",
            "upperPrice":"50",
            "pageNumber":"0",
            "onSale":"0",
            "metacritic":"0",
            "storeID[0]":"1,2,3"
        }
        url = "https://cheapshark-game-deals.p.rapidapi.com/deals"
        response: requests.Response = \
            requests.get(url, headers=headers, params=querystring)
        
        response_games: list[dict[str, str]] = response.json()

        companies: QuerySet[Company] = Company.objects.all()
        genres: QuerySet[Genre] = Genre.objects.all()

        game: dict[str, str]
        for game in response_games:
            try:
                temp_game: Game = Game.objects.create(
                    name=game['title'],
                    price=game['normalPrice'],
                    datetime_created=datetime.datetime.fromtimestamp(
                        game['releaseDate']
                    ),
                    company=random.choice(companies)
                )
                for _ in range(random.randint(0, 10)):
                    temp_game.genres.add(
                        random.choice(genres)
                    )

                temp_game.save()
            except IntegrityError as e:
                print("Game {} already exists".format(
                    game['title']
                ))


    def handle(self, *args, **kwargs):
        self.create_games()
        self.company_list()
        self.genre_list()
        print("FINISH")

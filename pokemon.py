import requests
import random
import time

class Pokemon:
    def __init__(self, name, hp=10, attack=30, defense=40, speed=60):
        self.name = name
        self._api = f'https://pokeapi.co/api/v2/pokemon/{self.name}'
        self.list_names_url = {}
        self.list_moves = {}
        self.type = None
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.get_types()
        self.get_moves()

    def __repr__(self):
        return f'{self.name} \n {self.type}\n {self.list_moves}'

    def get_types(self):
        res = requests.get(self._api)    
        pokemon_type = []
        for i in res.json()['types']:
            pokemon_type.append(i['type']['name'])
        self.type = tuple(pokemon_type)

    def get_moves(self):
        list_names_url = {}
        res = requests.get(self._api)
        moves = res.json()['moves']

        for move in moves:
            list_names_url[move['move']['name']] = move['move']['url']

        while len(self.list_names_url) < 4:
            try:
                move = random.choice(list(list_names_url.items()))
            except:
                print('Problema de Conexão, espera de 5 Segundos...')
                time.sleep(5)
                continue
            if move[0] not in self.list_names_url.keys() and requests.get(move[1]).json()['power'] != None:
                self.list_names_url.update(dict([move]))

        for name, url in self.list_names_url.items():
            list_move = {}
            res = requests.get(url)
            list_move['accuracy'] = res.json()['accuracy']
            list_move['power'] = res.json()['power']
            list_move['pp'] = res.json()['pp']
            list_move['type'] = res.json()['type']['name']
            self.list_moves[name] = list_move

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def defense(self):
        return self._defense
    
    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = value
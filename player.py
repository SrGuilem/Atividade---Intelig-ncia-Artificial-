import random
import requests
from datetime import datetime
import pickle
import time
import os
import copy
from matriz import Chart
import numpy as np
import pandas as pd

class Pokemon:
    def __init__(self, name, hp=random.randint(200,300), attack=random.randint(70,100),
                       defense=random.randint(60,90), speed=random.randint(70, 100)):
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
        type_of_pokemon = str(self.type).replace('(', '').replace(')', '').replace("'", '').replace("'", '').replace(',', '/').replace(' ', '')
        list_moves = [i for i in self.list_moves]
        space = '='*30
        return f'{space}\nPokemon: {self.name} \n Type: {type_of_pokemon}\n {self.list_moves}\n{space}\n'

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

class Player:
    def __init__(self, name):
        self.name = name
        self.squad = None
        self.get_list_pokemons()

    
    def get_list_pokemons(self):
        list_pokemons = []
        squad = []

        while len(list_pokemons) < 6:
            pokemon = random.choice(pokemons).lower()
            if pokemon not in list_pokemons:
                list_pokemons.append(pokemon)
        for pokemon in list_pokemons:
            while True:
                try:
                    squad.append(Pokemon(pokemon))
                    break
                except:
                    print(f'Linha 25, pokemon: {pokemon}')
        self.squad = tuple(squad)
   
pokemons = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle',
    'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto',
    'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 
    'Sandslash', 'Nidorina', 'Nidoqueen', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable',
    'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras',
    'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey',
    'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop',
    'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler',
    'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Doduo', 'Dodrio',
    'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno',
    'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan',
    'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra',
    'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros',
    'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar',
    'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 
    'Mewtwo', 'Mew', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil', 'Quilava', 'Typhlosion', 'Totodile', 'Croconaw', 
    'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak', 'Ariados', 'Crobat',
    'Chinchou', 'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Flaaffy']

retirados = ['Nidoran', 'Farfetch’d', 'Mr. Mime']

"""
player_1 = Player('Player_1')
time.sleep(2)
ia_1 = Player('ia_easy')
time.sleep(2)
ia_2 = Player('ia_medium')
time.sleep(2)
ia_3 = Player('ia_hard')

storage_pokemon = open('storage_pokemon.pkl', 'wb')
pickle.dump(player_1, storage_pokemon)
pickle.dump(ia_1, storage_pokemon)
pickle.dump(ia_2, storage_pokemon)
pickle.dump(ia_3, storage_pokemon)

"""

storage_pokemon = open('storage_pokemon.pkl', 'rb')
player_1 = pickle.load(storage_pokemon)
ia_1 = pickle.load(storage_pokemon)
ia_2 = pickle.load(storage_pokemon)
ia_3 = pickle.load(storage_pokemon)


class Simulator_Pokemon:
    def __init__(self, player_1):
        self._npc_list = [ia_1, ia_2, ia_3]
        self._squad = copy.deepcopy(player_1.squad)
        self.player_1 = player_1
        self.player_2 = None
        self.rodation = 0
        self.chosen_1 = 0
        self.chosen_2 = 0
        self._chart = Chart()

    def ia_escolha(self):
        type_pokemon = self.player_1.squad[self.chosen_1].type
        pokemons_ia = [i.type for i in self.player_2.squad]
        lista_total = [0, 0, 0, 0, 0, 0]
        for i in type_pokemon:
            for j in pokemons_ia:
                valor = sum([ self._chart.matriz[i][l] for l in j])

            for index in range(len(lista_total)):
                lista_total[index] = lista_total[index] + valor
        return lista_total


    def ia_ataque(self):
        names = [i for i in self.player_2.squad[self.chosen_2].list_moves]
        type_moves = [self.player_2.squad[self.chosen_2].list_moves[i]['type'] for i in names]
        type_pokemon = self.player_1.squad[self.chosen_1].type
        lista = []
        for i in type_moves:
            lista.append(self._chart.weight_calculator(i, type_pokemon))
        return np.argmax(lista)

    def start(self):
        self.clear()
        while True:
            print(f'Saudações {player_1.name}!!')
            player_1.name = input('Digite seu nome: ')
            name = input(f'Tem certeza que deseja que eu lhe chame de {player_1.name}:[Y/N]')
            if name.upper() == 'Y':
                print(f'{player_1.name} para você ser um treinador pokemons você recebeu 6 pokemons')
                for i in player_1.squad:
                    print(i)
                    input()
                break
            else:
                player_1.name = 'Player_1'

        while True:
            self.clear()
            print('Escolha a dificuldade do seu oponente: ')
            print('1 - Easy')
            print('2 - Medium')
            print('3 - Hard')
            while True:
                try:
                    level = int(input('[1/2/3]: '))
                    break
                except:
                    pass
            if level not in [1, 2, 3]:
                continue
            else:
                if level == 1:
                    self.player_2 = copy.deepcopy(self._npc_list[0])
                    self.battle()
                elif level == 2:
                    self.player_2 = copy.deepcopy(self._npc_list[1])
                    self.battle()
                elif level == 3:
                    self.player_2 = copy.deepcopy(self._npc_list[2])
                    self.battle()
    

    def battle(self):
        print('='*30+'BATALHA'+'='*30)
        print(f'{self.player_1.name} VERSUS {self.player_2.name}')
        if self.player_1.squad[self.chosen_1].speed >= self.player_2.squad[self.chosen_2].speed:
            while True:
                if (self.rodation % 2) == 0:
                    self.check_life()
                    self.display(self.player_1, self.player_2, self.chosen_1, self.chosen_2)
          
                else:
                    self.check_life()
                    self.display(self.player_2, self.player_1, self.chosen_2, self.chosen_1)

                result = self.check_lifes()
                if result:
                    return result

        else:
            while True: 
                if (self.rodation % 2) == 0:
                    self.check_life()
                    self.display(self.player_2, self.player_1, self.chosen_2, self.chosen_1)
                else:
                    self.check_life()
                    self.display(self.player_1, self.player_2, self.chosen_1, self.chosen_2)
                
                result = self.check_lifes()
                if result:
                    return result

    def check_lifes(self):
        pokemons_hp_1 = [i.hp for i in self.player_1.squad]
        pokemons_hp_2 = [i.hp for i in self.player_2.squad]
        if max(pokemons_hp_1) <= 0:
            return 1
        elif max(pokemons_hp_2) <= 0:
            return 2
        else:
            return None

    def check_life(self):
        if self.player_1.squad[self.chosen_1].hp <= 0:
            print(self.player_1.squad[self.chosen_1].name, 'Morto')
            while True:
                try:
                    self.chosen_1 = int(input('             Troca de pokemon: '))
                    if self.player_1.squad[self.chosen_1].hp <= 0:
                        print('POKEMON MORTO')
                        continue
                    else:
                        break
                except:
                    continue
            
        elif self.player_2.squad[self.chosen_2].hp <= 0:
            b = self.ia_escolha()

            if self.player_2.squad[np.argmin(b)].hp <= 0:
                if self.player_2.squad[0].hp >= 0:
                    self.chosen_2 = 0
                elif self.player_2.squad[1].hp >= 0:
                    self.chosen_2 = 1
                elif self.player_2.squad[2].hp >= 0:
                    self.chosen_2 = 2
                elif self.player_2.squad[3].hp >= 0:
                    self.chosen_2 = 3
                elif self.player_2.squad[4].hp >= 0:
                    self.chosen_2 = 4
                elif self.player_2.squad[5].hp >= 0:
                    self.chosen_2 = 5
            else:
                self.chosen_2 = np.argmin(b)


    def display(self, player_1, player_2, number_1, number_2):
        input()
        self.clear()
        pokemon_1 = player_1.squad[number_1]
        print('='*30)
        print(f'Jogador: {player_1.name}')
        print(f'Pokemon: {pokemon_1.name}')
        print(f'Type: {pokemon_1.type}')
        print(f'HP: {pokemon_1.hp}   ATTACK: {pokemon_1.attack}')
        print(f'DEFENSE: {pokemon_1.defense}   speed: {pokemon_1.speed}')
        print('x'*30)
        pokemon_2 = player_2.squad[number_2]
        print('='*30)
        print(f'Jogador: {player_2.name}')
        print(f'Pokemon: {pokemon_2.name}')
        print(f'Type: {pokemon_2.type}')
        print(f'HP: {pokemon_2.hp}   ATTACK: {pokemon_2.attack}')
        print(f'DEFENSE: {pokemon_2.defense}   speed: {pokemon_2.speed}')
        print('x'*30)
        if player_1.name not in ['ia_easy', 'ia_medium', 'ia_hard']:
            self.actions(player_1.name)
        elif player_1.name in ['ia_easy', 'ia_medium', 'ia_hard']:
            if player_1.name == 'ia_easy':
                self.actions(player_1.name)
            elif player_1.name == 'ia_medium':
                self.actions(player_1.name)
            elif player_1.name == 'ia_hard':
                self.actions(player_1.name)
        
    def actions(self, name):
        print()
        print(f'    {name} é sua vez')
        while True:
            print('     1 - Attack')
            print('     2 - Switch Pokemon')
            #================== 
            if name == 'ia_easy':
                time.sleep(random.choice([1, 2, 3, 4, 5]))
                actions = random.choice([1, 2])
                print(f'       {name} escolheu: ', actions)
            elif name == 'ia_medium':
                time.sleep(random.choice([1, 2, 3, 4, 5]))
                actions = random.choice([1, 2])
                print(f'       {name} escolheu: ', actions)

            elif name == 'ia_hard':
                b = self.ia_escolha()
                if np.argmin(b) == self.chosen_2:
                    actions = 2
                else:
                    actions = 1
                
            else:
                while True:
                    try:
                        actions = int(input('      Sua escolha: '))
                        break
                    except:
                        pass
            print()
            if actions in [1, 2]:
                while True:
                    if actions == 1:                    
                        for index ,move in enumerate(self.player_1.squad[self.chosen_1].list_moves):
                            print(f'        {index} {move}: {self.player_1.squad[self.chosen_1].list_moves[move]}')

                        #================== 
                        if name == 'ia_easy':
                            time.sleep(random.choice([1, 2, 3, 4, 5]))
                            move = random.choice([0, 1, 2, 3])
                            print(f'        {name} escolheu ', move)
                            self.damage(self.player_2, self.player_1, self.chosen_2, self.chosen_1, move)
                        elif name == 'ia_medium':
                            time.sleep(random.choice([1, 2, 3, 4, 5]))
                            move = self.ia_ataque()
                            print(f'        {name} escolheu ', move)
                            self.damage(self.player_2, self.player_1, self.chosen_2, self.chosen_1, move)
                        elif name == 'ia_hard':
                            time.sleep(random.choice([1, 2, 3, 4, 5]))
                            move = self.ia_ataque()
                            print(f'        {name} escolheu ', move)
                            self.damage(self.player_2, self.player_1, self.chosen_2, self.chosen_1, move)

                        else:
                            while True:
                                try:
                                    move = int(input('         Escolha o seu ataque: '))
                                    if move not in [0, 1, 2, 3]:
                                        print('PORRA')
                                        continue
                                    else:
                                        self.damage(self.player_1, self.player_2, self.chosen_1, self.chosen_2, move)
                                        break
                                except Exception as e:
                                    print(e)
                                    pass
                        #================== 
                        self.rodation +=1
                        time.sleep(5)
                        return

                    elif actions == 2:    
                        print('        Escolha qual Pokemon você deseja: ')
                        for index, pokemon in enumerate(self.player_1.squad):
                            print(f"        {index}: {pokemon.name}")
                        print()

                        if name == 'ia_easy':

                            while True:
                                self.chosen_2 = random.choice(range(len(self.player_2.squad) -1 ))
                                if self.player_2.squad[self.chosen_2].hp <= 0:
                                    print('        POKEMON MORTO')
                                    continue
                                else:
                                    break

                        elif name == 'ia_medium':

                            while True:
                                self.chosen_2 = random.choice(range(len(self.player_2.squad) -1))
                                if self.player_2.squad[self.chosen_2].hp <= 0:
                                    print('POKEMON MORTO')
                                    continue
                                else:
                                    break

                        elif name == 'ia_hard':
                            b = self.ia_escolha()
                            if self.player_2.squad[np.argmin(b)].hp <= 0:
                                if self.player_2.squad[0].hp >= 0:
                                    self.chosen_2 = 0
                                elif self.player_2.squad[1].hp >= 0:
                                    self.chosen_2 = 1
                                elif self.player_2.squad[2].hp >= 0:
                                    self.chosen_2 = 2
                                elif self.player_2.squad[3].hp >= 0:
                                    self.chosen_2 = 3
                                elif self.player_2.squad[4].hp >= 0:
                                    self.chosen_2 = 4
                                elif self.player_2.squad[5].hp >= 0:
                                    self.chosen_2 = 5
                            else:
                                self.chosen_2 =  np.argmin(b)
                                

                        else:
                            while True:
                                try:
                                    self.chosen_1 = int(input('             Troca de pokemon: '))
                                    if self.player_1.squad[self.chosen_1].hp <= 0:
                                        print('POKEMON MORTO')
                                        continue
                                    else:
                                        break
                                except:
                                    continue

                        self.rodation +=1
                        return
                    else:
                        pass

            else:
                continue



    def damage(self, player_1, player_2, pokemon_1, pokemon_2, move):
        name_move = [i for i in player_1.squad[pokemon_1].list_moves][move]
        list_pokemon_2_type = player_2.squad[pokemon_2].type
        type_move_1 = player_1.squad[pokemon_1].list_moves[name_move]['type']
        weight_type = self._chart.weight_calculator(type_move_1, list_pokemon_2_type)
        stab = 1.5 if type_move_1 in player_1.squad[pokemon_1].type else 1
        attack = player_1.squad[pokemon_1].attack
        defense = player_2.squad[pokemon_2].defense
        power = player_1.squad[pokemon_1].list_moves[name_move]['power']
        damage = (((22*power*(attack/defense)+2)/50) * stab * weight_type)
        player_2.squad[pokemon_2].hp -= damage
        print(f'Menos {damage} de HP!!!')

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')        






simulador = Simulator_Pokemon(player_1)
simulador.start()
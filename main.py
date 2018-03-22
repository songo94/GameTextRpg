from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

#Magic
fire = Spell('Fire',10, 160, 'black')
thunder = Spell('Thunder',12, 170, 'black')
quake = Spell('Earthquake',9, 152, 'black')
ice = Spell('Blizzard',8, 120, 'black')
meteor = Spell('Meteor',20, 200, 'black')

#Magic2
cure = Spell('Cure',12,120,'white')
cura = Spell('Cura', 18, 200, 'white')

#Items
potion = Item('Potion', 'potion', 'Heals for 50 hp', 50)
hipotion = Item('Hi-Potion', 'potion', 'Heals for 100 hp', 100)
superpotion = Item('Super Potion', 'potion', 'Heals for 500 hp', 500)
elixer = Item('Elixer', 'elixer', 'Fully restores HP/MP of one party member', 99999)
hielixer = Item('MegaElixier', 'elixer', 'Fully restore partys HP/MP ', 9999)
granade = Item('Granade', 'attack', 'deals 500 dmg', 500)

player_spells = [fire,thunder,quake,ice,meteor,cure,cura]
player_items = [{'item' : potion, 'quantity':15}, {'item' : hipotion, 'quantity':5}, {'item' : superpotion, 'quantity':5},
{'item' : elixer, 'quantity':5}, {'item' : hielixer, 'quantity':2}, {'item' : granade, 'quantity':5}]
enemy_spells = [fire,thunder,quake,ice,meteor]

#Create players
player1 = Person('Valos: ',2260,135,200,64,player_spells,player_items)
player2 = Person('Nick : ',1860,145,221,54,player_spells,player_items)
player3 = Person('Steve: ',1740,111,188,74,player_spells,player_items)
players = [player1,player2,player3]

#Create enemies
enemy1 = Person('Philip: ',3500,445,700,100,enemy_spells,[])
enemy2 = Person('Xard:  ',800,265,110,70,enemy_spells,[])
enemy3 = Person('Magnas:  ',910,165,120,80,enemy_spells,[])
enemies = [enemy1,enemy2,enemy3]
running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + 'An enemy attacks' + bcolors.ENDC)


while running:
    print('===============')
    print("\n\n")
    print('Name                HP                                     MP')
    for player in players:
        player.get_stats()
    print()
    print('Enemy: ')

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input('Choose action: ')
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print('You have attacked ', enemies[enemy].name.replace(" ","") ,'for', dmg , 'points of damage', 'Enemy HP is: ', enemies[enemy].get_hp())
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ","") + " has died")
                del enemies[enemy]
        elif index == 1:
            player.choose_spell()
            magic_choose = int(input('Choose magic: ')) - 1
            if magic_choose == -1:
                continue
            spell = player.magic[magic_choose]
            magic_dmg = player.magic[magic_choose].generate_spell()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL, 'You don\'t have enough mana' + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + ' heals for ' + str(magic_dmg) + ' HP.')
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + spell.name + ' deals ' + str(magic_dmg) + ' points of dmg')

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ","") + " has died")
                del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choose = int(input("Choose item: ")) - 1
            if item_choose == -1:
                continue
            item = player.items[item_choose]["item"]
            if player.items[item_choose]['quantity'] == 0:
                print(bcolors.FAIL + "\n" + "None left ...." + bcolors.ENDC)
                continue
            player.items[item_choose]['quantity'] -=1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name  + ' heals for ', item.prop, ' HP')
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + '\n' + item.name + ' heals to: ' ,player.maxhp, ' HP, and', player.maxmp, ' Mana')
            elif item.type == 'attack':
                enemies[enemy].take_dmg(item.prop)
                print('You attacked enemy for: ', item.prop, 'Enemy has ', enemies[enemy].hp, ' HP')
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + " has died")
                    del enemies[enemy]
    defeated_enemies = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print('You won')
        running = False

    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players +=1

    if defeated_players == 2:
        print("You lost")
        running = False

    for enemy in enemies:
        enemy_choice = random.randrange(0,2)
        if enemy_choice == 0:
            target = random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ", ""),' attacks for ', enemy_dmg, ' damage')
            print('--------------------------------------------------')
            print()
            print(enemy.name.replace(" ", ""),' HP: ',bcolors.FAIL + str(enemy.get_hp()) + "/", str(enemy.get_maxhp())+ bcolors.ENDC + '\n')

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + ' heals for ' + str(magic_dmg) + ' HP.')
            elif spell.type == "black":
                target = random.randrange(0,3)
                players[target].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ","") + "'s " +spell.name + ' deals ' + str(magic_dmg) + ' points of dmg')

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died")
                del players[target]




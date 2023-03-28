'''
Created on Mar. 27, 2023

@author: raymond

This program will play Prší with players and 'bots' who just play random, legal, cards.
https://en.wikipedia.org/wiki/Mau-Mau_(card_game)k

ASCI art: https://patorjk.com/software/taag/#p=display&f=Alpha&t=

Mar 27: Completed full implementation with only bots. Later I added custom ASCII art cards for all cards.
'''

import random
import time

gg = '''
.------..------..------..------.     .------..------..------..------.
|G.--. ||O.--. ||O.--. ||D.--. |.-.  |G.--. ||A.--. ||M.--. ||E.--. |
| :/\: || :/\: || :/\: || :/\: (( )) | :/\: || (\/) || (\/) || (\/) |
| :\/: || :\/: || :\/: || (__) |'-.-.| :\/: || :\/: || :\/: || :\/: |
| '--'G|| '--'O|| '--'O|| '--'D| (( )) '--'G|| '--'A|| '--'M|| '--'E|
`------'`------'`------'`------'  '-'`------'`------'`------'`------'
'''

cards_per_suit = 8 # I need to rework how the number of cards is handled.
cards_per_suit += 7

deck = []
discard = []
player1_hand = {'name': 'Player1','cards': []}
player2_hand = {'name': 'Player2','cards': []}
player3_hand = {'name': 'Player3','cards': []}
player4_hand = {'name': 'Player4','cards': []}
hands = [player1_hand, player2_hand, player3_hand, player4_hand]

def main():
    make_deck()
    print(deck)
    time.sleep(0.2)
    deal()
    time.sleep(0.2)
    for hand in hands:
        print(f'{hand["name"]} Hand: ', print_cards(hand['cards']))
    print('Top card is: ', print_cards([discard[0]]))
    print('What is left: ', len(deck), 'cards.\n', print_cards(deck))
    print('\n\n')
    time.sleep(0.2)
    game_loop()

def game_loop():
    global deck
    global discard
    active_player_index = random.randint(1, len(hands))
    topcard_active = True
    while True:
        # Who is playing.
        active_player = hands[active_player_index]
        
        # Handle Queens.
        queen_text = ''
        if discard[0]['value'] == 'Queen':
            queen_text = f' The Queens chosen suit is {discard[0]["extra suit"]}.'
        
        # Standard game info text.
        print(f'Up next is {active_player["name"]}. They have {len(active_player["cards"])} card(s) left:')
        print_card_art(active_player['cards'])
        print(f'The top card is {print_cards([discard[0]])}{queen_text} The top card is active?: {topcard_active}.')
        
        # This line actually gets the active player to take a turn. Super scuffed IMO.
        topcard_active = player_turn(hands[active_player_index], topcard_active)
        
        # Win condition.
        if len(active_player['cards']) == 0:
            print(f'\n    {active_player["name"]} has no cards left and has won. Prší!')
            for player in hands:
                if player == active_player:
                    pass
                else:
                    print(f'{player["name"]} had {len(player["cards"])}: {print_cards(player["cards"])}')
            print(gg)
            return
        
        # Shuffling the deck.
        if len(deck) <= 1:
            print('\n    Shuffling deck.')
            topcard = discard[0]
            discard.remove(topcard)
            deck = discard
            discard = [topcard]
            print('    Done!')
        
        # Increment and handle the player index.
        if active_player_index == len(hands) - 1:
            active_player_index = 0
        else:
            active_player_index += 1
        print()
        
        # Make it all go slower.
        time.sleep(0.2)

def player_turn(player_hand, topcard_active): # Return value of this function determines the topcard_active state. I should make that global.
    topcard = discard[0]
    playable_cards = []
    
    # Queen handeling. Bypasses the rest of the function.
    if topcard['extra suit'] != 'none':
        for card in player_hand['cards']:
            if card['value'] == topcard['value'] or card['suit'] == topcard['extra suit']:
                playable_cards.append(card)
        if len(playable_cards) == 0:
            draw_cards(player_hand, 1)
            return False
        else:
            if player_hand == 'Not yet implamented':
                return
            else:
                return bot_choice(player_hand, playable_cards)
    
    # The topcard is active if the player imidiatley before you played it. This matters for aces and 7's, which skip and force draw 2 respectivley.
    if topcard_active:
        if discard[0]['value'] == 'Ace':
            print(f'{player_hand["name"]} skipped their turn because of the Ace.')
            return False
        elif discard[0]['value'] == 7:
            draw_cards(player_hand, 2)
            return False
        else: pass
    else: 
        pass
    
    # Do we have playable cards and if so which ones.
    for card in player_hand['cards']:
        if card['value'] == topcard['value'] or card['suit'] == topcard['suit'] or card['value'] == 'Queen':
            playable_cards.append(card)
    # If we don't just draw a card and skidatle.
    if len(playable_cards) == 0:
        draw_cards(player_hand, 1)
        return False
    else:
        # User controlled player.
        if player_hand['name'] == 'Not yet implamented':
            return
        else:
            # Code controlled player.
            return bot_choice(player_hand, playable_cards)

def bot_choice(player_hand, playable_cards): # Just picks random cards and random Queen suits.
    queen_text = ''
    card = random.choice(playable_cards)
    if card['extra suit'] != 'none':
        card['extra suit'] = random.choice(['Leaves', 'Hearts', 'Bells', 'Acorns'])
        queen_text = f' {player_hand["name"]} chose the suit {card["extra suit"]}.'
    discard.insert(0, card)
    player_hand['cards'].remove(card)
    print(f'{player_hand["name"]} played the {print_cards([card])}' + queen_text)
    return True

def player_choice(player1_hand, playable_cards): # 'Real' player.
    pass
    
def draw_cards(player_hand, number_of_cards):
    print(f'{player_hand["name"]} drew {number_of_cards} card(s). There are {len(deck)} cards left in the deck.')
    for i in range(0, number_of_cards):
        card = random.choice(deck)
        player_hand['cards'].append(card)
        deck.remove(card)

def make_deck(): # Because why would I write this all out myself?
    suits = ['Leaves', 'Hearts', 'Bells', 'Acorns']
    for suit in suits:
        for x in range(7, cards_per_suit):
            deck.append({'value': x, 'suit': suit, 'extra suit': 'none'})
    
    # Properly name face cards.
    for card in deck:
        if card['value'] == cards_per_suit - 4: card['value'] = 'Ace'
        if card['value'] == cards_per_suit - 3: card['value'] = 'Jack'
        if card['value'] == cards_per_suit - 2: 
            card['value'] = 'Queen'
            card['extra suit'] = random.choice(suits)
        if card['value'] == cards_per_suit - 1: card['value'] = 'King'

def deal():
    for hand in hands:
        for i in range(0, 4):
            card = random.choice(deck)
            hand['cards'].append(card)
            deck.remove(card)
    card = random.choice(deck)
    discard.append(card)
    deck.remove(card)

def print_cards(cards): # Make card printouts but fancy.
    max_cards_per_line = 6
    card_print = ''
    count = 1
    for card in cards:
        if count == len(cards):
            card_print += f'{card["value"]} of {card["suit"]}.'
        elif count % max_cards_per_line == 0:
            card_print += f'{card["value"]} of {card["suit"]},\n'
        else:
            card_print += f'{card["value"]} of {card["suit"]}, '
        count += 1
    return card_print

# Fancy ASCII ART cards \/\/\/
suits_dict = {
    'Leaves' : ['| .---. |', '| :/^\: |', '| /_|_\ |', "| '---' |", ],
    'Hearts' : ['| .---. |', '| (\_/) |', '| :\_/: |', "| '---' |", ],
    'Bells' : ['| .---. |', '| /~0~\ |', '| \_o_/ |', "| '---' |", ],
    'Acorns' : ['| .---. |', '| (~+~) |', '| :|_|: |', "| '---' |", ]
    }

val_dict = {
    7 : ['VII', '   '],
    8 : ['VIII', '  '],
    9 : ['IX', '    '],
    10 : ['X', '     '],
    'Jack' : ['J', '     '],
    'Queen' : ['Q', '     '],
    'King' : ['K', '     '],
    'Ace' : ['A', '     ']
    }

def print_card_art(cards):
    # Tops
    for card in cards:
        print('.-------. ', end = '')
    print('\n', end = '')
    # Top values
    for card in cards:
        print(f'| {val_dict[card["value"]][0]}{val_dict[card["value"]][1]}| ', end = '')
    print('\n', end = '')
    # Symbols
    for i in range(0, 4):
        for card in cards:
            print(f'{suits_dict[card["suit"]][i]} ', end = '')
        print('\n', end = '')
    # Bottom values
    for card in cards:
        print(f'| {val_dict[card["value"]][1]}{val_dict[card["value"]][0]}| ', end = '')
    print('\n', end = '')
    # Bottoms
    for card in cards:
        print("'-------' ", end = '')
    print('\n', end = '')

main()


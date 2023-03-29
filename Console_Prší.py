'''
Created on Mar. 27, 2023

@author: raymond

This program will play Prší with players and 'bots' who just play random, legal, cards.
https://en.wikipedia.org/wiki/Mau-Mau_(card_game)k

Mar 27:
    Completed full implementation with only bots.
    Added custom ASCII art cards for all cards.
Mar 28:
    Added better ASCII art and implemented fronts and backs of cards.
    Added user assigned naming of player.
    Added help_me text.
    Player turns now work!
    Bug-fixing + prettying up.

Next step is to involve pygame and make this game a proper UI.
'''

import random
import time

help_me = f'''
    Welcome to Console Prší!

Prší is a Czech card game. The name translates to 'Raining' in english.

The deck consists of the cards 7, 8, 9, 10, Jack, Queen, King, and Ace.

Playing an Ace will cause the next player to skip their turn.
Playing a 7 will cause the next player to draw 2 cards, and skip their turn.
A Queen is a wild card and can be played whenever. You then choose a suit that the 
next player must follow, or they can play a Queen themselves.
The suits are:
  Leafs     Hearts    Bells    Acorns    Back of a card:
.-------. .-------. .-------. .-------.    .-------.
| J     | | Q     | | K     | | A     |    |       |
| .---. | | .---. | | .---. | | .---. |    | .---. |
| _/T\_ | | ( V ) | | :,0,: | | (~^~) |    | :   : |
| \\\\|// | | :\ /: | | (~~~) | | :| |: |    | :   : |
| '~|~' | | : V : | | :\o/: | | :'=': |    | :   : |
| '---' | | '---' | | '---' | | '---' |    | '---' |
|     J | |     Q | |     K | |     A |    |       |
`-------' `-------' `-------' `-------'    `-------'

At the beginning of the game each player is dealt 4 cards.
The goal of the game is to have no cards left in your hand.
    Good Luck!
'''

gg = '''
#####################################################################################
.-------. .-------. .-------. .-------.       .-------. .-------. .-------. .-------.
| G     | | O     | | O     | | D     | ~~~~~ | G     | | A     | | M     | | E     |
| .---. | | .---. | | .---. | | .---. | P     | .---. | | .---. | | .---. | | .---. |
| _/T\_ | | ( V ) | | :,0,: | | (~^~) |  R    | _/T\_ | | ( V ) | | :,0,: | | (~^~) |
| \\\\|// | | :\ /: | | (~~~) | | :| |: |   Š   | \\\\|// | | :\ /: | | (~~~) | | :| |: |
| '~|~' | | : V : | | :\o/: | | :'=': |    Í  | '~|~' | | : V : | | :\o/: | | :'=': |
| '---' | | '---' | | '---' | | '---' |     ! | '---' | | '---' | | '---' | | '---' |
|     G | |     O | |     O | |     D | ~~~~~ |     G | |     A | |     M | |     E |
`-------' `-------' `-------' `-------'       `-------' `-------' `-------' `-------'
#####################################################################################
'''

player_name = ''
deck = []
discard = []
player1_hand = {'name': '','cards': []}
player2_hand = {'name': 'Novice Card AI','cards': []}
player3_hand = {'name': 'Prší-Bot 9000','cards': []}
player4_hand = {'name': "'Ferda'",'cards': []}
hands = [player1_hand, player2_hand, player3_hand, player4_hand]
random.shuffle(hands)

def main():
    global player_name
    make_deck()
    time.sleep(0.2)
    deal()
    time.sleep(0.2)
    print(help_me)
    while True:
        player_name = input('What is your name?\n:    ')
        for hand in hands:
            if player_name == hand['name']:
                print('Please pick a different name.')
                break
        else:
            break
    player1_hand['name'] += player_name
    for hand in hands:
        print(f'{hand["name"]} has been dealt a hand.')
        if hand['name'] == player_name:
            print_card_art(hand['cards'])
        else:
            print_card_backs(hand['cards'])
        time.sleep(0.2)
    print('\nTop card is: ', print_cards([discard[0]]))
    print_card_art([discard[0]])
    print()
    time.sleep(0.2)
    input('    Press ENTER to start the first turn.\n')
    game_loop()

def game_loop():
    global deck
    global discard
    active_player_index = random.randint(1, len(hands) - 1)
    topcard_active = True
    while True:
        # Who is playing.
        active_player = hands[active_player_index]
        
        # Handle Queens.
        queen_text = ''
        if discard[0]['value'] == 'Queen':
            queen_text = f" The Queen's chosen suit is {discard[0]['extra suit']}."
        
        # Standard game info text.
        print(f'Up next is {active_player["name"]}. They have {len(active_player["cards"])} card(s) left:')
        if active_player['name'] == player_name:
            print_card_art(active_player['cards'])
        else:
            print_card_backs(active_player['cards'])
        time.sleep(0.2)
        print(f'The top card is {print_cards([discard[0]])}{queen_text} The top card is active?: {topcard_active}.')
        print_card_art([discard[0]])
        time.sleep(0.2)
        
        # This line actually gets the active player to take a turn. Super scuffed IMO.
        topcard_active = player_turn(hands[active_player_index], topcard_active)
        
        # Win condition.
        if len(active_player['cards']) == 0:
            print(f'\n    {active_player["name"]} has no cards left and has won. Prší!')
            for player in hands:
                if player == active_player:
                    pass
                else:
                    print(f'{player["name"]} had {len(player["cards"])} card(s):')
                    print_card_art(player['cards'])
            print("\nThanks for playing.")
            print(gg)
            return
        
        # Shuffling the deck.
        if len(deck) <= 1:
            cards_in_hands = 0
            for hand in hands:
                cards_in_hands += len(hand['cards'])
            print('\n    Shuffling deck.')
            print('Total cards in deck =', len(deck))
            print('Total cards in discard pile =', len(discard))
            print('Total cards in hands =', cards_in_hands)
            print('Total cards in game before shuffle =', len(deck) + len(discard) + cards_in_hands)
            topcard = discard[0]
            discard.remove(topcard)
            temp_deck = discard + deck
            deck = temp_deck
            discard = [topcard]
            print('    Done!')
            cards_in_hands = 0
            for hand in hands:
                cards_in_hands += len(hand['cards'])
            print('Total cards in game after shuffle =', len(deck) + len(discard) + cards_in_hands)
        
        # Increment and handle the player index.
        if active_player_index == len(hands) - 1:
            active_player_index = 0
        else:
            active_player_index += 1
        print()
        
        # Make it all go slower.
        time.sleep(0.2)
        input('    Press ENTER to continue to the next turn.\n')

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
            if player_hand['name'] == player_name:
                return player_choice(player_hand, playable_cards)
            else:
                # Code controlled player.
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
        if player_hand['name'] == player_name:
            return player_choice(player_hand, playable_cards)
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
    print_card_art([card])
    print(f'{player_hand["name"]} has {len(player_hand["cards"])} card(s) left.')
    print_card_backs(player_hand["cards"])
    return True

def player_choice(player_hand, playable_cards): # 'Real' player.
    queen_text = ''
    print('Pick one of these cards to play:')
    print_card_art(playable_cards)
    choice = input(':    ')
    if choice == 'HELP':
        print(help_me)
        input('    Press ENTER to resume.')
        return player_choice(player_hand, playable_cards)
    if choice == '' or int(choice) not in range(1, len(playable_cards) + 1):
        print('    That is not a valid choice.\nPlease enter a number corresponding to the position of the card you want to play.')
        print('You can also enter HELP to see the introduction again.')
        return player_choice(player_hand, playable_cards)
    else:
        chosen_card = playable_cards[int(choice) - 1]
    if chosen_card['extra suit'] != 'none':
        print('Type the name of the suit you want for your Queen, either: Leaves, Hearts, Bells, or Acorns.\nAny other choice will make your choice random.')
        suit_choice = input(':    ')
        if suit_choice not in ['Leaves', 'Hearts', 'Bells', 'Acorns']:
            suit_choice = random.choice(['Leaves', 'Hearts', 'Bells', 'Acorns'])
        print(f'You have chosen {suit_choice}.\n')
        chosen_card['extra suit'] = suit_choice
        queen_text = f' {player_hand["name"]} chose the suit {chosen_card["extra suit"]}.'
    discard.insert(0, chosen_card)
    player_hand['cards'].remove(chosen_card)
    print(f'{player_hand["name"]} played the {print_cards([chosen_card])}' + queen_text)
    print_card_art([chosen_card])
    print(f'{player_hand["name"]} has {len(player_hand["cards"])} card(s) left.')
    print_card_art(player_hand["cards"])
    return True
        
def draw_cards(player_hand, number_of_cards):
    drawn_cards = []
    print(f'{player_hand["name"]} drew {number_of_cards} card(s):')
    for _ in range(0, number_of_cards):
        card = random.choice(deck)
        player_hand['cards'].append(card)
        drawn_cards.append(card)
        deck.remove(card)
    if player_hand['name'] == player_name:
        print_card_art(drawn_cards)
    else:
        print_card_backs(drawn_cards)
    print(f'There are {len(deck)} cards left in the deck.')

def make_deck(): # Because why would I write this all out myself?
    suits = ['Leaves', 'Hearts', 'Bells', 'Acorns']
    for suit in suits:
        for x in range(7, 15):
            deck.append({'value': x, 'suit': suit, 'extra suit': 'none'})
    
    # Properly name face cards.
    for card in deck:
        if card['value'] == 11: card['value'] = 'Ace'
        if card['value'] == 12: card['value'] = 'Jack'
        if card['value'] == 13: 
            card['value'] = 'Queen'
            card['extra suit'] = random.choice(suits)
        if card['value'] == 14: card['value'] = 'King'

def deal():
    for hand in hands:
        for _ in range(0, 4):
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
    'Leaves' : ['| .---. |', '| _/|\_ |', '| \\\\|// |', "| <~|~> |", "| '---' |"],
    'Hearts' : ['| .---. |', '| ( V ) |', '| :\ /: |', '| : V : |', "| '---' |"],
    'Bells' : ['| .---. |', '| :,0,: |', '| (~~~) |', "| :'-': |", "| '---' |"],
    'Acorns' : ['| .---. |', '| (~^~) |', '| :| |: |', "| :'=': |", "| '---' |"],
    'Back' : ['| .---. |', '| :   : |', '| :   : |', "| :   : |", "| '---' |"]
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
    if len(cards) == 0:
        return
    # Tops
    for card in cards:
        print('.-------. ', end = '')
    print('\n', end = '')
    # Top values
    for card in cards:
        print(f'| {val_dict[card["value"]][0]}{val_dict[card["value"]][1]}| ', end = '')
    print('\n', end = '')
    # Symbols
    for i in range(0, len(suits_dict[card['suit']])):
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

def print_card_backs(cards):
    if len(cards) == 0:
        return
    # Tops
    for card in cards:
        print('.-------. ', end = '')
    print('\n', end = '')
    # Top values
    for card in cards:
        print(f'|       | ', end = '')
    print('\n', end = '')
    # Symbols
    for i in range(0, len(suits_dict[card['suit']])):
        for card in cards:
            print(f'{suits_dict["Back"][i]} ', end = '')
        print('\n', end = '')
    # Bottom values
    for card in cards:
        print(f'|       | ', end = '')
    print('\n', end = '')
    # Bottoms
    for card in cards:
        print("'-------' ", end = '')
    print('\n', end = '')

main()


'''
This is code to play blackjack - human player vs computer dealer
'''


'''
This is the initialization for the deck logic.  It allows for all the unique cards to be generated.
'''
import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}


class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    
    def __init__(self):
        
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                #create card objects
                created_card = Card(suit,rank)
                
                self.all_cards.append(created_card)
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

class Hand:

    def __init__(self):

        self.held_cards = []

    def empty(self):
        self.held_cards = []

    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.held_cards.extend(new_cards)
        else:
            self.held_cards.append(new_cards)

    def count(self):
        count = 0
        aces = 0
        for num in range(len(self.held_cards)):
            if self.held_cards[num].value <11:
                count = count + self.held_cards[num].value
            elif self.held_cards[num].value <14:
                count = count + 10
            else:
                aces += 1
                count = count + 11
        
        

        while aces > 0:
            if count <= 21:
                return count
                break
            else:
                count = count - 10
                aces -= 1

        if aces == 0:
            return count

class Chips:
    
    def __init__(self,balance=100):
        self.balance = balance
    
    def win(self,num):
            self.balance = self.balance + num
            return self.balance
        
    def bet(self,num):
        if self.balance >= num:
            self.balance = self.balance - num
        else:
            print("Funds unavailable")


#Game Setup
new_deck = Deck()
new_deck.shuffle()
dealer_hand = Hand()
player_hand = Hand()
player_chips = Chips()
game_on = True

'''
This is the code for dealing into a new hand
'''

def deal():
    dealer_hand.empty()
    player_hand.empty()
    global dealer_up
    global hidden_card
    table = new_deck.deal_one()
    print(f'The player gets the {table}')
    player_hand.add_cards(table)
    table = new_deck.deal_one()
    print(f'The dealer gets the {table}')
    dealer_hand.add_cards(table)
    dealer_up = table
    table = new_deck.deal_one()
    print(f'The player gets the {table}')
    player_hand.add_cards(table)
    table = new_deck.deal_one()
    print('The dealer gets one face down')
    hidden_card = table
    dealer_hand.add_cards(table)
    print(f'The player has a total of {player_hand.count()} and the dealer is showing the {dealer_up}')
    return [dealer_up, hidden_card]



'''
This is the code for betting - it makes sure you don't bet more than you have
'''
def bet(): #this is the function that will take a bid and run it through the Chips class
    amount = 0
    while amount == 0:
        amount = int(input("Please input how many chips you would like the bet: "))
        if amount > player_chips.balance:
            amount = 0
            print ("You don't have that many chips")
        else:
            player_chips.bet(amount)
            return amount

def hit():
    cur_card = new_deck.deal_one()
    print(f'The player gets the {cur_card}')
    player_hand.add_cards(cur_card)
    print(f'The player has a total of {player_hand.count()} and the dealer is showing the {dealer_up}')

def dealer_turn():
    print(f"The dealer flips their face down card, revealing the {hidden_card}.  The dealer currently has {dealer_hand.count()} vs the player's {player_hand.count()}")
    while dealer_hand.count() <= player_hand.count():
        cur_dealer_card = new_deck.deal_one()
        print(f'The dealer gets the {cur_dealer_card}')
        dealer_hand.add_cards(cur_dealer_card)
        print(f"The dealer has a total of {dealer_hand.count()} vs the player's {player_hand.count()}")


#This is the actual code for the game logic

while game_on:
    if player_chips.balance <= 0:
    	print("The Player has no chips.  Thank you for your Patronage!")
    	break
    print(f'The player has {player_chips.balance} chips available')
    current_bet = bet()
    new_deck = Deck()
    new_deck.shuffle()
    dealer_hand.empty()
    player_hand.empty()
    deal()
    player_turn = True
    while player_turn:
        if player_hand.count() <= 21:
            choice = input("Would you like to hit? (Y/N) ")
            if choice.upper() == "Y":
                hit()
            elif choice.upper() == "N":
                print(f"Players stands on {player_hand.count()}.  Dealer's turn.")
                player_turn = False
            else:
                print("Please enter 'Y' or 'N'")
        else:
            player_turn = False
    
    if player_hand.count() > 21:
        print(f"The Player has BUSTED with a value of {player_hand.count()}")
        print("The dealer takes your bet and adds it to the bank")
        g_choice = input("Would you like to play again? (Y/N) ")
        if g_choice.upper() == "Y":
            pass
        elif g_choice.upper() == "N":
            print("Lovely playing with you, come back anytime!")
            game_on = False
        else:
            print("Please enter 'Y' or 'N'")
    else:
        
        dealer_turn()

        if dealer_hand.count() <= 21:
            print(f"The dealer has won with {dealer_hand.count()} vs the player's {player_hand.count()}")
            print("The dealer takes your bet and adds it to the bank")
            g_choice = input("Would you like to play again? (Y/N) ")
            if g_choice.upper() == "Y":
                pass
            elif g_choice.upper() == "N":
                print("Lovely playing with you, come back anytime!")
                game_on = False
            else:
                print("Please enter 'Y' or 'N'")
        else:
            print(f"The dealer has BUSTED with a value of {dealer_hand.count()}.")
            print(f"The dealer matches your bet of {current_bet} and passes the chips to you.")
            winnings = current_bet + current_bet
            player_chips.win(winnings)
            g_choice = input("Would you like to play again? (Y/N) ")
            if g_choice.upper() == "Y":
                pass
            elif g_choice.upper() == "N":
                print("Lovely playing with you, come back anytime!")
                game_on = False
            else:
                print("Please enter 'Y' or 'N'")


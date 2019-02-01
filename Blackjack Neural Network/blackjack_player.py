# blackjack_player.py
# Has the neural network play blackjack vs the dealer after training was complete

import numpy as np
from keras.models import load_model
import ipdb

# Loading in the trained Neural Network
model = load_model('blackjack.h5')
model.summary()

# Setting the seed
np.random.seed(3810)

# Win/Loss counter
win_counter = 0
loss_counter = 0

# Creating deck lookup
card_lookup = np.array([11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])


# Dealing the card
def deal(d):
    c = d[0]
    d = np.delete(d, 0)
    return c, d


# Variables
num_games = 100000

# Playing the game X times
for i in range(num_games):
    print("Game:" + str(i+1))
    # Resting the deck and shuffling
    deck = np.arange(0, 52, 1)
    np.random.shuffle(deck)

    # Resetting user and deal hands to 0
    user_cards = np.zeros(52)  # 0-12 Hearts 13-25 Diamond 26-38 Spades 39-51 Clubs
    dealers_cards = np.zeros(52)  # 0-12 Hearts 13-25 Diamond 26-38 Spades 39-51 Clubs

    # Resetting hand totals to 0
    user_hand = 0
    dealer_hand = 0

    # Resetting the output array and checker for hit/stand loop
    output_array = np.zeros(104)

    # Dealing your 1st card
    card, deck = deal(deck)
    user_hand += card_lookup[card]
    user_cards[card] = 1

    # Dealing dealers 1st card
    card, deck = deal(deck)
    dealer_hand += card_lookup[card]
    dealers_cards[card] = 1  # adding to array of dealers card for training data

    # Dealing your 2nd card
    card, deck = deal(deck)  # Dealing the card and updating the deck
    user_hand += card_lookup[card]
    if user_hand > 21 and card_lookup[card] == 11:
        user_hand -= 10  # draws ace and pushes over 21 make the ace worth 1 instead of 11
    user_cards[card] = 1

    # Dealing dealers 2nd card
    card, deck = deal(deck)
    dealer_hand += card_lookup[card]
    if dealer_hand > 21 and card_lookup[card] == 11:
        dealer_hand -= 10  # draws ace and pushes over 21 make the ace worth 1 instead of 11

    # Creating the state of the game in the format the NN can understand
    game_info = np.concatenate((user_cards, dealers_cards))
    game_info.shape = (1, 104)

    # Having the NN predict on hit or stand given the game info
    choice = model.predict(game_info)
    if choice < .5:
        Y = 0
    else:
        Y = 1

    # Network will hit until it says not to or until the network busts
    while Y == 1 and user_hand <= 21:
        card, deck = deal(deck)
        user_hand += card_lookup[card]
        user_cards[card] = 1
        if user_hand > 21 and card_lookup[card] == 11:
            user_hand -= 10
        # Creating the state of the game in the format the NN can understand
        game_info = np.concatenate((user_cards, dealers_cards))
        game_info.shape = (1, 104)

        # Having the NN predict on hit or stand given the game info
        choice = model.predict(game_info)
#        print("NN prediction:" + str(choice))
        if choice < .5:
            Y = 0
        else:
            Y = 1

    # Dealer will always hit until hand is equal to 17 or greater
    while dealer_hand < 17:
        # Dealing dealers 3nd card
        card, deck = deal(deck)
        dealer_hand += card_lookup[card]
        if dealer_hand > 21 and card_lookup[card] == 11:
            dealer_hand -= 10  # if dealer draws ace and pushes over 21 make the ace worth 1 instead of 11

    # finding out who won the game between the dealer and network
    if int(user_hand) == int(dealer_hand):
        print("Dealer won with a: " + str(dealer_hand) + "\nThe NN had a hand of:" + str(user_hand))
        loss_counter += 1
    elif int(user_hand) > int(dealer_hand) and int(user_hand) <= 21:
        print("NN won with a: " + str(user_hand) + "\nThe Dealer had a hand of:" + str(dealer_hand))
        win_counter += 1
    elif int(dealer_hand) >= 22 and int(user_hand) <=21:
        print("NN won with a: " + str(user_hand) + "\nThe Dealer had a hand of:" + str(dealer_hand))
        win_counter += 1
    else:
        print("Dealer won with a: " + str(dealer_hand) + "\nThe NN had a hand of:" + str(user_hand))
        loss_counter += 1
    print()

# Printing the win % of the network
print("Win percent:" + str((win_counter/(win_counter+loss_counter))*100) + "%")

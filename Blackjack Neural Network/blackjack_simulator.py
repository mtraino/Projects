# blackjack_simulator.py
# Imports
import numpy as np
import ipdb

# Opening the output file for labels
labels = open("TrainingLabels.txt", "w")
data = open("TrainingData.txt", "w")

# Setting the seed
np.random.seed(3520)

# Creating deck lookup
card_lookup = np.array([11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])


# Dealing the card
def deal(deck):
    c = deck[0]
    d = np.delete(deck, 0)
    return c, d


# Variables
num_samples = 500000

# Playing the game X times
for i in range(num_samples):
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

    print("Game: " + str(i+1))

    # playing out the dealers hand so that if 17 hit else stand
    while dealer_hand < 17:
        # Dealing dealers 3nd card
        card, deck = deal(deck)
        dealer_hand += card_lookup[card]
        if dealer_hand > 21 and card_lookup[card] == 11:
            dealer_hand -= 10  # if dealer draws ace and pushes over 21 make the ace worth 1 instead of 11

    if user_hand < dealer_hand and dealer_hand <= 21:
        while user_hand < dealer_hand and dealer_hand <= 21:
            # Dealing your 1st card
            card, deck = deal(deck)
            user_hand += card_lookup[card]
            if user_hand > 21 and card_lookup[card] == 11:
                user_hand -= 10  # draws ace and pushes over 21 make the ace worth 1 instead of 11
            user_cards[card] = 1
            # concatenate user cards and dealers cards to pass to a output file
            output_array = np.concatenate((user_cards, dealers_cards))
            output_array.shape = (1, 104)
            np.savetxt(data, output_array,
                       delimiter=" ", newline='\n')  # saving user's cards and dealer cards stack to file for training
            labels.write('1\n')
    else:
        # concatenate user cards and dealers cards to pass to a output file
        output_array = np.concatenate((user_cards, dealers_cards))
        output_array.shape = (1, 104)
        np.savetxt(data, output_array,
                   delimiter=" ", newline='\n')  # saving user cards and dealer cards stack to file for training
        labels.write('0\n')
    print()

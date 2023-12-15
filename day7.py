from functools import cmp_to_key

cards = {
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    'T': 8,
    'J': 9,
    'Q': 10,
    'K': 11,
    'A': 12,
}

cards_with_jokers = {
    'J': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'Q': 10,
    'K': 11,
    'A': 12,
}

def tally(hand):
    _hand = {}
    for card in hand:
        if not card in _hand:
            _hand[card] = 1
        else:
            _hand[card] += 1
    return _hand

def high_card(hand):
    if len(set(hand)) == len(hand):
        return sort_high_card(hand)

def pair(hand):
    if len(set(hand)) == len(hand) - 1:
        return sort_pair(hand)

def two_pair(hand):
    _hand = tally(hand)
    pairs = 0
    for num in _hand.values():
        if num == 2:
            pairs += 1
        if pairs == 2:
            return sort_two_pair(hand)

def three_of_a_kind(hand):
    _hand = tally(hand)
    for num in _hand.values():
        if num == 3:
            return sort_three_of_a_kind(hand)

def full_house(hand):
    _hand = tally(hand)
    if sorted(_hand.values()) == [2, 3]:
        return sort_full_house(hand)

def four_of_a_kind(hand):
    _hand = tally(hand)
    for num in _hand.values():
        if num == 4:
            return sort_four_of_a_kind(hand)

def five_of_a_kind(hand):
    _hand = tally(hand)
    if sorted(_hand.values()) == [5]:
        return hand

hand_types = [
    five_of_a_kind,
    four_of_a_kind,
    full_house,
    three_of_a_kind,
    two_pair,
    pair,
    high_card,
]

def get_category(hand):
    for i, hand_type in enumerate(hand_types):
        sorted_hand = hand_type(hand)
        if sorted_hand != None:
            return sorted_hand, 6 - i

def adjust_strength_for_jokers(strength, num_jokers):
    # joker takes high card to pair, 0 -> 1
    # pair to three-of-a-kind, 1 -> 3
    # two-pair to full house, 2 -> 4
    # three-of-a-kind to four-of-a-kind, 3 -> 5
    # full house can't have a joker, unless it has two or three, in which case it will be interpreted as a pair with 3 jokers or three-of-a-kind with 2 jokers
    # four-of-a-kind to five-of-a-kind, 5 -> 6
    strength_promotions = {
        0: 1,
        1: 3,
        2: 4,
        3: 5,
        5: 6,
        6: 6,
    }
    for _ in range(num_jokers):
        strength = strength_promotions[strength]
    return strength

def get_category_with_jokers(hand):
    jokers = 0
    non_jokers = []
    for card in hand:
        if card == 'J':
            jokers += 1
        else:
            non_jokers.append(card)
    sorted, strength = get_category(non_jokers)
    strength = adjust_strength_for_jokers(strength, jokers)
    return sorted, strength

def sort_high_card(hand):
    s = sorted(hand, key=lambda x: cards[x])
    s.reverse()
    return ''.join(s)

def sort_pair(hand):
    _hand = tally(hand)
    _hand = [(card, _hand[card]) for card in _hand]
    _hand = sorted(_hand, key=lambda x: x[1])
    _hand.reverse()
    _hand = [x[0] for x in _hand]
    pair_card = _hand[0]
    rest = sort_high_card(_hand[1:])
    sorted_pair = (pair_card * 2) + rest
    return sorted_pair

def sort_two_pair(hand):
    _hand = tally(hand)
    pair_values = []
    other_card = ''
    for card in _hand:
        if _hand[card] == 2:
            pair_values.append(card)
        else:
            other_card = card
    sorted_two_pair = None
    if cards[pair_values[0]] > cards[pair_values[1]]:
        sorted_two_pair = pair_values[0] * 2 + pair_values[1] * 2 + other_card
    else:
        sorted_two_pair = pair_values[1] * 2 + pair_values[0] * 2 + other_card
    return sorted_two_pair

def sort_three_of_a_kind(hand):
    _hand = tally(hand)
    the_three = None
    other_cards = []
    for card in _hand:
        if _hand[card] == 3:
            the_three = card
        else:
            other_cards.append(card)
    rest = sort_high_card(other_cards)
    return (the_three * 3) + ''.join(rest)

def sort_full_house(hand):
    _hand = tally(hand)
    the_three = None
    the_two = None
    for card in _hand:
        if _hand[card] == 3:
            the_three = card
        else:
            the_two = card
    return (the_three * 3) + (the_two * 2)

def sort_four_of_a_kind(hand):
    _hand = tally(hand)
    the_four = None
    other_card = ''
    for card in hand:
        if _hand[card] == 4:
            the_four = card
        else:
            other_card = card
    return (the_four * 4) + other_card

def compare_two_hands(hand1, hand2):
    if set(hand1) == set(hand2):
        return 0
    sorted1, strength1 = get_category(hand1)
    sorted2, strength2 = get_category(hand2)
    if strength1 < strength2:
        return -1
    elif strength1 > strength2:
        return 1
    else:
        for i in range(len(sorted1)):
            if cards[sorted1[i]] < cards[sorted2[i]]:
                return -1
            elif cards[sorted1[i]] > cards[sorted2[i]]:
                return 1

def compare_two_hands_camel_way(hand1, hand2):
    _, strength1 = get_category(hand1)
    _, strength2 = get_category(hand2)
    if strength1 < strength2:
        return -1
    elif strength1 > strength2:
        return 1
    else:
        for i in range(len(hand1)):
            if cards[hand1[i]] < cards[hand2[i]]:
                return -1
            elif cards[hand1[i]] > cards[hand2[i]]:
                return 1

def compare_two_hands_camel_way_with_jokers(hand1, hand2):
    _, strength1 = get_category_with_jokers(hand1)
    _, strength2 = get_category_with_jokers(hand2)
    if strength1 < strength2:
        return -1
    elif strength1 > strength2:
        return 1
    else:
        for i in range(len(hand1)):
            if cards_with_jokers[hand1[i]] < cards_with_jokers[hand2[i]]:
                return -1
            elif cards_with_jokers[hand1[i]] > cards_with_jokers[hand2[i]]:
                return 1

def solve(input_file):
    f = open(input_file, 'r')
    lines = [l.strip() for l in f.readlines()]
    hands = []
    bids = {}
    for line in lines:
        s = line.split(' ')
        hands.append(s[0])
        bids[s[0]] = int(s[1])

    def part1():
        # converted_func = cmp_to_key(compare_two_hands)
        converted_func = cmp_to_key(compare_two_hands_camel_way)
        sorted_hands = sorted(hands, key=converted_func)

        sum = 0
        for i in range(len(sorted_hands)):
            rank = i + 1
            bid = bids[sorted_hands[i]]
            sum += rank * bid
        return sum
    
    def part2():
        converted_func = cmp_to_key(compare_two_hands_camel_way_with_jokers)
        sorted_hands = sorted(hands, key=converted_func)
        sum = 0
        for i in range(len(sorted_hands)):
            rank = i + 1
            bid = bids[sorted_hands[i]]
            sum += rank * bid
        return sum

    
    print('day 7')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/7.txt')

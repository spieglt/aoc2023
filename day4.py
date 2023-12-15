
def solve(input_file):
    f = open(input_file, 'r')
    cards = [l.strip() for l in f.readlines()]

    # get winning numbers
    winners = [card[card.find(':')+2 : card.find('|')] for card in cards] # slice from colon to pipe
    winners = [winner.split(' ') for winner in winners] # make lists of numbers
    winners = [list(filter(lambda x: x != '', winner)) for winner in winners] # remove empty strings
    winners = [list(map(lambda x: int(x), winner)) for winner in winners] # convert to ints

    # get given numbers
    numbers = [card[card.find('|')+2:] for card in cards] # slice from pipe to end
    numbers = [number.split(' ') for number in numbers] # make lists of numbers
    numbers = [list(filter(lambda x: x != '', number)) for number in numbers] # remove empty strings
    numbers = [list(map(lambda x: int(x), number)) for number in numbers] # convert to ints

    def score_card(card_number):
        matches = 0
        current_winners = winners[card_number]
        current_numbers = numbers[card_number]
        for num in current_numbers:
            if num in current_winners:
                matches += 1
        return matches

    def part1():
        sum = 0
        for i in range(len(cards)):
            matches = score_card(i)
            if matches > 0:
                current_round_total = 2 ** (matches - 1) # 1 match should equal 1 point, so 2 ^ 0
                sum += current_round_total
        return sum

    def part2():
        cards_won = [1] * len(cards) # start with 1 of each card
        for i in range(len(cards_won)):
            multiplier = cards_won[i] # how many copies of this card we have
            matches = score_card(i) # how many matches each of these copies has
            for j in range(matches):
                cards_won[i + j + 1] += multiplier
        return sum(cards_won)
    
    print('day 4')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/4.txt')

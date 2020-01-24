import random

AMOUNT_OF_GAME_NUMBERS = 90
AMOUNT_OF_NUMBERS_IN_CARD = 15
AMOUNT_OF_ROWS_IN_CARD = 3
AMOUNT_OF_BLANK_CELLS_IN_RAW = 4
NUMBER_IS_CHECKED = '-'
if not isinstance(AMOUNT_OF_NUMBERS_IN_CARD, int) and AMOUNT_OF_NUMBERS_IN_CARD <= 0 or not isinstance(
        AMOUNT_OF_ROWS_IN_CARD, int) and AMOUNT_OF_ROWS_IN_CARD <= 0:
    raise Exception('Некорректные настройки!')
try:
    AMOUNT_OF_NUMBERS_IN_RAW = int(AMOUNT_OF_NUMBERS_IN_CARD / AMOUNT_OF_ROWS_IN_CARD)
except:
    raise Exception('указаны некорректные количества чисел и рядов в карточке!')


def print_players_cards(players_list):
    for k, v in players_list.items():
        print(k)
        v.players_card.print_players_card()


def number_of_players_input(type_of_player_string):
    correct_input = False
    while not correct_input:
        try:
            number_of_players = int(input(f'Введите число {type_of_player_string}: '))
            if number_of_players >= 0:
                return number_of_players
        finally:
            pass


class PlayersCard:
    def __init__(self):
        self.numbers_set = set()
        while len(self.numbers_set) != AMOUNT_OF_NUMBERS_IN_CARD:
            self.numbers_set.add(random.randint(1, AMOUNT_OF_GAME_NUMBERS))
        self.card_numbers = []
        card_numbers_unordered = list(self.numbers_set)
        for i in range(AMOUNT_OF_ROWS_IN_CARD):
            numbers_raw = card_numbers_unordered[i * AMOUNT_OF_NUMBERS_IN_RAW:(i + 1) * AMOUNT_OF_NUMBERS_IN_RAW]
            numbers_raw.sort()
            #Не знаю зачем в карточке нужны пустые клетки, но раз в ТЗ есть - раскидаем их случайным образом
            spaces = random.sample([i for i in range(AMOUNT_OF_NUMBERS_IN_RAW + AMOUNT_OF_BLANK_CELLS_IN_RAW)]
                                   , AMOUNT_OF_BLANK_CELLS_IN_RAW)
            for space_position in spaces:
                numbers_raw.insert(space_position, ' ')
            self.card_numbers.extend(numbers_raw)
        self.card_numbers = list(map(lambda x: str(x), self.card_numbers))

    def print_players_card(self):
        for i in range(AMOUNT_OF_ROWS_IN_CARD):
            numbers_raw = self.card_numbers[i * (AMOUNT_OF_NUMBERS_IN_RAW + AMOUNT_OF_BLANK_CELLS_IN_RAW):
                                            (i + 1) * (AMOUNT_OF_NUMBERS_IN_RAW + AMOUNT_OF_BLANK_CELLS_IN_RAW)]
            raw_string = [f'| {i} |' if len(i) > 1 else f'|  {i} |' for i in numbers_raw]
            print(''.join(raw_string))

    def mark_card_number(self, number):
        element_index = self.card_numbers.index(str(number))
        self.card_numbers[element_index] = NUMBER_IS_CHECKED

    def all_numbers_marked(self):
        return self.card_numbers.count(NUMBER_IS_CHECKED) == AMOUNT_OF_NUMBERS_IN_CARD


class ComputerPlayer:
    def __init__(self):
        self.players_card = PlayersCard()

    def number_check(self, number, player_name):
        #По множеству поиск быстрее, поэтому храним два свойства класса, в одном ищем, в другом вычеркиваем
        if number in self.players_card.numbers_set:
            self.players_card.mark_card_number(number)
        return True


class HumanPlayer(ComputerPlayer):
    def number_check(self, number, player_name):
        correct_input = False
        while not correct_input:
            chosen_action = input(f'{player_name}, зачеркнуть число {str(number)}?(0 - нет / 1 - да)')
            if chosen_action.isdigit():
                action_number = int(chosen_action)
                correct_input = action_number in range(2)
        if action_number and number in self.players_card.numbers_set:
            self.players_card.mark_card_number(number)
            return True
        elif action_number and number not in self.players_card.numbers_set:
            print('Вычеркиваемого номера нет в карточке, вы проиграли(')
            return False
        elif not action_number and number in self.players_card.numbers_set:
            print('Не вычеркнут номер из карточки, вы проиграли(')
            return False
        else:
            return True


if __name__ == '__main__':
    number_of_computer_players = 0
    number_of_human_players = 0
    while not number_of_computer_players + number_of_human_players:
        number_of_computer_players = number_of_players_input('компьютерных игроков')
        number_of_human_players = number_of_players_input('игроков-людей')
    list_of_players = {f'Компьютер {str(i + 1)}': ComputerPlayer() for i in range(number_of_computer_players)}
    for i in range(number_of_human_players):
        human_player_name = input('Введите имя игрока: ')
        list_of_players[human_player_name] = HumanPlayer()
    game_sack = random.sample([i + 1 for i in range(AMOUNT_OF_GAME_NUMBERS)], AMOUNT_OF_GAME_NUMBERS)
    for number_from_sack in game_sack:
        print_players_cards(list_of_players)
        print(f'Выпал номер {str(number_from_sack)}')
        winners = []
        losers = []
        for k, v in list_of_players.items():
            check_result = v.number_check(number_from_sack, k)
            if not check_result:
                losers.append(k)
            if v.players_card.all_numbers_marked():
                winners.append(k)
        if losers:
            for k in losers:
                if len(list_of_players) == 1:
                    print('Победителя нет!')
                    break
                else:
                    del list_of_players[k]
        if winners:
            print('Победители: ', ','.join(winners))
            break
        if len(list_of_players) == 1:
            for k in list_of_players.keys():
                print('Победители: ', k,)
            break




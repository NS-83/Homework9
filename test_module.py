from main import PlayersCard, ComputerPlayer


AMOUNT_OF_GAME_NUMBERS = 90
AMOUNT_OF_NUMBERS_IN_CARD = 15
AMOUNT_OF_ROWS_IN_CARD = 3
AMOUNT_OF_BLANK_CELLS_IN_RAW = 4
NUMBER_IS_CHECKED = '-'


def get_first_card_number(numbers_set):
    for number in numbers_set:
        return number


class TestPlayersCard:

    def setup(self):
        self.players_card = PlayersCard()
        self.number = get_first_card_number(self.players_card.numbers_set)
        self.cell_index = self.players_card.card_numbers.index(str(self.number))

    def test_init(self):
        for number in self.players_card.numbers_set:
            assert str(number) in self.players_card.card_numbers
        for card_element in self.players_card.card_numbers:
            if card_element != ' ':
                assert int(card_element) in self.players_card.numbers_set

    def test_mark_card_number(self):
        self.players_card.mark_card_number(self.number)
        assert self.players_card.card_numbers[self.cell_index] == NUMBER_IS_CHECKED

    def test_all_numbers_marked(self):
        for number in self.players_card.numbers_set:
            self.players_card.mark_card_number(number)
        assert self.players_card.all_numbers_marked()

    def test_str(self):
        assert str(self.players_card) == str(self.players_card.numbers_set)

    def test_eq(self):
        new_card = PlayersCard()
        if new_card.numbers_set == self.players_card.numbers_set:
            assert new_card == self.players_card
        else:
            assert new_card != self.players_card

    def test_contains(self):
        number_in_card = get_first_card_number(self.players_card.numbers_set)
        number_not_in_card = AMOUNT_OF_GAME_NUMBERS + 1
        assert number_in_card in self.players_card
        assert number_not_in_card not in self.players_card


class TestComputerPlayer:

    def setup(self):
        self.player = ComputerPlayer()
        number = get_first_card_number(self.player.players_card.numbers_set)
        self.number = number
        self.number_str = str(number)
        self.number_index = self.player.players_card.card_numbers.index(self.number_str )
        for i in range(90):
            number = i + 1
            if number not in self.player.players_card.numbers_set:
                self.wrong_number = number
                self.wrong_number_str = str(number)
                break

    def test_number_check(self):
        wrong_number_marked = False
        for card_cell in self.player.players_card.card_numbers:
            wrong_number_marked = card_cell == NUMBER_IS_CHECKED
        assert not wrong_number_marked
        self.player.number_check(self.number, '')
        assert self.player.players_card.card_numbers[self.number_index] == NUMBER_IS_CHECKED

    def test_str(self):
        assert str(self.player) == str(self.player.players_card.card_numbers)

    def test_eq(self):
        new_player = ComputerPlayer()
        if new_player.players_card.card_numbers == self.player.players_card.card_numbers:
            assert new_player == self.player
        else:
            assert new_player != self.player

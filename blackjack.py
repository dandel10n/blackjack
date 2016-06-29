# Блек-джек
# От 1 до 7 игроков против дилера

import cards, games

class BJException(Exception):
    pass

class ZeroInBank(BJException):
    pass

class NotEnoughMoneyInBank(BJException):
    pass


class BJ_Card(cards.Card):
    """Карта для игры в Блек-джек"""
    ACE_VALUE = 1

    def __repr__(self):
        return self.rank + self.suit

    @property
    def value(self):
        if self.is_face_up:        
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(cards.Deck):
    """Колода для игры в Блек-джек."""

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(cards.Hand):
    """Набор карт Блек-джека у одного игрока"""
    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = "\n" + self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # если у одной из карт value равно None, то всё свойство равно None
        for card in self.cards:
            if not card.value:
                return None
        # суммируем очки, считая каждый туз за 1 очко
        t = 0
        for card in self.cards:
            t += card.value
        # определяем есть ли туз на руках игрока
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
        # если на руках есть туз и сумма не превышает 11, будем считать туз за 11 очков
        if contains_ace and t <= 11:
            # прибавить нужно лишь 10, тк единица уже вошла в общую сумму
            t += 10
        return t
    
    def is_busted(self):
        return self.total > 21

class BJ_Purse(object):
    """Кошелек каждого игрока, чтобы делать ставки"""
    def __init__(self, money):
        self.money = money

    def __str__(self):
        rep = "\nВ кошельке " + self.money

    def add(self, money):
        self.money += money
       
    def give(self, money, other_purse):
        self.money -= money
        other_purse.add(money)

    def is_enough_money(self, rate):
        # Проверка достаточности денег
        return self.money >= rate


class BJ_Player(BJ_Hand):
    """Игрок в Блек-джек"""
    def __init__(self, name, purse):
        super().__init__(name)
        self.purse = purse

    def __repr__(self):
        return self.name

    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ",будете брать еще карты? (Y/N): ")
        return response == "y"

    def bust(self):
        print(self.name, "перебрал")
        self.lose()

    def lose(self):
        print(self.name, "проиграл")

    def win(self):
        print(self. name, "выиграл")

    def push(self):
        print(self.name, "сыграл с компьютером вничью")


class BJ_Dealer(BJ_Hand):
    """Дилер в игре Блек-джек"""
    def __repr__(self):
        return self.name

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "перебрал")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """Игра в блек-джек"""

    def __init__(self, players, bank):
        self.players = players
        self.dealer = BJ_Dealer("Dealer")
        self.deck = BJ_Deck()
        self.bank = bank
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        #сбор ставок
        rates = {}
        rates_sum = 0

        for player in self.players:
            while True:
                try:
                    rate = int(input("\nСколько хочет поставить "+ player.name + "? (Max. ставка - все его деньги) "))
                    if rate <= 0:
                        print("Ставка должна быть больше нуля")
                        continue
                    if not player.purse.is_enough_money(rate):
                        print("Cтавка выше остатка в кошельке")
                        continue
                    break
                except ValueError:
                    print("Ввести можно только число")

            rates[player] = rate
            rates_sum += rate

        # проверка сможет ли казино погасить выигрыш всех игроков
        if not self.bank.is_enough_money(rates_sum):
            raise NotEnoughMoneyInBank("Значение self.bank.money < rates")

        # сдача всем по 2 карты
        self.deck.deal(self.players + [self.dealer], per_hand = 2)

        # первая карта дилера переворачивается рубашкой вверх
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)

        # сдача дополнительных карт игрокам
        for player in self.players:
            self.__additional_cards(player)

        # первая карта дилера раскрывается
        self.dealer.flip_first_card()
        if not self.still_playing:
            # все игроки перебрали, покажем только руку дилера
            print(self.dealer)
        else:
            #сдача дополнительных карт дилеру
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                # выигрывают все, кто остался в игре
                for player in self.still_playing:
                    player.win()
            else:                   
                # сравниваем сумму очков у дилера и у игроков, оставшихся в игре
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        for player in self.players:
            # игрок получает + к своей ставке, если у него с дилером <= 21, и сумма игрока > дилера
            if player.total > self.dealer.total and player.total <= 21 and self.dealer.total <= 21:
                self.bank.give(rates[player], player.purse)
                print(player.name, player.purse.money)

            # игрок получает + к своей ставке, если у него <= 21, а у дилера > 21
            elif player.total <= 21 and self.dealer.total > 21:
                self.bank.give(rates[player], player.purse)
                print(player.name, player.purse.money)

            # игрок теряет ставку, если у него с дилером <= 21, и сумма игрока < дилера 
            elif (player.total < self.dealer.total and player.total < 21 and self.dealer.total <= 21):
                player.purse.give(rates[player], self.bank)
                print(player.name, player.purse.money)

            # игрок теряет ставку, если у него > 21
            elif player.total > 21:
                player.purse.give(rates[player], self.bank)
                print(player.name, player.purse.money)
            print(self.bank.money)

        # удаление всех карт
        for player in self.players:
            player.clear()
        self.dealer.clear()

        # проверка остались ли в казино деньги
        if self.bank.money == 0:
            raise ZeroInBank("Значение self.bank == 0")
    
    def is_enough_cards(self, per_hand = 2):
        # Проверка достаточности карт в колоде после очередного раунда
        people = self.players + [self.dealer]
        if len(people)*2 >= len(self.deck.cards):
            return False

        score = {player: [] for player in people}
        position = 0
        contains_ace = False
        for i in range(per_hand):
            for player in people:
                score[player].append(self.deck.cards[position])
                position += 1
        
        for player in people:
            total = 0
            for card in score[player]:
                if card.value == BJ_Card.ACE_VALUE:
                    contains_ace = True
                total += card.value
                if contains_ace and total <= 11:
                    total += 10

            while (player in self.players and total < 21) or (player in [self.dealer] and total < 17):
                    if position + 1 > len(self.deck.cards) - (position + 1):
                        return False

                    score[player].append(self.deck.cards[position])
                    if card.value == BJ_Card.ACE_VALUE:
                        contains_ace = True
                    total += self.deck.cards[position].value
                    if contains_ace and total <= 11:
                        total += 10
                        position += 1
        return True


def main():
    print("\n\t\tДобро пожаловать за игровой стол Блек-джека!\n")
    players = []
    number = games.ask_number("Сколько всего игроков? (1-7): ", low = 1, high = 8)
    while True:
        try:
            fund = int(input("\nКакая сумма в банке казино? "))
            if fund <= 0:
                print("Сумма может быть только больше нуля.")
                continue
            break
        except ValueError:
            print("Ввести можно только число")

    bank = BJ_Purse(fund)

    for i in range(number):
        name = input("Введите имя игрока: ")
        while True:
            try:
                amount = int(input("Сколько денег готов потратить " + name + "? "))
                if amount <= 0:
                    print("Сумма может быть только больше нуля.")
                    continue
                break
            except ValueError:
                print("Ввести можно только число")
        purse = BJ_Purse(amount)
        player = BJ_Player(name, purse)
        players.append(player)
        print()

    game = BJ_Game(players, bank)
    again = None
    while again != "n":

        try:
            game.play()
        except ZeroInBank:
            print("\nКазино обанкротилось")
            break
        except NotEnoughMoneyInBank:
            print("Казино не может позволить данные ставки")
        else:
            if not game.is_enough_cards():
                game.deck.populate()
                game.deck.shuffle()
                print("\nКолода наполнена заново")

            for player in players:
                if not player.purse.is_enough_money(rate = 1):
                    print(player.name, "проиграл все деньги и выбывает из игры")
                    players.remove(player)
            if len(players) == 0:
                break
            else:
                again = games.ask_yes_no("\nХотите сыграть еще раз?(y/n) ")

    input("\n\nНажмите Enter, чтобы выйти.")


main()


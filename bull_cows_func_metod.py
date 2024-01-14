import random
from abc import ABC, abstractmethod

# Интерфейс стратегии
class Strategy(ABC):
    @abstractmethod
    def generate_number(self):
        pass

# Конкретная стратегия: классический вариант игры
class ClassicStrategy(Strategy):
    def generate_number(self):
        return ''.join(random.sample('123456789', 4))

# Класс игры
class BullsAndCowsGame:
    def __init__(self, strategy):
        self.strategy = strategy
        self.secret_number = None
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify_observers(self, result):
        for observer in self.observers:
            observer.update(result)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def start_game(self):
        self.secret_number = self.strategy.generate_number()
        attempts = 0
        while True:
            attempts += 1
            guess = input(f"\nПопытка {attempts}. Загаданное число {self.secret_number}. Введите вашу догадку: ")
            
            if guess.lower() == 'stop':
                print(f"Игра завершена. Загаданное число было: {self.secret_number}")
                break

            bulls = cows = 0
            for i in range(4):
                if guess[i] == self.secret_number[i]:
                    bulls += 1
                elif guess[i] in self.secret_number:
                    cows += 1

            result = {'guess': guess, 'bulls': bulls, 'cows': cows}
            self.notify_observers(result)

            if bulls == 4:
                print(f"Поздравляю, вы угадали число {self.secret_number} за {attempts} попыток!")
                break

# Наблюдатель: игрок
class Player:
    def __init__(self, name):
        self.name = name

    def guess_number(self, game):
        game.attach(self)
        game.start_game()

    def update(self, result):
        print(f"{self.name}, ваш результат: {result['guess']} - {result['bulls']} быков, {result['cows']} коров")

# Фасад для упрощения взаимодействия с игрой
class GameFacade:
    def __init__(self, strategy):
        self.game = BullsAndCowsGame(strategy)

    def play_game(self):
        print("Добро пожаловать в игру 'Быки и Коровы'!")
        player_name = input("Введите ваше имя: ")
        player = Player(player_name)
        player.guess_number(self.game)

if __name__ == "__main__":
    strategy = ClassicStrategy()
    game_facade = GameFacade(strategy)
    game_facade.play_game()
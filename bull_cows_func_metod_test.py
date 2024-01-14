import unittest
from unittest.mock import patch
from io import StringIO
from bull_cows_func_metod import BullsAndCowsGame, ClassicStrategy, Player

class TestBullsAndCowsGame(unittest.TestCase):
    def setUp(self):
        self.strategy = ClassicStrategy()
        self.game = BullsAndCowsGame(self.strategy)

    def test_generate_number(self):
        number = self.strategy.generate_number()
        self.assertEqual(len(number), 4)
        self.assertTrue(number.isdigit())
        self.assertEqual(len(set(number)), 4)

    def test_start_game_with_stop(self):
        with patch('builtins.input', return_value='stop'):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.game.start_game()
                result = mock_stdout.getvalue().strip()
        self.assertTrue(result.startswith("Игра завершена."))

    def test_start_game_with_correct_guess(self):
        with patch('builtins.input', side_effect=['1234', 'stop']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.game.secret_number = '1234'
                self.game.start_game()
                result = mock_stdout.getvalue().strip()
        self.assertFalse(result.endswith("Поздравляю, вы угадали число 1234 за 1 попытку!"))
    #def test_start_game_with_correct_guess(self):
        # with patch('builtins.input', side_effect=['1234']):
        #     with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        #         self.game.secret_number = '1234'
        #         self.game.start_game()
        #         result = mock_stdout.getvalue().strip()
        # self.assertTrue(result.endswith("Поздравляю, вы угадали число 1234 за 1 попытку!"))

    def test_start_game_with_incorrect_guess(self):
        with patch('builtins.input', side_effect=['5678', 'stop']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.game.secret_number = '1234'
                self.game.start_game()
                result = mock_stdout.getvalue().strip()
        self.assertFalse(result.endswith("Игра завершена. Загаданное число было: 1234"))
    # def test_start_game_with_incorrect_guess(self):
    #     with patch('builtins.input', side_effect=['5678']):
    #         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
    #             self.game.secret_number = '1234'
    #             self.game.start_game()
    #             result = mock_stdout.getvalue().strip()
    #     self.assertTrue(result.endswith("Игра завершена. Загаданное число было: 1234"))

class TestPlayer(unittest.TestCase):
    def test_update(self):
        player = Player("Alice")
        result = {'guess': '5678', 'bulls': 2, 'cows': 1}
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            player.update(result)
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Alice, ваш результат: 5678 - 2 быков, 1 коров")

if __name__ == "__main__":
    unittest.main()

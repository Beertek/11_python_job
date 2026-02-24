import unittest
from unittest.mock import patch
import random
from loto_09 import LottoCard, Player, LottoGame

class TestLottoCard(unittest.TestCase):
    """Тесты для класса LottoCard"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.card = LottoCard("Тестовая карточка")
    
    def test_str_method(self):
        """Тест магического метода __str__"""
        str_representation = str(self.card)
        self.assertIsInstance(str_representation, str)
        self.assertIn("Тестовая карточка", str_representation)
    
    def test_len_method(self):
        """Тест магического метода __len__"""
        self.assertEqual(len(self.card), 15)
        
        # Отмечаем число
        numbers = []
        for row in self.card.rows:
            for num in row:
                if num is not None:
                    numbers.append(num)
        
        if numbers:
            self.card.check_number(numbers[0])
            self.assertEqual(len(self.card), 14)
    
    def test_contains_method(self):
        """Тест оператора in"""
        # Находим любое число на карточке
        number_to_check = None
        for row in self.card.rows:
            for num in row:
                if num is not None:
                    number_to_check = num
                    break
            if number_to_check:
                break
        
        if number_to_check:
            self.assertIn(number_to_check, self.card)
            
            # Отмечаем число
            self.card.check_number(number_to_check)
            # После отметки число не должно считаться доступным
            self.assertNotIn(number_to_check, self.card)
    
    def test_eq_method(self):
        """Тест сравнения карточек"""
        card1 = LottoCard("Карточка 1")
        card2 = LottoCard("Карточка 2")
        
        # Разные карточки должны быть разными
        self.assertNotEqual(card1, card2)
        
        # Копируем данные
        card2.rows = card1.rows.copy()
        card2.marked = card1.marked.copy()
        card2.numbers_left = card1.numbers_left
        
        # Теперь они должны быть равны
        self.assertEqual(card1, card2)
    
    def test_ne_method(self):
        """Тест неравенства карточек"""
        card1 = LottoCard("Карточка 1")
        card2 = LottoCard("Карточка 2")
        
        self.assertNotEqual(card1, card2)
        self.assertTrue(card1 != card2)


class TestPlayer(unittest.TestCase):
    """Тесты для класса Player"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.player1 = Player("Тестовый игрок", "human")
        self.player2 = Player("Компьютер", "computer")
    
    def test_str_method(self):
        """Тест магического метода __str__"""
        self.assertEqual(str(self.player1), "Тестовый игрок (human)")
        self.assertEqual(str(self.player2), "Компьютер (computer)")
    
    def test_eq_method(self):
        """Тест сравнения игроков"""
        player_copy = Player("Тестовый игрок", "human")
        self.assertEqual(self.player1, player_copy)
        self.assertNotEqual(self.player1, self.player2)
    
    def test_comparison_methods(self):
        """Тест методов сравнения"""
        self.player1.score = 10
        self.player2.score = 20
        
        self.assertLess(self.player1, self.player2)
        self.assertGreater(self.player2, self.player1)
    
    def test_win_rate(self):
        """Тест расчета процента побед"""
        self.assertEqual(self.player1.win_rate(), 0.0)
        
        self.player1.add_win()
        self.assertEqual(self.player1.win_rate(), 100.0)
        
        self.player1.add_loss()
        self.assertEqual(self.player1.win_rate(), 50.0)
    
    def test_add_win(self):
        """Тест добавления победы"""
        self.player1.add_win()
        self.assertEqual(self.player1.games_played, 1)
        self.assertEqual(self.player1.games_won, 1)
        self.assertEqual(self.player1.score, 10)
    
    def test_add_loss(self):
        """Тест добавления поражения"""
        self.player1.add_loss()
        self.assertEqual(self.player1.games_played, 1)
        self.assertEqual(self.player1.games_won, 0)
        self.assertEqual(self.player1.score, 0)


class TestLottoGame(unittest.TestCase):
    """Тесты для класса LottoGame"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.game = LottoGame(['human', 'computer'])
    
    def test_str_method(self):
        """Тест магического метода __str__"""
        str_representation = str(self.game)
        self.assertIsInstance(str_representation, str)
        self.assertIn("Игра в лото", str_representation)
    
    def test_len_method(self):
        """Тест магического метода __len__"""
        self.assertEqual(len(self.game), 90)
    
    def test_getitem_method(self):
        """Тест доступа по индексу"""
        player = self.game[0]
        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "Игрок 1")
    
    def test_iter_method(self):
        """Тест итерации по игрокам"""
        players = list(self.game)
        self.assertEqual(len(players), 2)
        self.assertIsInstance(players[0], Player)
    
    def test_contains_method(self):
        """Тест проверки наличия игрока"""
        player = self.game[0]
        self.assertIn(player, self.game)
        self.assertIn("Игрок 1", self.game)
        self.assertNotIn("Несуществующий игрок", self.game)
    
    @patch('builtins.input', return_value='n')
    def test_human_move_skip(self, mock_input):
        """Тест хода человека (пропуск)"""
        # Находим число, которого нет на карточке
        number = 100  # Заведомо не существующее
        self.game.current_barrel = number
        
        game_over, message = self.game.human_move(0)
        self.assertFalse(game_over)
        self.assertIn("пропустил ход", message)
    
    def test_computer_move(self):
        """Тест хода компьютера"""
        self.game.current_barrel = 1
        game_over, message = self.game.computer_move(1)
        
        # Компьютер может либо зачеркнуть, либо пропустить
        possible_messages = [
            "Компьютер 2 зачеркнул 1",
            "Компьютер 2 пропустил ход"
        ]
        self.assertIn(message, possible_messages)
    
    def test_get_next_barrel(self):
        """Тест получения следующего бочонка"""
        initial_len = len(self.game.barrels)
        barrel = self.game.get_next_barrel()
        
        self.assertIsNotNone(barrel)
        self.assertEqual(len(self.game.barrels), initial_len - 1)
    
    def test_get_statistics(self):
        """Тест получения статистики"""
        stats = self.game.get_statistics()
        self.assertIsInstance(stats, str)
        self.assertIn("СТАТИСТИКА ИГРОКОВ", stats)


class TestGameIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_game_initialization(self):
        """Тест инициализации игры"""
        game = LottoGame(['human', 'computer', 'computer'])
        
        self.assertEqual(len(game.players), 3)
        self.assertEqual(game.players[0].type, 'human')
        self.assertEqual(game.players[1].type, 'computer')
        self.assertEqual(game.players[2].type, 'computer')
        
        # Проверяем, что у всех есть карточки
        for player in game.players:
            self.assertIsNotNone(player.card)
            self.assertEqual(len(player.card), 15)
    
    @patch('builtins.input', return_value='n')
    def test_full_game_with_mocks(self, mock_input):
        """Тест полной игры с моками"""
        game = LottoGame(['human', 'computer'])
        
        # Эмулируем несколько ходов
        for _ in range(5):
            barrel = game.get_next_barrel()
            if barrel:
                game.play_turn(game.current_player_idx)
                game.current_player_idx = (game.current_player_idx + 1) % len(game.players)
        
        # Проверяем, что игра продолжается
        self.assertGreater(len(game.barrels), 0)


if __name__ == '__main__':
    unittest.main()
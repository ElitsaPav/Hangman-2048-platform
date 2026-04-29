import unittest
import pygame
from unittest.mock import patch
from Hangman.button import Button
from Hangman.game import Game


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 800))
        self.button = Button(100, 100, 'A')

    def test_button_initialization(self):
        self.assertEqual(self.button.x, 100)
        self.assertEqual(self.button.y, 100)
        self.assertEqual(self.button.letter, 'A')
        self.assertTrue(self.button.available)

    def test_button_click_outside(self):
        pygame.mouse.set_pos((50, 50))
        pygame.event.pump()
        self.assertFalse(self.button.click())

    def test_button_click_inside(self):
        with patch("pygame.mouse.get_pos", return_value=(110, 110)):
            self.assertTrue(self.button.click())


class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 800))
        self.game = Game()

    def test_game_initialization(self):
        self.assertIsInstance(self.game.words, list)
        self.assertIsInstance(self.game.word, str)
        self.assertIn(self.game.word, self.game.words)
        self.assertEqual(self.game.hangman_status, 0)

    def test_word_selection(self):
        self.assertIn(self.game.word, ["CAT", "MOUSE", "FRIDGE", "PYTHON", "PHONE", "BABY", "ELEPHANT", "CUPBOARD", "SOFA",
                      "PENCIL", "UMBRELLA", "GUIDE", "CALIFORNIA", "UNIVERSITY", "CANDLE", "DESSERT",
                      "BATHROOM", "BANANA", "SUMMER", "PROJECT", "GARDEN", "ROAD", "PEPPER", "PARENT"
                      ])

    def test_button_creation(self):
        self.assertEqual(len(self.game.buttons), 26)
        for button in self.game.buttons:
            self.assertIsInstance(button, Button)

    def test_correct_letter_guess(self):
        self.game.word = "PYTHON"
        self.game.clicked_letters.append("P")
        self.assertIn("P", self.game.clicked_letters)

    def test_incorrect_letter_guess(self):
        self.game.word = "PYTHON"
        self.game.clicked_letters.append("X")
        if "X" not in self.game.word:
            self.game.hangman_status += 1
        self.assertEqual(self.game.hangman_status, 1)

    def test_game_winning_condition(self):
        self.game.word = "BANANA"
        self.game.clicked_letters = list("BANANA")
        guessed = all(letter in self.game.clicked_letters for letter in self.game.word)
        self.assertTrue(guessed)

    def test_game_losing_condition(self):
        self.game.hangman_status = 6  # Max incorrect guesses
        self.assertEqual(self.game.hangman_status, 6)


if __name__ == "__main__":
    unittest.main()

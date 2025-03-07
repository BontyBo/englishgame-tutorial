from django.test import TestCase
from .views import processWordDisplay, getRandomWord

class ProcessWordDisplayTests(TestCase):

    def test_all_characters_guessed(self):
        # Complete Game Condition
        word = "hello"
        guessedChar = "helo"
        result = processWordDisplay(word, guessedChar)
        self.assertEqual(result, "h e l l o")
    
    def test_no_characters_guessed(self):
        # Initial Condition ควร return ช่องว่างเท่าตัวอักษร
        word = "hello"
        guessedChar = ""
        result = processWordDisplay(word, guessedChar)
        self.assertEqual(result, "_ _ _ _ _")
    
    def test_some_characters_guessed(self):
        # ถ้าใส่คำไม่ครบ ควรแสดงแค่ตัวอักษรที่ใส่
        word = "hello"
        guessedChar = "he"
        result = processWordDisplay(word, guessedChar)
        self.assertEqual(result, "h e _ _ _")
    
    def test_edge_case_empty_word(self):
        # ถ้าคำว่างเปล่าควรไม่มีเลย
        word = ""
        guessedChar = "a"
        result = processWordDisplay(word, guessedChar)
        self.assertEqual(result, "")
    
    def test_case_sensitivity_upper_word(self):
        # Case to test if the function is case-sensitive
        word = "Hello"
        guessedChar = "h"
        result = processWordDisplay(word, guessedChar)
        self.assertEqual(result, "h _ _ _ _")

    def test_case_sensitivity_upper_guessed(self):
        # Case to test if the function is case-sensitive
        word = "hello"
        guessedChar = "H"
        result = processWordDisplay(word, guessedChar)
        self.assertEqual(result, "h _ _ _ _")

    def test_input_wrong_word_type(self):
        word = 123
        guessedChar = "1"
        with self.assertRaises(TypeError) as context:
            processWordDisplay(word, guessedChar)
        self.assertEqual(str(context.exception), "word type is not string")
    
    def test_input_wrong_guessed_type(self):
        word = "123"
        guessedChar = 1
        with self.assertRaises(TypeError) as context:
            processWordDisplay(word, guessedChar)
        self.assertEqual(str(context.exception), "guessed character type is not string")
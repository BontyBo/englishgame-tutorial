from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from hangman.models import wordBank 
class HangmanGameTest(StaticLiveServerTestCase):
    def setUp(self):
      #ปาร์คเปิด Google Chrome ขึันมา
       self.driver = webdriver.Chrome()
       self.driver.implicitly_wait(10)
       wordBank.objects.create(word="bed")


       # สร้าง server จำลอง
       self.driver.get(self.live_server_url)
    def tearDown(self):
       self.driver.quit()

    def test_setup_game(self):
        self.driver.get(self.live_server_url + "/hangman")
        #ปาร์คเห็นว่าใน url มีคำว่า hangman
      
        self.assertIn("/hangman", self.driver.current_url) 
        # ปาร์คเห็นข้อความ "Welcome to Hangman" บนหน้าเว็บ 
        self.assertIn("Welcome to Hangman", self.driver.page_source)

    def test_hangman_game_uses_correct_template(self):
        response = self.client.get(reverse("hangman:index"))  
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, "hangman/game.html")  
   
    def test_initial_game_state(self):
        """ ทดสอบว่าเมื่อเริ่มเกมต้องเห็นช่องว่าง 3 ช่อง """
        # ปาร์คเห็นช่องว่าง 3 ช่อง
        self.driver.get(self.live_server_url + "/hangman")
        word_display = self.driver.find_element(By.ID, "word-display").text
        self.assertEqual(word_display, "_ _ _")  # ต้องมีช่องว่าง 3 ช่อง

    def test_guess_wrong_letter(self):
        """ ทดสอบว่าเมื่อใส่ตัวอักษรผิด จำนวน attempt ต้องลดลง """
        self.driver.get(self.live_server_url + "/hangman")
        input_box = self.driver.find_element(By.ID, "guess-input")
        submit_button = self.driver.find_element(By.ID, "submit-guess")

        # ปาร์คใส่ตัวอักษรผิด เช่น 'x'
        input_box.send_keys("x")
        submit_button.click()

        # ปาร์คเห็นข้อความแจ้งเตือนว่า Incorrect guess!
        alert = self.driver.find_element(By.ID, "message").text
        print(f"DEBUG: Retrieved message: '{alert}'") 
        self.assertIn("Incorrect guess!", alert)

        # ปาร์คเห็นจำนวน attempts ลดลงเหลือ 2
        attempts_left = self.driver.find_element(By.ID, "attempts-left").text
        self.assertEqual(attempts_left, '2')

        guess_letter = self.driver.find_element(By.ID,"guessed-letters").text
        self.assertIn("x",guess_letter)

    def test_guess_correct_letters(self):
        self.driver.get(self.live_server_url + "/hangman")
        """ ทดสอบว่าเมื่อใส่ตัวอักษรถูกทั้งหมดจะชนะเกม """

        # ปาร์คเดาตัว 'b'
        input_box = self.driver.find_element(By.ID, "guess-input")
        submit_button = self.driver.find_element(By.ID, "submit-guess")
        input_box.send_keys("b")
        submit_button.click()

        # ปาร์คเดาตัว 'e'
        input_box = self.driver.find_element(By.ID, "guess-input")
        submit_button = self.driver.find_element(By.ID, "submit-guess")
        input_box.send_keys("e")
        submit_button.click()

        # ปาร์คเดาตัว 'd'
        input_box = self.driver.find_element(By.ID, "guess-input")
        submit_button = self.driver.find_element(By.ID, "submit-guess")
        input_box.send_keys("d")
        submit_button.click()

        # ตรวจสอบว่าแสดงคำเต็ม "bed"
        word_display = self.driver.find_element(By.ID, "word-display").text
        self.assertEqual(word_display, "b e d")

        # ปาร์คเห็นข้อความ Congratulations! You won!
        message = self.driver.find_element(By.ID, "message").text
        self.assertIn("Congratulations! You won!", message)

    def test_lose_game(self):
        self.driver.get(self.live_server_url + "/hangman")
        """ ทดสอบว่าเดาผิด 3 ครั้งแล้วต้องแพ้ """

        # ปาร์คเดาผิด 3 ครั้ง โดยใส่ตัวอักษร x , y , z 
        for letter in ["x", "y", "z"]:
            input_box = self.driver.find_element(By.ID, "guess-input")
            submit_button = self.driver.find_element(By.ID, "submit-guess")
            input_box.send_keys(letter)
            submit_button.click()

        # ปาร์คเห็นข้อความ Game Over! The word was: bed
        message = self.driver.find_element(By.ID, "message").text
        self.assertIn("Game Over! The word was: bed", message)
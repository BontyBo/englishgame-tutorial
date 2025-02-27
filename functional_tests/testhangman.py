from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class HangmanGameTest(StaticLiveServerTestCase):
   def setUp(self):
      #ปาร์คเปิด Google Chrome ขึันมา
       self.driver = webdriver.Chrome()
       self.driver.implicitly_wait(10)

       # สร้าง server จำลอง
       self.driver.get(self.live_server_url)
   def tearDown(self):
       self.driver.quit()

   def test_hangman_game(self):
      #ปาร์คเห็นว่าใน url มีคำว่า hangman
       self.assertIn("/hangman", self.driver.current_url) 
        # ปาร์คเห็นข้อความ "Welcome to Hangman" บนหน้าเว็บ 
       self.assertIn("Welcome to Hangman", self.driver.page_source)

import time

from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from secret_key import EMA_PASSWORD

# ads argument to ignore certificate
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')

# ads argument to ignore insecure localhost to Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--allow-insecure-localhost')

USER = get_user_model()


class GuiTestSelenium(TestCase):
    def test_reviews_page_chrome(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8002')
        assert 'Welcome to Personal Portal application' in selenium_webdriver.page_source
        time.sleep(10)

    def test_login(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8002/accounts/login/')

        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('GuiTestUser')
        time.sleep(3)
        password_field = selenium_webdriver.find_element(By.ID, 'id_password')
        password_field.send_keys('Nereknu155')
        time.sleep(3)

        # find the Cancel button and click on it
        cancel_button = selenium_webdriver.find_element(By.CLASS_NAME, 'btn-primary')
        cancel_button.click()

        # wait for the page to load
        WebDriverWait(selenium_webdriver, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'guestDropdown'))
        )
        # assert the expected text is in the new page source
        self.assertIn('You are not logged in', selenium_webdriver.page_source,
                      'The text was not found on the next page')

    def test_submit_review(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8002/accounts/login/')

        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('ema.drobna@firma.cz')
        time.sleep(3)

        password_field = selenium_webdriver.find_element(By.ID, 'id_password')
        password_field.send_keys(f"{EMA_PASSWORD}")
        time.sleep(3)

        submit_button = selenium_webdriver.find_element(By.CLASS_NAME, 'btn-success')
        submit_button.click()

        # wait for the page to load
        WebDriverWait(selenium_webdriver, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'reviewsLink'))
        )

        reviews_button = selenium_webdriver.find_element(By.XPATH, '//*[@id="reviewsLink"]')
        reviews_button.click()

        create_review_button = selenium_webdriver.find_element(By.ID, 'createReviewButton')
        create_review_button.click()

        goal_field = selenium_webdriver.find_element(By.ID, 'id_goal')
        goal_field.send_keys('Ema Drobná - Be more proactive')
        time.sleep(2)

        description_field = selenium_webdriver.find_element(By.ID, 'id_description')
        description_field.send_keys('Test review describes accomplishment of my goal')
        time.sleep(2)

        training_field = selenium_webdriver.find_element(By.ID, 'id_training')
        training_field.send_keys('Undergo this training to accomplish your goal')
        time.sleep(2)

        submit_button = selenium_webdriver.find_element(By.CLASS_NAME, 'btn-success')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(2)

        # assert the expected text is in the new page source
        self.assertIn('My Reviews Summary', selenium_webdriver.page_source,
                      'The text was not found on the next page')

    def test_submit_review_invalid_user(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8002/accounts/login/')

        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('admin')
        time.sleep(3)

        password_field = selenium_webdriver.find_element(By.ID, 'id_password')
        password_field.send_keys('admin-pass')
        time.sleep(3)

        submit_button = selenium_webdriver.find_element(By.CLASS_NAME, 'btn-success')
        submit_button.click()
        time.sleep(10)

        self.assertIn('Please enter a correct username and password.', selenium_webdriver.page_source,
                      'The text was not found on the next page')


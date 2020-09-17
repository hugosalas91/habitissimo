from django.test import SimpleTestCase
from django.urls import reverse, resolve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from front_app.views import home
from time import sleep


class HomepageTests(FunctionalTest):
    
    def test_homepage_status_code(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)
        
    def test_homepage_template(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.assertTemplateUsed(self.response, 'front_app/home.html')
        
    def test_homepage_contains_correct_html(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.assertContains(self.response, 'Bienvenido a Habitissimo')
        
    def test_homepage_does_not_contain_incorrect_html(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.assertNotContains(self.response, 'Hola mundo')
        
    def test_homepage_url_resolves_homepageview(self):
        url = reverse('home')
        self.response = self.client.get(url)
        view = resolve('/')
        self.assertEqual(
            view.func.__name__, 
            home.__name__
        )
    
    def test_can_search_a_service(self):
        # Hugo wants to visit Habitissimo Challenge webpage
        self.browser.get(self.live_server_url)

        # He notices the page title mention home
        self.assertIn('Home', self.browser.title)
        
        # He notices the page welcomes you
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Bienvenido a Habitissimo', header_text)
        
        # He is invited to search a service for his home
        inputbox = self.browser.find_element_by_id('search')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Qué necesitas...'
        )
        
        # He types "Pint" into a text box (Hugo is searching paint the exterior of his premises)
        inputbox.send_keys('Pint')
        sleep(5)
        
        # He see an autocomplete list and select "Pintar Exterior Local"
        click = self.browser.find_elements_by_xpath("//*[contains(text(), 'Pintar Exterior Local')]")[0].click()
        
        # He clicks search button
        search_button = self.browser.find_element_by_id('search-button')
        click = search_button.find_element_with_tag_name('input').click()
        sleep(10)
        
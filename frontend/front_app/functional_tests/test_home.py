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

        """"
        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        self.add_list_item('Use peacock feathers to make a fly')

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfied, she goes back to sleep
        """

    """
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        self.add_list_item('Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
    """
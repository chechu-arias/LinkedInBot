from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from time import sleep
from secret import email, password

import sys


class LinkedInBot():
    
    def __init__(self, entity, outputfile):

        self.driver = webdriver.Chrome()
        self.entityname = entity
        self.resultfile = outputfile

    def input_data(self):

        email_input = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_input.send_keys(email)

        password_input = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_input.send_keys(password)

        # Clicks the init session
        init_session_button = self.driver.find_element_by_xpath('//*[@id="app__container"]/main/div[3]/form/div[3]/button')
        init_session_button.click()


    def scroll_down_page(self):

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(0.5)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height





    def login(self):
        
        self.driver.get('https://es.linkedin.com/')

        sleep(1)

        #Click the login LinkedIn
        login_button = self.driver.find_element('xpath','/html/body/nav/div/a') #/html/body/nav/div/a
        login_button.click()

        # Waits for load of page
        sleep(1)

        # Inputs the email and password
        try:
            
            self.input_data()

        except NoSuchElementException:
            
            login_button = self.driver.find_element_by_xpath('/html/body/div[2]/main/p/a')
            login_button.click()

            self.input_data()
        

        # Skips the phone check
        try:
            skip_phone = self.driver.find_element_by_xpath('//*[@id="ember983"]/button')
            skip_phone.click()
        except NoSuchElementException:
            pass


    def search_entity(self):

        search_input = self.driver.find_element_by_xpath('/html/body/div[8]/header/div[2]/div/div/div[1]/div/input')
        search_input.send_keys(self.entityname)
        search_input.send_keys(Keys.ENTER)

        sleep(5)

        result_list_container = self.driver.find_element_by_class_name('search-results-container')

        result_list_elements = result_list_container.find_elements_by_tag_name("li")
        
        first_result_button_elements = result_list_elements[0].find_elements_by_tag_name("h3")

        first_result_button = first_result_button_elements[0]

        first_result_button.click()

        sleep(3)


    def obtain_info(self):

        self.driver.get(self.driver.current_url + "people/")

        self.scroll_down_page()
        sleep(2)

        all_people_container = self.driver.find_elements_by_class_name("org-people-profiles-module__profile-list")

        all_people_list = all_people_container[0].find_elements_by_tag_name("li")
        
        employees = []
        for person in all_people_list:
            
            all_fields_in_a_person = person.find_elements_by_tag_name("div")

            elems = all_fields_in_a_person[0].text.split("\n")
            name = elems[0]

            try:
                job = elems[1]
            except IndexError:
                job = ""

            if len(name) and name != "Miembro de LinkedIn":
                res = name + " : " + job
                employees.append(res)
            else:
                continue

        with open(self.resultfile, "w") as outfile:
            outfile.write("\n".join(employees))



if __name__ == "__main__":

    if len(sys.argv) == 3:

        entity = sys.argv[1]
        outputfile = sys.argv[2]

        bot = LinkedInBot(entity, outputfile)
        bot.login()
        bot.search_entity()
        bot.obtain_info()

    else:

        print("Wrong usage: 2 parameters were expected, but only {} were given.".format(len(sys.argv)))
        print("Usage python3 LinkedInBot.py name_of_the_enterprise output_filename")

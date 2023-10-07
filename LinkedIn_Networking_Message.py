from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime
import requests
import json
import random
import xlrd
import os
import openai
import time


# define wait

def wait(times):
    start_time = time.time()
    while True:
        end_time = time.time()
        if end_time - start_time > times:
            break


# Initialize OpenAI

openai.api_key = "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"

def call_openai_api(instruction, prompt):
    model = "gpt-3.5-turbo"
    # model = "gpt-4"
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response

def linkedin_login(webdriver, username, password):
    # Initialize url and class name
    class_login = "form__input--floating"
    ID_input_username = "username"
    ID_input_password = "password"
    class_login_button = "login__form_action_container"
    url_LinkedIn = "https://www.linkedin.com/login"

    # Log In
    webdriver.get(url_LinkedIn)
    login_elements = webdriver.find_elements(By.CLASS_NAME,class_login)
    username_key = login_elements[0].find_element(By.ID, ID_input_username)
    password_key = login_elements[1].find_element(By.ID, ID_input_password)
    username_key.send_keys(username)
    password_key.send_keys(password)
    login_button = webdriver.find_element(By.CLASS_NAME,class_login_button)
    login_button.click()

    # for verification purpose, fuck linkedin
    wait(15)

def networking_message(search_string, number_of_connection,
                       username, password, resume):

    '''
        search_string: the tag that you want your connections to have. e.g. goldman saches
        number_of_connection: number of people you want to message with
        username: your LinkedIn username
        password: your LinkedIn password
        resume: your resume as a string
    '''

    # Initialize url and class name
    class_next_page_button = "artdeco-pagination__button"
    class_search_box = "search-global-typeahead__input"
    class_filter_box = "search-reusables__primary-filter"
    class_filter_botton = "artdeco-pill"
    class_search_card_container = "reusable-search__result-container"
    class_search_card_link = "app-aware-link"
    class_people_about_text = "inline-show-more-text"
    class_people_experience_list = "artdeco-card"
    class_people_experience_box = "pvs-entity"
    class_people_name = "text-heading-xlarge"
    class_connect_button = "artdeco-button"
    class_connect_button_text = "artdeco-button__text"
    class_message_box_popup = "msg-overlay-container"
    class_message_box = "msg-form__contenteditable"
    class_send_button = "msg-form__send-button"

    # Initialize driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    wd = webdriver.Chrome(options=options)
    
    # Log In
    linkedin_login(wd, username, password)

    # Search
    search_box = wd.find_element(By.CLASS_NAME,class_search_box)
    search_box.send_keys(search_string)
    search_box.send_keys(Keys.ENTER)
    wait(3)

    # Filter people category
    head_filters = wd.find_elements(By.CLASS_NAME,class_filter_box)
    people_button = head_filters[0].find_element(By.CLASS_NAME,class_filter_botton)
    people_button.click()
    wait(3)

    # Scrape All People
    search_results = wd.find_elements(By.CLASS_NAME,class_search_card_container)
    while len(search_results) < number_of_connection * 2:
        # times 2 because some profile cannot be messaged
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait(2)
        next_page = wd.find_elements(By.CLASS_NAME,class_next_page_button)
        next_page[1].click()
        wait(2)
        search_results += wd.find_elements(By.CLASS_NAME,class_search_card_container)

    people_link_list = []

    # Obtain link to the profile of all people
    for searched_people in search_results:
        try:
            people_link = searched_people.find_elements(By.CLASS_NAME,class_search_card_link)
            people_link_list.append(people_link[1].get_attribute('href'))
        except:
            pass

    # Obtain detailed information for all people
    total_cost = 0
    for link in people_link_list:
        wd.get(link)
        wait(2)
        people_name = wd.find_element(By.CLASS_NAME,class_people_name).text
        people_experiences_list = wd.find_elements(By.CLASS_NAME,class_people_experience_list)
        people_experiences = people_experiences_list[3].find_elements(By.CLASS_NAME,class_people_experience_box)
        people_experiences = people_experiences + people_experiences_list[4].find_elements(By.CLASS_NAME,class_people_experience_box)
        people_experiences = people_experiences + people_experiences_list[5].find_elements(By.CLASS_NAME,class_people_experience_box)

        for i in range(len(people_experiences)):
            experience_text = people_experiences[i].text
            lines = experience_text.splitlines()
            people_experiences[i] = lines[1::2]

        people_experiences_concatenated_string = '\n'.join([string for sublist in people_experiences for string in sublist])
        
        # send message to each person
        send_message = wd.find_elements(By.CLASS_NAME, class_connect_button)

        index = 0
        for button in send_message[5:len(send_message)]:
            # first button is turn on notification, which you won't want

            # in case we find a "connect" button
            try:
                button.click()
                wait(1)
                chatbox = wd.find_element(By.CSS_SELECTOR, '[aria-label="Add a note"]')
                chatbox.click()
                print("messaging: " + people_name)
                break
            except Exception as e:
                pass
            
            # in case this person's "connect" button does not exist
            try:
                button.click()
                wait(1)
                chatbox_present = wd.find_elements(By.CLASS_NAME, class_message_box_popup)
                chatbox = chatbox_present[0].find_elements(By.CLASS_NAME, class_message_box)[0]
                chatbox.click()
                chatbox.send_keys(Keys.CONTROL + "a")  # This will select all the content
                chatbox.send_keys(Keys.DELETE)
                print("")
                print("messaging: " + people_name)
                break
            except Exception as e:
                pass
        
        #wd.send_keys(response_text)

        # Create networking message for one person    
        instruction = f''' now you should behave like the most advanced AI in generating networking cold message.
                        You should generate professional, respectful, and warm massage for a college students
                        to those he/she want to establish connection and have coffee chat / zoom chat with.
                        You should behave as a student described in the following resume. You should
                        introduce yourself very briefly and conciselu about your passion and capability,
                        you should also explain, and emphasize with passion, about what particular
                        experience of the person whom you reach out makes you interested.
                        DO NOT include subject line.
                        Here is your resume: {resume}'''

        prompt = f''' the person you connect with is: {people_name},
                    and here's his/her information on LinkedIn: {people_experiences_concatenated_string}'''
        try:
            response = call_openai_api(instruction, prompt)
            response_text = response['choices'][0]['message']['content']
            cost = response['usage']['prompt_tokens'] * 0.0015 * 0.001 + response['usage']['prompt_tokens'] * 0.002 * 0.001
            total_cost = total_cost + cost
            try:
                chatbox.click()
                chatbox.send_keys(response_text)
            except:
                chatbox = wd.find_element(By.ID, "custom-message")
                chatbox.click()
                chatbox.send_keys(response_text)
            try:
                send = wd.find_element(By.CLASS_NAME, class_send_button)
            except:
                send = wd.find_element(By.CSS_SELECTOR, '[aria-label="Send now"]')

            wait(1)
            send.click()
            print("Successfully messaged: " + people_name)
        except Exception as e:
            print(e)
            print("Failed messaging: " + people_name)
            pass

        wait(2)

    # end
    wd.quit()

    print("You cost one of the developer, David He, " + str(total_cost) + " on openAI!")
    print("Good job!")

################################# Just for testing purpose #######################################################



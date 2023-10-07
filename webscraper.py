from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime
import re
import os

def waiting(times):
    """
    Function to wait for a specified amount of time.
    """
    start_time = time.time()
    while True:
        end_time = time.time()
        if end_time - start_time > times:
            break

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
    waiting(15)
    
def webscrape_linkedin(job_name, username, password):
    """
    Webscrapes LinkedIn for job data.
    """

    # Define constants
    url_LinkedIn = "https://www.linkedin.com/jobs/search?keywords=&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_E=1&position=1&pageNum=0"
    class_search_bar = "dismissable-input__input"
    class_each_job_card = "base-card"
    class_each_job_card_link = "base-card__full-link"
    class_all_job_card = 'jobs-search__results-list'
    class_job_description = 'description__text'
    class_more_job_button = 'infinite-scroller__show-more-button'
    class_num_applicants = 'num-applicants__caption'
    class_category_job = "description__job-criteria-item"

    # Initialize driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    wd = webdriver.Chrome(options=options)
    
    # Open LinkedIn page and search desired position
    # Default tags: Internship, United States
    wd.get(url_LinkedIn)
    waiting(2)
    search_bar = wd.find_elements(By.CLASS_NAME,class_search_bar)
    search_bar[2].click()
    search_bar[2].send_keys(job_name)
    search_bar[2].send_keys(Keys.ENTER)
    waiting(2)

    # select internship, internship is at index 15
    filter_button = wd.find_elements(By.CLASS_NAME,"filter-button")[5]
    filter_button.click()
    waiting(1)
    intern_buttons = wd.find_elements(By.CSS_SELECTOR, '[type="checkbox"]')
    intern_buttons[15].click()
    waiting(1)
    intern_buttons[15].send_keys(Keys.ENTER)
    waiting(1)
    # sometime it works, sometime it doesn't


    # Fetch and parse the LinkedIn URL
    each_job_elements = wd.find_elements(By.CLASS_NAME,class_each_job_card)
    all_jobs_num = wd.find_element(By.CLASS_NAME,'results-context-header__job-count')
    new_jobs_num = wd.find_element(By.CLASS_NAME,'results-context-header__new-jobs')


    # get ALL jobs
    while True:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        waiting(2)
        wd.execute_script("window.scrollBy(0, -200);")
        waiting(2)
        wd.execute_script("window.scrollBy(0, 500);")
        waiting(3)
        
        new_items = wd.find_elements(By.CLASS_NAME, class_each_job_card)
        waiting(2)
        try:
            load_more = wd.find_element(By.CLASS_NAME, class_more_job_button)
            load_more.click()
            waiting(2)
        except:
            pass
        if len(new_items) == len(each_job_elements):
            break
        each_job_elements = new_items

    # initialize the data storage

    result = pd.DataFrame(columns=["Company","Position Name", \
                               "Location","Status", \
                               "Job Description", "Application Link",\
                                   "Number of Applicants", "Industry",\
                                   "Salary"])
    job_link_list = []

    # get titles and positions, and links to detail page
    index = 0
    for element in each_job_elements:
        try:
            result.at[index, result.columns[0]] = element.text.split('\n')[2]
            result.at[index, result.columns[1]] = element.text.split('\n')[1]
            result.at[index, result.columns[2]] = element.text.split('\n')[3]
            result.at[index, result.columns[3]] = element.text.split('\n')[4]
            link = element.find_element(By.CLASS_NAME, class_each_job_card_link)
            link_url = link.get_attribute('href')
            job_link_list.append(link_url)
            result.at[index, result.columns[5]] = link_url
            index = index + 1
        except:
            pass

    # get job description by looking into detail page
    index = 0
    for url in job_link_list:
        wd.get(url)
        waiting(1.5)
        # get job description
        try:
            jd = wd.find_element(By.CLASS_NAME,class_job_description)
            result.at[index, result.columns[4]] = jd.text
        except:
            result.at[index, result.columns[4]] = "INVALID LINK"

        # get number of applicants
        try:
            num_applicants = wd.find_element(By.CLASS_NAME,class_num_applicants)
            pattern = r'\d+'
            result.at[index, result.columns[6]] = int(re.search(pattern, num_applicants.text).group())
        except:
            result.at[index, result.columns[6]] = ""

        # get job's industry
        try:
            job_categories = wd.find_elements(By.CLASS_NAME,class_category_job)
            result.at[index, result.columns[7]] = job_categories[3].text
        except:
            result.at[index, result.columns[7]] = ""

        # get job's industry, not very accurate
        try:
            pattern = r'\$([\d,]+)'
            salary = re.findall(pattern, jd.text)[0]
            salary.replace("," , "")
            salary = int(salary)
            if salary > 300:
                salary = salary // 2000
            result.at[index, result.columns[8]] = salary
        except:
            result.at[index, result.columns[8]] = 0

        index = index + 1

    # Close the webdriver and return the result
    wd.quit()

    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H-%M-%S')
    file_name = f"LinkedIn_Scrapted_{job_name}.csv"

    # Save the scraped data to CSV
    save_scraped_data_to_csv(result, file_name)

    return result


def save_scraped_data_to_csv(df, filename="scraped_data.csv"):
    df.to_csv(filename, index=True, index_label='Row Number')

def load_data_from_csv(filename="scraped_data.csv"):
    return pd.read_csv(filename)

def get_job_data(job_name, linkedin_account, linkedin_password):
    filename = f"LinkedIn_Scrapted_{job_name}.csv"

    # Check if CSV file exists
    if os.path.exists(filename):
        print("Loading data from CSV...")
        return pd.read_csv(filename)
    else:
        print("")
        print("Scraping LinkedIn for job data...")
        print("Depending on job you search, this takes up to 40 minutes...")
        return webscrape_linkedin(job_name, linkedin_account, linkedin_password)



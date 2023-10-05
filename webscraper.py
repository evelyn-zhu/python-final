import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def webscrape_linkedin():
    """
    Webscrapes LinkedIn for job data.
    """

    # Define constants
    url_LinkedIn = "https://www.linkedin.com/jobs/search?keywords=Data\%20Scientist&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_E=1&position=1&pageNum=0"
    class_each_job_card = "base-card"
    class_each_job_card_link = "base-card__full-link"
    class_job_description = 'description__text'

    # Initialize the webdriver
    wd = webdriver.Chrome()

    # Fetch and parse the LinkedIn URL
    wd.get(url_LinkedIn)
    each_job_elements = wd.find_elements(By.CLASS_NAME, class_each_job_card)

    # Scroll until 5 job listings are obtained
    while len(each_job_elements) < 1:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        waiting(2)
        new_items = wd.find_elements(By.CLASS_NAME, class_each_job_card)
        waiting(2)
        if len(new_items) == len(each_job_elements):
            break
        each_job_elements = new_items

    # Store the results
    index = 0
    result = pd.DataFrame(
        columns=["Basic Info", "Title", "Company", "Position Name", "Application Link", "Job Description"])
    job_link_list = []

    # Extract job details
    for element in each_job_elements:
        # Extract and clean the title
        basic_info = element.text.split("\n")
        title = basic_info[0]
        company = basic_info[2] if len(
            basic_info) > 2 else ''  # Assume company is on the third line, handle cases where it might not be

        result.at[index, "Basic Info"] = element.text
        result.at[index, "Title"] = title
        result.at[index, "Company"] = company

        link = element.find_element(By.CLASS_NAME, class_each_job_card_link)
        link_url = link.get_attribute('href')
        job_link_list.append(link_url)
        result.at[index, "Application Link"] = link_url
        result.at[index, "Position Name"] = link.text

        index += 1

    # Extract job descriptions
    for i, url in enumerate(job_link_list):
        wd.get(url)
        waiting(3)
        try:
            jd = wd.find_element(By.CLASS_NAME, class_job_description)
            result.at[i, "Job Description"] = jd.text
        except:
            result.at[i, "Job Description"] = "INVALID LINK"

    # Close the webdriver and return the result
    wd.quit()

    # Save the scraped data to CSV
    save_scraped_data_to_csv(result)

    return result


def save_scraped_data_to_csv(df, filename="scraped_data.csv"):
    df.to_csv(filename, index=True, index_label='Row Number')

def load_data_from_csv(filename="scraped_data.csv"):
    return pd.read_csv(filename)

def get_job_data():
    filename = "scraped_data.csv"

    # Check if CSV file exists
    if os.path.exists(filename):
        print("Loading data from CSV...")
        return pd.read_csv(filename)
    else:
        print("Scraping LinkedIn for job data...")
        return webscrape_linkedin()


# Advanced LinkedIn Job Analytics & Networking with OpenAI GPT-4

Harnessing the advanced capabilities of modern Natural Language Processing (NLP) and robust web scraping techniques, this project is a cutting-edge solution for job seekers and professionals alike. It integrates intricate data extraction from LinkedIn, subsequent high-fidelity processing, and intelligent content generation using OpenAI's GPT-4, all culminating in a powerful platform that redefines job analytics and networking.

## Core Functionalities

### webscraper.py
**High-Resolution Web Scraper**:
- **Data Extraction**: Dives deep into LinkedIn's data-rich environments, capturing nuanced job details, company profiles, and industry trends based on specified criteria.
- **Data Storage**: Organizes the scraped data into structured datasets, making it ready for further processing and analysis.
- **Analysis**: Profiles job markets, highlighting emerging trends, desired skills, and potential growth areas.

### job_openings.py
**Time Series Analysis & Prediction Functions**:
- **Data Extraction**: Reads an Excel file with data using the provided filename. Converts the 'Time' column to a datetime format using the '%YM%m' structure.
- **Data Processing**: Calculates a 12-month moving average of the 'value' column in the dataframe. Utilizes a rolling mean and standard deviation approach to detect anomalies in a time series. Calculates and displays the difference between consecutive forecasted values to identify growth or decline.
- **Analysis**: Identifies the optimal ARIMA model parameters (p, d, q) by iterating through potential combinations and comparing the Akaike Information Criterion (AIC). Uses the previously determined best ARIMA model parameters to forecast future job openings.

### graph_jobs.py
**Professional Analytics for Job Industries**:
- **Data Preparation**: Drops missing data entries and cleans the 'Industry' field by truncating the string. Aggregates and summarizes applicant and job opening data by industry.
- **Data Analysis**: 1, Showcases industries with a significant number of applicants. 2, Highlights industries with the most job openings. 3, Computes the ratio of applicants to job openings and identifies industries that offer the best chances of employment with minimal competition.

### similarity.py
**Deep Skill Matching Algorithm**:
- **Data Extraction**: Scours LinkedIn job listings, extracting required skills and qualifications with impeccable accuracy.
- **Data Processing**: Processes the extracted skills, categorizing them into core competencies and desirable traits.
- **Analysis**: Deploys cosine similarity algorithms on processed data to identify the alignment between user skills and job requirements, ensuring accurate recommendations.
- **Outcome**: Users receive feedback on how their skillset aligns with potential job opportunities, elevating their application potential.

### skills.py
**Dynamic Skill Extraction Engine**:
- **Data Extraction**: With the help of NLP, this module meticulously extracts skills and endorsements from LinkedIn profiles.
- **Data Processing**: Categorizes and ranks extracted skills based on relevance and endorsements, ensuring that the most vital skills stand out.
- **Analysis**: Compares user's skill repertoire against industry benchmarks, identifying areas of strength and potential improvement.

### cover_letter_1.py & cover_letter_2.py
**Precise Cover Letter Architect**:
- **Data Extraction**: Gathers specific job details like role, company values, and required qualifications.
- **Content Generation**: Utilizing GPT-4's unparalleled NLP capabilities, these modules craft bespoke cover letters that not only resonate with the job description but also emphasize the user's unique value proposition.
- **Outcome**: Personalized cover letters that enhance user's application visibility among a sea of generic applications.

### linkedin_messaging.py
**Advanced LinkedIn Interaction Enhancer**:
- **Data Extraction**: Retrieves connection profiles and past interaction history.
- **Content Generation**: With GPT-4 at its core, this tool drafts context-aware, personalized messages tailored to each connection, ensuring meaningful interactions.
- **Outcome**: Efficiently networks on LinkedIn, nurturing connections and fostering potential job leads.

### linkedin_easyapply.py
**Premium Job Application Accelerator**:
- **Data Extraction**: Gathers up-to-date URLs of job listings tailored to the user's preferences, ensuring the most relevant opportunities are considered.
- **Content Generation**: Populate LinkedIn's "Easy Apply" forms, ensuring accurate and context-aware information submission.
- **Outcome**: Streamlines the process of job hunting by automating applications to several listings, saving time and effort.

### main.py
**Unified Interface & Integration Core**:
- **Data Flow Management**: Orchestrates the seamless flow of data across all modules, from extraction to final output.
- **User Interface**: Provides an intuitive interface, allowing users to easily navigate and utilize the platform's vast functionalities.

## Prerequisites

1. Python 3.x
2. Google Chrome Browser and the corresponding [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/).
3. Essential Python libraries: `selenium`, `pandas`, `Numpy`, `openai`, `xlrd`, `requests`, `datetime`, `time`, `json`, `random`, `xlrd`, `os`, `doc`, `re`, `sys`, `docx`, `docx2pdf`, `matploylib`, `warnings`, `math`, `webdriver_manager`, `packaging`, `pymogo`, `transformers`, `torch`, `skillNer`, `typing`, `gensim`, `sklearn`, `spacy`, `en_core_web_lg` (download from spacy).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LinkedIn_Job_Analytics_Networking.git
2. Enter the directory:
   ```bash
   cd LinkedIn_Job_Analytics_Networking
3. Set up the environment:
   ```bash
   pip install -r requirements.txt
4. Ensure the right version of ChromeDriver is available and located in the directory.

## Usage Guidelines

1. Update LinkedIn credentials and necessary details in the scripts.
2. Launch the main interface:
   ```bash
   python main.py

## Important Notes

- This sophisticated tool might operate against LinkedIn's terms. Exercise caution and use responsibly.
- Ensure compatibility between ChromeDriver and your Chrome browser version.
- We recommend initial tests in a controlled setting before extensive deployment.

## Liscense
MIT

## Clarification
This project is intended for educational and research purposes. The developers disclaim responsibility for any misuse or potential violations of terms of service.

## Contributors:
Chris Wang, David He, Evelyn Zhu, Kathy Wang, Rui Xi

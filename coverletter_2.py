import requests
import json
import random
import numpy as np
import xlrd
import os
import openai
import time
from docx import Document
from webscraper import get_job_data

openai.api_key = "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"

def call_openai_api(instruction, prompt):
    model = "gpt-4"
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    return response

def write_coverletter(df, row_number, resume):
    # Convert DataFrame to numpy structured array
    job_data = df.to_records(index=False)

    # Using numpy where condition to get valid links
    valid_jobs = np.where(job_data['Job Description'] != b"INVALID LINK")[0]
    
    if row_number > len(valid_jobs):
        print("Invalid row number!")
        return
    
    job_index = valid_jobs[row_number]
    
    company_name = job_data['Company'][job_index].decode('utf-8')  # Decode bytes to string
    jd = job_data['Job Description'][job_index].decode('utf-8')

    print(f"writing your cover letter for {company_name}!")
    
    instruction = f'''
    Now you should behave like the most advanced robot for generating cover letter for a college student.
    Your task is to generate genuine, professional, and enthusiastic cover letters.
    You will be given a resume later in this prompt and will use the information in the resume,
    including name, education, professional experience, research experience, and another other contents, to write the cover letter.
    Specifically, while writing the cover letter you should showcase than the writer is a good match for the position
    by associating the facts in the resume with the job description/requirement.
    Be careful not to makeup any qualification or experience that is not on the resume.
    The job/company related information will be the input of later conversation,
    I will provide the information of one company per input, and your job is to generate one cover letter tailored for that company each time.
    Below is my resume:
    
    {resume}
    '''
    
    doc = Document()
    response = call_openai_api(instruction, "Below is the job description:" + jd)
    doc.add_paragraph(response['choices'][0]['message']['content'])

    # Save the tailored cover letter
    new_filename = f"Cover_Letter_for_{company_name}.docx"
    doc.save(new_filename)
    
    print(f"Cover letter tailored for {company_name} saved as '{new_filename}'!")

    cost = response['usage']['prompt_tokens'] * 0.03 * 0.001 + response['usage']['prompt_tokens'] * 0.03 * 0.001
    print("total cost: " + str(cost))

# Sample code to simulate using the function (You can modify or remove)
# NOTE: Ensure 'get_job_data' returns a pandas DataFrame.
# job_data_df = get_job_data()
# job_description = input("Please enter the job description:")
# write_coverletter(job_data_df, 0, job_description)


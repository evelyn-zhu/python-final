import requests
import json
import random
import pandas as pd
import xlrd
import os
import openai
import time
from docx import Document
from webscraper import get_job_data

openai.api_key = "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"

def call_openai_api(instruction, prompt):
    # model = "gpt-3.5-turbo"
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

    index = row_number
    for i in range(len(df)):
        if df.loc[i, "Job Description"] != "INVALID LINK":
            index = index - 1
        if index == 0:
            row_number = i
            break

    company_name = df.loc[row_number, "Company"]
    jd = df.loc[row_number, "Job Description"]
    
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

#job_description = input("Please enter the job description:")
#print(job_description)
#write_coverletter(job_description)

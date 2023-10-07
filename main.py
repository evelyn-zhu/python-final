from coverletter_1 import generate_cover_letter, display_jobs_with_numbers
from coverletter_2 import write_coverletter
from webscraper import get_job_data
from similarity import preprocess_text, compute_similarity_and_skills, extract_skills, HARD_SKILLS
from tabulate import tabulate
from docx import Document
from skills import classification, get_skill, give_list
from LinkedIn_Networking_Message import networking_message

def display_menu():
    menu_width = 50
    print("\n" + "█" * menu_width)
    print(" " * ((menu_width - len("Job Analytics Engine")) // 2) + "Job Analytics Engine")
    print("█" * menu_width)
    print("\n{:<5} {:<42}".format("1.", "NLP Powered Job Description Similarity Check"))
    print("{:<5} {:<42}".format("2.", "Extract Skills from Job Title Clusters"))
    print("{:<5} {:<42}".format("3.", "Auto-Generate Cover Letter from Job Data"))
    print("{:<5} {:<42}".format("4.", "AI-Driven LinkedIn Networking Message"))
    print("{:<5} {:<42}".format("5.", "Auto Apply"))
    print("{:<5} {:<42}".format("6.", "Exit Application"))
    print("\n" + "█" * menu_width)

def display_welcome():
    welcome_width = 70
    contributors = ["Chris Wang", "David He", "Evelyn Zhu", "Kathy Wang", "Rui Xi"]
    
    print("\n" + "▓" * welcome_width)
    print(" " * ((welcome_width - len("Welcome to the Job Analytics Engine")) // 2) + "Welcome to the Job Analytics Engine")
    print("▓" * welcome_width)
    print("\nEmpowering your job search and preparation with state-of-the-art AI technology.")
    print("\n" + "─" * welcome_width)
    print("Contributors:")
    for contributor in contributors:
        print(" " * ((welcome_width - len(contributor)) // 2) + contributor)
    print("─" * welcome_width + "\n")



def main():
    display_welcome()
    job_name = input("Please provide the position name you are interested in: ")
    linkedin_account = input("Please provide your linkedin user email (we will not save it): ")
    linkedin_password = input("Please provide your linkedin password (we will not save it): ")
    job_data_df = get_job_data(job_name, linkedin_account, linkedin_password)
    df_cleaned = job_data_df  # Use job_data_df directly

    # Prompt user for resume details first
    resume_file = input("Please provide the filename where your resume is saved: ")

    # Read the file
    if resume_file.endswith('.docx'):
        doc = Document(resume_file)
        resume_text = ' '.join([para.text for para in doc.paragraphs])
    else:
        with open(resume_file, 'r', encoding='utf-8') as file:
            resume_text = file.read()

    extracted_skills = extract_skills(resume_text, HARD_SKILLS)
    print("\nExtracted Skills:")
    for skill in extracted_skills:
        print(skill)

    # Menu-driven loop
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            processed_resume = preprocess_text(resume_text)
            similarity_results = compute_similarity_and_skills(job_data_df, processed_resume)

            headers = ["Position", "Similarity Score", "Overlapping Skills", "Missing Skills"]
            table_data = [(res["Position"], res["Similarity Score"], ', '.join(res["Overlapping Skills"]),
                           ', '.join(res["Missing Skills"])) for res in similarity_results]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

        elif choice == "2":
            job_title = input("Please enter the job title you want to apply for: ")
            df_label, cluster_id = classification(df_cleaned, job_title)
            annotation, job_num = get_skill(df_label, cluster_id)
            result_list = give_list(annotation, job_num)
            print(result_list)

        elif choice == "3":

            # Directly display jobs with row numbers without computing similarity
            display_jobs_with_numbers(job_data_df)

            try:
                row_number = int(input("Please enter the row number of the job you want to generate a cover letter for: "))
                mode = input("To use existing template, press 1; to use AI generated cover letter, press 2:")
                if mode == "1":
                    generate_cover_letter(job_data_df, row_number, resume_text)
                elif mode == "2":
                    write_coverletter(job_data_df, row_number, resume_text)
                else:
                    print("invalid choice, please try again.")
            except ValueError:
                print("Please enter a valid integer row number.")

        elif choice == "4":
            search_string = input("Please enter the company/position/features of people you want to reach out:")
            number_of_connection = input("Please enter the number of people you want to message:")
            networking_message(search_string, int(number_of_connection), linkedin_account, linkedin_password, resume_text)

        elif choice == "5":
            print("we are still implementing this function")
        
        elif choice == "6":
            print("Thanks for using us! See you next time.")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()

from cover_letter import generate_cover_letter, display_jobs_with_numbers
from webscraper import get_job_data
from similarity import preprocess_text, compute_similarity_and_skills, extract_skills, HARD_SKILLS
from tabulate import tabulate
from docx import Document
from skills import classification, get_skill, give_list

def display_menu():
    print("\n--- Job Analysis Menu ---")
    print("1. Find similarity with job descriptions")
    print("2. Extract skills from job title cluster")
    print("3. Generate a cover letter based on a job row number")
    print("4. Exit")

def main():
    job_data_df = get_job_data()
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
        choice = input("Enter your choice (1-4): ")

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
            l = give_list(annotation, job_num)
            print(l)

        elif choice == "3":

            # Directly display jobs with row numbers without computing similarity
            display_jobs_with_numbers(job_data_df)

            try:
                row_number = int(
                    input("Please enter the row number of the job you want to generate a cover letter for: "))
                generate_cover_letter(row_number, resume_text)
            except ValueError:
                print("Please enter a valid integer row number.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()

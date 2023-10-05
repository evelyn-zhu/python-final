from transformers import BertTokenizer, BertModel
import torch
import re
import pandas as pd  # Assuming you will be using a pandas DataFrame for the job data.

# Initialize BERT model and tokenizer
model_name = "bert-base-uncased"
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

#add comment
HARD_SKILLS = [
    "python", "r", "sql", "excel", "machine learning", "deep learning",
    "data analytics", "statistics", "nlp", "tableau", "powerbi", "sas", "java",
    "c++", "hadoop", "spark", "tensorflow", "keras", "pytorch"
]

def preprocess_text(text):
    return text.lower().replace("\n", " ")

def encode_text(text):
    encoded_input = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        output = model(**encoded_input)
    return output.last_hidden_state.mean(dim=1)

def extract_skills(text, skills_list):
    found_skills = []
    text = text.lower()
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill)
    return set(found_skills)

def compute_similarity_and_skills(job_data_df, processed_resume):
    resume_embedding = encode_text(processed_resume)
    resume_skills = extract_skills(processed_resume, HARD_SKILLS)
    results = []

    for index, row in job_data_df.iterrows():
        job_desc = row["Job Description"]
        if job_desc != "INVALID LINK":
            job_desc_embedding = encode_text(job_desc)
            similarity = torch.nn.functional.cosine_similarity(resume_embedding, job_desc_embedding)

            job_skills = extract_skills(job_desc, HARD_SKILLS)
            overlap_skills = resume_skills.intersection(job_skills)
            missing_skills = job_skills - resume_skills

            results.append({
                "Position": row["Position Name"],
                "Similarity Score": similarity.item(),
                "Overlapping Skills": overlap_skills,
                "Missing Skills": missing_skills
            })

    return sorted(results, key=lambda x: x["Similarity Score"], reverse=True)


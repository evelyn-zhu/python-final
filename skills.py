import pandas as pd
import spacy
from sklearn.cluster import MiniBatchKMeans
from spacy.matcher import PhraseMatcher
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor


def clean_data(df):
    df_cleaned = df.dropna(subset=['Position Name',
                                   'Job Description'])  # Drop rows where either 'Position Name' or 'Job Description' is NaN

    df_cleaned["Job Description"] = df_cleaned["Job Description"].apply(remove_stopwords)
    df_cleaned["Position Name"] = df_cleaned["Position Name"].str.lower()
    df_cleaned["Job Description"] = df_cleaned["Job Description"].str.lower()

    return df_cleaned


def classification(df_cleaned, job):
    df_cleaned = clean_data(df_cleaned).head(20)
    job_title = job

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_cleaned["Position Name"])

    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(tfidf_matrix)

    cluster_labels = kmeans.labels_
    result_df = pd.DataFrame({'Position Name': df_cleaned["Position Name"], 'Cluster Label': cluster_labels})
    df_label = pd.concat([result_df.set_index("Position Name"), df_cleaned.set_index("Position Name")],
                         axis=1).reset_index()

    new_job_title_vector = tfidf_vectorizer.transform([job_title])
    predicted_cluster = kmeans.predict(new_job_title_vector)
    return df_label, predicted_cluster[0]


def get_skill(df_label, cluster_id):
    nlp = spacy.load("en_core_web_lg")
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

    job_description = ""
    job_num = 0
    for i in df_label[df_label["Cluster Label"] == cluster_id]["Job Description"]:
        job_description += i
        job_num += 1
    print("Please wait...")

    annotations = skill_extractor.annotate(job_description)
    print("Gonna complete")
    return annotations, job_num


def give_list(annotations, job_num):
    skill_list = {}
    for t in annotations['results']:
        for skill in annotations['results'][t]:
            if skill['doc_node_value'] not in skill_list:
                skill_list[skill['doc_node_value']] = 1
            else:
                skill_list[skill['doc_node_value']] += 1
    l = []
    for key, item in skill_list.items():
        if item >= job_num:
            l.append(key)
    return l

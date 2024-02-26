from fastapi import FastAPI
import uvicorn
from jobs import Applicant
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
# password = quote_plus("n@mkha123")

# # Construct the DB_URL with the encoded password
# DB_URL = f"mysql://root:{password}@127.0.0.1:3306/seeker"
# engine = create_engine(DB_URL)
# Base = declarative_base()
# class Job(Base):
#     __tablename__ = 'base_job_post'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     description = Column(String)
#     education = Column(String)
#     location = Column(String)

# Create session maker
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Create the app object
# app = FastAPI()

# def load_jobs():
#     session = SessionLocal()
#     jobs = session.query(Job).all()
#     session.close()
#     return jobs
# final_jobs = load_jobs()
# final_jobs = pd.DataFrame(final_jobs)
# print(final_jobs.columns)
app = FastAPI()
final_jobs = pd.read_csv('final_jobs.csv')
shared_data = {"normalized_weighted_similarity": None, "user_id": None}
final_jobs['title'] = final_jobs['title'].fillna('')
final_jobs['description'] = final_jobs['description'].fillna('')
final_jobs['education'] = final_jobs['education'].fillna('')
final_jobs['location'] = final_jobs['location'].fillna('')
# pickle_in = open("recommend.pkl","rb")
# recommend_jobs=pickle.load(pickle_in)
all_text_data = (
    final_jobs['title'].astype(str) +
    ' ' +
    final_jobs['description'].astype(str) +
    ' ' +
    final_jobs['education'].astype(str) +
    ' ' +
    final_jobs['location'].astype(str)
)

# Create a TF-IDF vectorizer and fit on all text data
tfidf_vectorizer = TfidfVectorizer()
tfidf_combined = tfidf_vectorizer.fit_transform(all_text_data)

# Transform each individual column
tfidf_jobtitle = tfidf_vectorizer.transform(final_jobs['title'])
tfidf_jobdes = tfidf_vectorizer.transform(final_jobs['description'])
tfidf_jobedu = tfidf_vectorizer.transform(final_jobs['education'])
tfidf_jobloc = tfidf_vectorizer.transform(final_jobs['location'])
# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}



@app.post("/recommend")
def recommend(request: Applicant):
        # Retrieve the applicant's data based on the provided ID
        applicant_id = request.id
        applicant_position = request.position
        applicant_skills = request.skills
        applicant_education = request.education
        applicant_location = request.location
        # applicant_data = applicants_data.loc[applicants_data['ID'] == int(applicant_id)]

        # user_tfidf = tfidf_vectorizer.transform(applicant_data['Position of Interest'])
        user_tfidf = tfidf_vectorizer.transform([applicant_position])
        user_tfidf_reshaped = user_tfidf.reshape(1, -1)
        similarity1 = cosine_similarity(user_tfidf_reshaped, tfidf_jobtitle)
        similarity1= similarity1.flatten().tolist()

        # user_tfidf = tfidf_vectorizer.transform(applicant_data['Skills'])
        user_tfidf = tfidf_vectorizer.transform([applicant_skills])
        user_tfidf_reshaped = user_tfidf.reshape(1, -1)
        similarity2 = cosine_similarity(user_tfidf_reshaped, tfidf_jobdes)
        similarity2= similarity2.flatten().tolist()

        # user_tfidf = tfidf_vectorizer.transform(applicant_data['Education Qualifications'])
        user_tfidf = tfidf_vectorizer.transform([applicant_education])
        user_tfidf_reshaped = user_tfidf.reshape(1, -1)
        similarity3 = cosine_similarity(user_tfidf_reshaped, tfidf_jobedu)
        similarity3= similarity3.flatten().tolist()

        # user_tfidf = tfidf_vectorizer.transform(applicant_data['Locations'])
        user_tfidf = tfidf_vectorizer.transform([applicant_location])
        user_tfidf_reshaped = user_tfidf.reshape(1, -1)
        similarity4 = cosine_similarity(user_tfidf_reshaped, tfidf_jobloc)
        similarity4= similarity4.flatten().tolist()
        # recommended_jobs = recommend.recommend()
        # Assign weights to each similarity type
        weight1 = 0.4# Adjust the weights based on your preferences
        weight2 = 0.4
        weight3 = 0.1
        weight4 = 0.1

        # Compute the weighted average similarity
        weighted_similarity = []
        for i in range(len(similarity1)):
            weighted_similarity.append(
                weight1 * similarity1[i] +
                weight2 * similarity2[i] +
                weight3 * similarity3[i] +
                weight4 * similarity4[i])
            

        # Normalize the weighted similarity to ensure it is in the range [0, 1]
        normalized_weighted_similarity = (np.array(weighted_similarity) / sum([weight1, weight2, weight3, weight4]))

        # Print or use the normalized weighted similarity
        print("Weighted Similarity:", normalized_weighted_similarity)
        normalized_weighted_similarity= normalized_weighted_similarity.flatten().tolist()
        top = sorted(range(len(normalized_weighted_similarity)), key=lambda i: normalized_weighted_similarity[i], reverse=True)[:30]
        # recommendation = pd.DataFrame(columns=['ApplicantID', 'ID'])
        recommendation = pd.DataFrame(columns=['ApplicantID', 'ID', 'title', 'company', 'location','education', 'description'])
        for i, idx in enumerate(top):
            recommendation.loc[i, 'ApplicantID'] = applicant_id
            recommendation.loc[i, 'ID'] = final_jobs.at[idx, 'ID']
            recommendation.loc[i, 'title'] = final_jobs.at[idx, 'title']
            recommendation.loc[i, 'company'] = final_jobs.at[idx, 'company']
            recommendation.loc[i, 'location'] = final_jobs.at[idx, 'location']
            recommendation.loc[i, 'company_id'] = final_jobs.at[idx, 'company_id']
            recommendation.loc[i, 'education'] = final_jobs.at[idx, 'education']
            recommendation.loc[i, 'description'] = final_jobs.at[idx, 'description']

        nearestjobs = recommendation['ID']
        jobs = pd.DataFrame(columns=['ID', 'title', 'company', 'location','education', 'description'])
        count = 0
        for i in nearestjobs:
            index = np.where(final_jobs['ID'] == i)[0][0]
            job_id = i.item()
            jobs.at[count, 'ID'] = job_id
            jobs.at[count, 'title'] = final_jobs.at[index, 'title']
            jobs.at[count, 'company'] = final_jobs.at[index, 'company']
            jobs.at[count, 'location'] = final_jobs.at[index, 'location']
            jobs.at[count, 'education'] = final_jobs.at[index, 'education']
            jobs.at[count, 'description'] = final_jobs.at[index, 'description']
            count += 1
        print("The top 10 recommended Jobs are: ")
        return jobs
    
        # for i, idx in enumerate(top):
        #     recommendation.loc[i, 'ApplicantID'] = applicant_id
        #     recommendation.loc[i, 'ID'] = final_jobs.at[idx, 'ID']
        # nearestjobs = recommendation['ID']
        # jobs = pd.DataFrame(columns=['ID', 'position'])
        # count = 0
        # for i in nearestjobs:
        #     index = np.where(final_jobs['ID'] == i)[0][0]
        #     job_id = i.item()
        #     jobs.at[count, 'ID'] = job_id
        #     jobs.at[count, 'position'] = final_jobs.at[index, 'title']
        #     count += 1
        # print("The top 10 recommended Jobs are: ")
        # return jobs

# @app.post("/recommend")
# def recommend(normalized_weighted_similarity = shared_data["normalized_weighted_similarity"],
#     user_id = shared_data["user_id"]):
    # top = sorted(range(len(normalized_weighted_similarity)), key=lambda i: normalized_weighted_similarity[i], reverse=True)[:30]
    # recommendation = pd.DataFrame(columns=['ApplicantID', 'ID'])
    
    # for i, idx in enumerate(top):
    #     recommendation.loc[i, 'ApplicantID'] = user_id
    #     recommendation.loc[i, 'ID'] = final_jobs.at[idx, 'ID']
    # nearestjobs = recommendation['ID']
    # jobs = pd.DataFrame(columns=['ID', 'position'])
    # count = 0
    
    # for i in nearestjobs:
    #     index = np.where(final_jobs['ID'] == i)[0][0]
    #     jobs.at[count, 'ID'] = i
    #     jobs.at[count, 'position'] = final_jobs.at[index, 'title']
    #     count += 1
    # print("The top 10 recommended Jobs are: ")
    # return jobs


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload
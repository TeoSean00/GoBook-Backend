import json
import pandas as pd
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
nltk.download('stopwords')
nltk.download('punkt')


class ContentBasedFilter:

    class_data = requests.get("http://class_service:5006/class")
    classes_df = pd.DataFrame(class_data.json())
    print("------ initialised dataframe ------")
    # Combine the 'title' and 'description' columns into a single column
    classes_df['combined'] = classes_df['className'] + ' ' + \
        classes_df['content'] + ' ' + classes_df['objective']
    # Tokenize the text and remove stopwords
    stop_words = set(stopwords.words('english'))
    classes_df['combined'] = classes_df['combined'].apply(lambda x: ' '.join([word.lower() for word in word_tokenize(x) if word.lower() not in set(stopwords.words('english'))]))
    # Compute TF-IDF vectors for each title
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(classes_df['combined'])
    print("------ generated cosine_sim ------")
    # Compute cosine similarity between titles
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # Define a function to get recommendations for a given title

    def get_recommendations(booking, cosine_sim=cosine_sim, df=classes_df):

        print("------- df received is --------")
        print(df.head())
        print("------- booking received is --------")
        print(booking,file=sys.stderr)
        print("------- cosine sim received is --------")
        print(cosine_sim,file=sys.stderr)
        print(type(booking))
        
        # Get the index of the title in the dataframe
        idx = df[df['className'] == booking].index[0]
        print("------- idx is --------")
        print(idx)

        # Compute the cosine similarity between the title and all other titles
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the titles by similarity score
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the top 3 most similar titles
        sim_scores = sim_scores[1:4]

        # Get the titles indices
        titles_indices = [i[0] for i in sim_scores]

        # Get class details of recommended classes
        recommendation_items = df.iloc[titles_indices]['_id'].tolist()
        print("Recommended items are ",recommendation_items)
        recommendation_output = []
        for enrolled_class in recommendation_items:
            # This is for docker
            class_data = requests.request("GET", "http://class_service:5006/class/" + str(enrolled_class))
            # class_data = requests.request("GET", "http://localhost:5006/class/" + enrolled_class)
            print("class data received is! HERE!",class_data)
            recommendation_output.append(class_data.json())

        print("recommendation output is! HERE!",recommendation_output)
        # Return the top 3 most similar titles
        return recommendation_output
        # return df.iloc[titles_indices]['className'].tolist()

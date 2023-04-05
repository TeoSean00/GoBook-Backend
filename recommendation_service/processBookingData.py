import json
from contentBasedFilter import ContentBasedFilter
from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import sys
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)  


producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

c = KafkaConsumer('booking',bootstrap_servers= ['kafka:9092'],group_id='my_group_id',auto_offset_reset='latest',value_deserializer=lambda x:loads(x.decode('utf-8')))

# c = KafkaConsumer({
#     'bootstrap.servers': 'kafka:9092',
#     'group.id': 'mygroup',
#     'auto.offset.reset': 'latest'
# })

# def main():
#     while True:
#         msg = c.poll(1.0)

#         if msg is None:
#             continue
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 print('End of partition reached {}'.format(msg.topic()))
#                 continue
#             else:
#                 print('Error while consuming message: {}'.format(msg.error()))
#                 continue
#         else:
#             print('Received message: {}'.format(msg.value().decode('utf-8')))
#             history = msg.value().decode('utf-8')
#             print("History is",json.loads(history))
#             latestBooking = json.loads(history)
#             recommendations = ContentBasedFilter.get_recommendations(latestBooking["className"].strip())
#             recommendObj = {
#                 "userId" : latestBooking["userId"],
#                 "recommendation" : recommendations
#             }
#             print("------- recommendation received is --------",file=sys.stderr)
#             print(recommendObj,file=sys.stderr)
#             producer.send('recommendations', recommendObj)

# def get_classes():
#     classes_df = pd.DataFrame(classes_data)
#     print("------ initialised dataframe ------")
#     # Combine the 'title' and 'description' columns into a single column
#     classes_df['combined'] = classes_df['className'] + ' ' + \
#         classes_df['content'] + ' ' + classes_df['objective']
#     # Tokenize the text and remove stopwords
#     stop_words = set(stopwords.words('english'))
#     classes_df['combined'] = classes_df['combined'].apply(lambda x: ' '.join([word.lower() for word in word_tokenize(x) if word.lower() not in set(stopwords.words('english'))]))
#     # Compute TF-IDF vectors for each title
#     tfidf = TfidfVectorizer()
#     tfidf_matrix = tfidf.fit_transform(classes_df['combined'])
#     print("------ generated cosine_sim ------")
#     # Compute cosine similarity between titles
#     cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # Define a function to get recommendations for a given title

def main():
    for msg in c:
        print('Received message: {}',msg.value)
        history = msg
        print("History is", history.value["metadata"])

        latestBooking = history.value['metadata']
        print("latestBooking is",latestBooking)
        recommendations = ContentBasedFilter.get_recommendations(latestBooking["coursename"].strip())
        recommendObj = {
            "userId" : latestBooking["userID"],
            "recommendation" : recommendations
        }
        print("------- recommendation received is --------",file=sys.stderr)
        print(recommendObj,file=sys.stderr)
        producer.send('recommendations', recommendObj)
        print("Recommendations sent ---------------------------------")
        # producer.flush()


if __name__ == '__main__':
    main()
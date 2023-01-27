import snscrape.modules.twitter as sntwit
import pymongo as pm
import pandas as pd
from pymongo import MongoClient
import streamlit as st
# tweeter data scrapping as per keyword or hashtag
data1=[]
with st.form("my_form"):
    search= st.text_input("Enter a keyword or hashtag based on that daya should be scrapped: ")
    number_tweets=st.slider('Enter the count of tweets to be scrapped:', 0,1000,100)
    num_tweet=int(number_tweets)
    submit=st.form_submit_button("Submit")
    if submit:
        for i,tweet in enumerate(sntwit.TwitterSearchScraper(search).get_items()):
            if i>1000:
                break
            data1.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.likeCount,tweet.source])                                   
df=pd.DataFrame(data1,columns=["Date","ID","URL","Content","User_name","Reply_count","Retweet_count","Language","Likes_count","Source"])
st.write(df)
with st.form("form"):
    st.write("Press Enter to upload the data into database:")
    Enter=st.form_submit_button("Enter")
    if Enter:
        data=df.to_dict("records")
        client=MongoClient("mongodb://localhost:27017/")
        db=client["tweeter_database"]
        collection=db[search]
        db.collection.insert_many(data)
        st.success("Data has been uploaded:",icon='✅')
        st.write("list of collection names:")
        mycoll=db.list_collection_names()
        st.write(mycoll)
st.write("Download the file in the format you want:")
st.write("Download in csv format")
def convert_to_csv(df1):
    return df1.to_csv()
csv_file=convert_to_csv(df)
st.download_button(csv_file,f"{search}_tweet.csv","text/csv",key="download-csv")
st.write("Downalod in json format")
def convert_to_json(df1):
    return df1.to_json()
json_file=convert_to_json(df)
st.download_button(json_file,f"{search}_tweet.json","text/json",key="download-json")

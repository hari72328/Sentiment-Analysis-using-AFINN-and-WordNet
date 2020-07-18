import tweepy 
import pandas as pd
import re
from afinn import Afinn
from matplotlib import pyplot as plt 
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer 
lem = WordNetLemmatizer()
pstem = PorterStemmer() 
stop_words = set(stopwords.words('english'))


consumer_key="Fx5HJUTIrXMa2KGvuARs2a4QJ"
consumer_secret="eVQVdmjif7sSBBkziCLPbRbUCLbuifl6xSLgB5Jn6e5drfWOfe"
access_token="1257959882361196544-qSFoh4fRAK26eQIbZQ4cRzStyABgIS"
access_token_secret="eVfO2fynnsAFBuSiQxBSnxyE1gmHIAQ6EJhYTjX2lvPim"


auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


def entereddata(entered_query,no_of_tweets,n):
    query=entered_query
    tweets=int(no_of_tweets)
    data=[]
    for i,status in enumerate(tweepy.Cursor(api.search,q=query,count=50,lang="en",tweet_mode="extended").items(tweets)):
        ##print(i,status.full_text)  
        data.append(status.full_text)
    df=pd.DataFrame(data,columns=["TEXT"])
    df.drop_duplicates(subset="TEXT",inplace=True) ##removing duplicates
    for i in range(len(df)):
        txt = df.iloc[i]["TEXT"]
        txt=re.sub(r'@[A-Z0-9a-z_:]+','',txt)#replace username-tags
        txt=re.sub(r'^[RT]+','',txt)#replace RT-tags
        txt = re.sub('https?://[A-Za-z0-9./]+','',txt)#replace URLs
        txt=re.sub("[^a-zA-Z]", " ",txt)#replace hashtags
        df.at[i,"TEXT"]=txt
    df_copy=df
    if n==0:
        ##print("yes")
        afinn_fun(df_copy,no_of_tweets)
    elif n==1:
       wordnet_fun(df_copy,no_of_tweets)
        

def afinn_fun(df_copy,no_of_tweets):
    af = Afinn()
    l=[]
    count_total=0
    count_pos=0
    count_neut=0
    count_neg=0
    for i in range(len(df_copy.index)):
        sent = df_copy.iloc[i]['TEXT']
        if(af.score(sent)>0):
            count_pos=count_pos+1
            count_total=count_total+1
        elif(af.score(sent)<0):
            count_neg=count_neg+1
            count_total=count_total+1
        else:
            count_neut=count_neut+1
            count_total=count_total+1
            
    l=[count_pos,count_neg,count_neut]
    show_output(l,count_total,no_of_tweets)

def wordnet_fun(df_copy,no_of_tweets):
    li_swn=[]
    li_swn_pos=[]
    li_swn_neg=[]
    missing_words=[]
    for i in range(len(df_copy.index)):
        text = df_copy.iloc[i]["TEXT"]
        tokens = nltk.word_tokenize(text)
        wordsList = [w for w in tokens if not w in stop_words]  
        tagged_sent =nltk.pos_tag(wordsList)
        store_it = [(word,nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in tagged_sent]
        #print("Tagged Parts of Speech:",store_it)

        pos_total=0
        neg_total=0
        for word,tag in store_it:
            if(tag=='NOUN'):
                tag='n'
            elif(tag=='VERB'):
                tag='v'
            elif(tag=='ADJ'):
                tag='a'
            elif(tag=='ADV'):
                tag = 'r'
            else:
                tag='nothing'

            if(tag!='nothing'):
                concat = word+'.'+tag+'.01'
                try:
                    this_word_pos=swn.senti_synset(concat).pos_score()
                    this_word_neg=swn.senti_synset(concat).neg_score()
                    #print(word,tag,':',this_word_pos,this_word_neg)
                except Exception as e:
                    wor = lem.lemmatize(word)
                    concat = wor+'.'+tag+'.01'
                    # Checking if there's a possiblity of lemmatized word be accepted into SWN corpus
                    try:
                        this_word_pos=swn.senti_synset(concat).pos_score()
                        this_word_neg=swn.senti_synset(concat).neg_score()
                    except Exception as e:
                        wor = pstem.stem(word)
                        concat = wor+'.'+tag+'.01'
                        # Checking if there's a possiblity of lemmatized word be accepted
                        try:
                            this_word_pos=swn.senti_synset(concat).pos_score()
                            this_word_neg=swn.senti_synset(concat).neg_score()
                        except:
                            missing_words.append(word)
                            continue
                pos_total+=this_word_pos
                neg_total+=this_word_neg
        li_swn_pos.append(pos_total)
        li_swn_neg.append(neg_total)

        if(pos_total!=0 or neg_total!=0):
            if(pos_total>neg_total):
                li_swn.append(1)
            else:
                li_swn.append(-1)
        else:
            li_swn.append(0)
    df_copy.insert(1,"pos_score",li_swn_pos,True)
    df_copy.insert(2,"neg_score",li_swn_neg,True)
    df_copy.insert(3,"sent_score",li_swn,True)
    pt=0
    nt=0
    ntr=0
    for i in range(len(df_copy.index)):
        if df_copy.iloc[i]["sent_score"]==1:
            pt=pt+1
        elif df_copy.iloc[i]["sent_score"]==-1:
            nt=nt+1
        else:
            ntr=ntr+1
    tt=pt+nt+ntr
    l=[pt,nt,ntr]
    show_output(l,tt,no_of_tweets)

    

def show_output(l,total_tweets,no_of_tweets):
    # Creating dataset 
    tweets=["POSITIVE","NEGATIVE","NEUTRAL"]
      
    data = l 
    def func(pct, allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return "{:.1f}%\n".format(pct, absolute) 
    # Creating plot 
    fig = plt.figure(figsize =(10, 7))
    fig.patch.set_facecolor('#80c1ff')
    plt.pie(data,autopct = lambda pct: func(pct, data),  labels = tweets,explode=(0.1,0.1,0.1),shadow = True,colors =("blue","red","yellow"),textprops = dict(color ="black") )  
    plt.legend(title ="SENTIMENT",loc ="upper right",prop={"family":"Times New Roman"},bbox_to_anchor=(0.85, 0.5, 0.5, 0.5))
    plt.text(x=1.4,y=-1,s="Total tweets: "+str(no_of_tweets),fontsize=12)
    plt.text(x=1.4,y=-1.1,s="Total tweets with sentiment: "+str(total_tweets),fontsize=12)
    plt.text(x=1.4,y=-1.2,s="Total positive tweets: "+str(l[0]),fontsize=12)
    plt.text(x=1.4,y=-1.3,s="Total negative tweets: "+str(l[1]),fontsize=12)
    plt.text(x=1.4,y=-1.4,s="Total neutral tweets: "+str(l[2]),fontsize=12)
    plt.title("SENTIMENT ANALYSIS",fontsize=20)    
    # show plot 
    plt.show() 
        

    



















        

import tkinter as tk
import requests
from datapreprocessing import *

HEIGHT = 700
WIDTH = 800

def get_output_afinn(entered_query,no_of_tweets):
          try:
                entereddata(entered_query,no_of_tweets,n=0)
          except:
                label2=tk.Label(root,text="TRY TO ENTER VALID INPUT IN BOTH FIELDS",bg="black",fg="white",font=("Helvetica", 16))
                label2.pack()
                root.after(3000, label2.destroy)
        
def get_output_wordnet(entered_query,no_of_tweets):
        try:
                entereddata(entered_query,no_of_tweets,n=1)
                
        except:
                label3=tk.Label(root,text="TRY TO ENTER VALID INPUT IN BOTH FIELDS",bg="black",fg="white",font=("Helvetica", 16))
                label3.pack()
                root.after(3000, label3.destroy)


if __name__=="__main__":
                
        root = tk.Tk()
        root.title("SENTIMENT ANALYSIS USING AFINN AND WORDNET")
    

        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)

        background_image = tk.PhotoImage(file='image.png')
        background_label = tk.Label(root, image=background_image)
        background_label.place(x=0,y=0,relwidth=1, relheight=1)

        frame1 = tk.Frame(root, bg='#80c1ff', bd=5)
        frame1.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.1,anchor="center")

        lb1=tk.Label(frame1,text="ENTER SEARCH QUERY",bg="#80c1ff",font=("Helvetica",11,'bold'))
        lb1.place(relwidth=0.4,relheight=1)


        entry1 = tk.Entry(frame1, font=40)
        entry1.place(relx=0.4,relwidth=0.6, relheight=1)


        frame2= tk.Frame(root, bg='#80c1ff', bd=5)
        frame2.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.1,anchor="center")

        lb2=tk.Label(frame2,text="TWEETS COUNT",bg="#80c1ff",font=("Helvetica",11,'bold'))
        lb2.place(relwidth=0.4,relheight=1)

        entry2= tk.Entry(frame2, font=40)
        entry2.place(relx=0.4,relwidth=0.6, relheight=1)



        button1 = tk.Button(root, text="AFINN",bg="#80c1ff",font=("Helvetica", 16,'bold'), command=lambda: get_output_afinn(entry1.get(),entry2.get()))
        button1.place(relx=0.25, rely=0.7, relwidth=0.2, relheight=0.1,anchor="center")

        button2= tk.Button(root, text="WORDNET",bg="#80c1ff",font=("Helvetica", 16,'bold'), command=lambda: get_output_wordnet(entry1.get(),entry2.get()))
        button2.place(relx=0.75, rely=0.7, relwidth=0.2, relheight=0.1,anchor="center")

        canvas.pack()
        root.mainloop()

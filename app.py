from flask import Flask, render_template, request
import pandas as pd
import random
import csv
import openai

app = Flask(__name__)
openai.api_key = "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"
message_history=[]

@app.route('/')
def home():
    return render_template('home.html')
 

@app.route('/generate/', methods=['GET'])
def generate():
    N = int(request.args.get('nvalue'))
    print(N)
    data = pd.read_csv("https://raw.githubusercontent.com/dev7796/data101_tutorial/main/files/dataset/airbnb.csv")
    aggregate=["mean", "max", "min"]
    attributes = ["name", "host_name", "neighbourhood_group", "neighbourhood", "room_type"]
    numerical_attribute = ["floor", "price"]
    question = "What is the {0} {1} when {2} = {3} and {4} = {5}"
    questionList=[]

    for i in range(0,N):
        first = random.randint(0, len(aggregate)-1) #mean
        second = random.randint(0, len(numerical_attribute)-1) #price
        third = random.randint(0, len(attributes)-1) 
        fourth = random.randint(0, len(data)-1)
        fifth = random.choice([ele for ele in list(range(0,len(attributes))) if ele != third])
        sixth = random.choice([ele for ele in list(range(0,len(data))) if ele != fourth])
        q = question.format(aggregate[first], numerical_attribute[second], attributes[third], data.loc[fourth, attributes[third]], attributes[fifth],data.loc[sixth, attributes[fifth]])
        questionList.append(q)
        with open('questions_list.csv', 'a') as file:
            file.write(q+"\n")

    # f.close()
    return render_template('generate.html', questionList = questionList)

@app.route('/chat/', methods=['GET'])
def chat():
  input = request.args.get("user_input")
  question_type = request.args.get("question_type")
  dataset_link = request.args.get("dataset_link")
  print(question_type)

#   print(dataset_link)
  if(question_type == "Coding"):
      input=input + " (Rcode)"
      if(dataset_link!="No result"):
        input = input+" using "+dataset_link+"as a dataset"
  else:
      input=input + " limit to 200 words"
  # print(question_type)
  # print(input)
  # return "test"
  message_history.append({"role":"user","content":input})
  
  if(question_type=="Coding"):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history
        )
  else:
     completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history,
        max_tokens=200
        )
  gpt_reply = completion.choices[0].message.content
  print(gpt_reply)
  message_history.append({"role":"assistant","content":gpt_reply})
  if(question_type=="Coding"):
    gpt_reply = ''.join(gpt_reply.split("```")[1].split('```')[0])
  return gpt_reply

if __name__ == '__main__':
   app.run(debug=True) # Have always on debug when you develop,before finish version
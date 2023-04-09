from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)
 
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

    return render_template('generate.html', questionList = questionList)


if __name__ == '__main__':
   app.run(debug=True) # Have always on debug when you develop,before finish version
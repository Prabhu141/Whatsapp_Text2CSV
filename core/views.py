from django.shortcuts import render, redirect
from django.http import HttpResponse
import regex
import pandas as pd
import numpy as np
import emoji
import csv
import json
from collections import Counter
import matplotlib.pyplot as plt
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from .models import whatsapp, Film
from .forms import WhatsappForm, FilmForm


def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = regex.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
    s = s.split(":")
    if len(s)==2:
        return True
    else:
        return False

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author= None
    return date, time, author, message
dot='./media/'
def index(requests):
    documents = whatsapp.objects.all()
    for obj in documents:
        baseurls = obj.chat
    print(baseurls)
    data = []
    #conversation = 'whatsapp-chat-data.txt'
    conversation = dot + str(baseurls)
    print(conversation)
    with open(conversation, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    data.append([date, time, author, ' '.join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message = getDatapoint(line)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(line)
    df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.to_csv('./media/data.csv', index = False)
    return HttpResponse('halloo world')


def upload_txt(request):
    if request.method == 'POST':
        form = WhatsappForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('index')
            documents = whatsapp.objects.all()
            for obj in documents:
                baseurls = obj.chat
            print(baseurls)
            # data = []
            # #conversation = 'whatsapp-chat-data.txt'
            # conversation = dot + str(baseurls)
            # print(conversation)
            # with open(conversation, encoding="utf-8") as fp:
            #     fp.readline()
            #     messageBuffer = []
            #     date, time, author = None, None, None
            #     while True:
            #         line = fp.readline()
            #         if not line:
            #             break
            #         line = line.strip()
            #         if date_time(line):
            #             if len(messageBuffer) > 0:
            #                 data.append([date, time, author, ' '.join(messageBuffer)])
            #                 messageBuffer.clear()
            #                 date, time, author, message = getDatapoint(line)
            #                 messageBuffer.append(message)
            #             else:
            #                 messageBuffer.append(line)
            # df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
            # df['Date'] = pd.to_datetime(df['Date'])
            # df.to_csv(dot+'media/data.csv', index = False)
            #filename = "test1.txt"
            filename = dot + str(baseurls)
            df = pd.read_csv(filename, header=0, encoding='utf8')
            # df = pd.read_csv(filename, header=0, na_values=['NA'], delimiter='\t', encoding='utf8')
            # df = pd.read_csv(filename, header=None, names=['col1', 'col2', 'col3'], encoding='utf8')
            # # df = pd.read_csv(filename, header=None, delimiter='\t', encoding='utf8')
            # # df = pd.read_csv(filename, header=None, na_values=['NA'], encoding='utf8')
            #df.head()
            df.to_csv(dot+'media/data.csv', index=False)
            with open(dot+'/media/data.csv', 'r', encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Advance past the header
                for row in reader:
                    print(row)

            # genre, _ = Genre.objects.get_or_create(name=row[0])

                    film, _ = Film.objects.get_or_create(title=row[0],
                      year=row[1],
                      filmurl = row[2],
                      genre=row[3])
                    # film, _ = Film.objects.get_or_create(title=row[3],
                    #   year=row[4],
                    #   filmurl = row[6],
                    #   genre=row[2])
                    film.save()
        #filedata = dot+'/media/data.csv'
        # dfjson = pd.read_csv(filedata , index_col=None, header=0,  encoding= 'unicode_escape')
        # #geeks = df.to_html()
        # json_records = dfjson.reset_index().to_json(orient ='records')
        # data = []
        # data = json.loads(json_records)
        return render(request, 'form_upload.html', {})
    else:
        form = WhatsappForm()
        documents = whatsapp.objects.all()
    return render(request, 'form_upload.html', {
        'form': form
    })
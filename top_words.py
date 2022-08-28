import re
import pymorphy2
import os.path
import os
import docx
import pandas as pd

docsnames = []
docs = []

def get_filenames():
    for path, dirs, files in os.walk(os.path.abspath(r"Docs")):
        docsnames.append(files)

def get_files():
    for name in docsnames[0]:
        filename = 'Docs/' + str(name)
        doc = docx.Document(filename)

        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        file = '\n'.join(text)
        docs.append(file)

get_filenames()
get_files()

# print(docs[1])

morph = pymorphy2.MorphAnalyzer()

#Эта функция приводит все слова к именительному падежу
def lemmatize(text):
    words = text.split() # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)
    return res

text_array = []
i = 0
while i < 39:
    text_array.append([''])
    i += 1

data = docs[19]
block = [19, 44, 68, 74, 92, 136, 146, 156]
I = 0
while I < 165:
    if (I not in block):
        data = docs[I]

        data = re.sub(r'[^\w\s{}]', '', data)
        data = data.lower()

        class_array_open = []
        class_array_close = []
        class_array = []

        i = 0
        while i < len(data):
            if (data[i] == "{"):
                class_array_open.append(i)
            if (data[i] == "}"):
                class_array_close.append(i)
            i += 1

        i = 1
        if (len(class_array_open) > 0):
            last_class_number = data[class_array_open[0] + 1:class_array_close[0]]
            class_array.append(int(last_class_number))
        while i < len(class_array_open):
            tmp = data[class_array_open[i] + 1:class_array_close[i]]
            if (tmp != last_class_number):
                class_array.append(int(data[class_array_open[i] + 1:class_array_close[i]]))
            last_class_number = tmp
            i += 1

        i = 0
        while i < len(class_array_open) - 1:
            text_array[int(data[class_array_open[i] + 1:class_array_close[i]]) - 1].append(
                data[class_array_close[i] + 1:class_array_open[i + 1]])
            i += 1

    I += 1

i = 0
while i < len(text_array):
    j = 0
    ans = ""
    while j < len(text_array[i]):
        ans += re.sub(r'[^\w\s{}]', '', str(text_array[i][j])) + " "
        j += 1
    text_array[i] = ans
    i += 1

i = 0
while i < len(text_array):
    text_array[i] = lemmatize(text_array[i])
    i += 1

i = 0
while i < len(text_array):
    j = 0
    while j < len(text_array[i]):
        if (len(text_array[i][j]) <= 2):
            del text_array[i][j]
        j += 1
    i += 1

words = [] #тут будет уникальный список слов
i = 0
while i < len(text_array):
    text_array[i]
    j = 0
    while j < len(text_array[i]):
        word = text_array[i][j]
        if (word not in words):
            words.append(word)
        j += 1
    i += 1
how_many_times = []# тут будет как часто это слово встречается
i = 0

while i < len(words):
    how_many_times.append(0)
    i += 1


i = 0
while i < len(text_array):
    j = 0
    while j < len(words):
        how_many_times[j] += text_array[i].count(words[j])
        j += 1
    i += 1

sorted_words = []
sorted_how_many_times = []

while len(words) > 0:
    times = max(how_many_times)
    times_index = how_many_times.index(times)
    sorted_how_many_times.append(times)
    sorted_words.append(words[times_index])
    del how_many_times[times_index]
    del words[times_index]

i = 0
while i < 600:
    # print(sorted_words[i] + " : " + str(sorted_how_many_times[i]))
    i += 1


top_words = sorted_words[:600]
file = open('top.txt', 'w')
for word in top_words:
     file.write(word + '\n')



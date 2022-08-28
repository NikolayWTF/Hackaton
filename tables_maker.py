import os
import pandas as pd
import docx
import pymorphy2

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

morph = pymorphy2.MorphAnalyzer()
# Эта функция приводит все слова к именительному падежу
def lemmatize(text):
    words = text.lower().split()  # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)
    return res


get_filenames()
get_files()

lemmatized_docs = []
for doc in docs:
    lemmatized_docs.append(lemmatize(doc))


f = open('top.txt')
columns = [word.strip() for word in f]

data = []
for i in range(39):
    table = []
    for doc in lemmatized_docs:
        freq_for_doc = []
        for word in columns:
            word_freq = doc.count(word)
            freq_for_doc.append(word_freq)
        table.append(freq_for_doc)
    data.append(table)

num = 1
for table in data:
    finder = '{' + str(num) + '}'
    num += 1

    for doc in range(len(lemmatized_docs)):
        if finder in lemmatized_docs[doc]:
            ans = 1.0
        else:
            ans = 0.0
        table[doc].append(ans)

columns.append('ans')
number = 1
for table in data:
    df = pd.DataFrame(table, columns=columns)
    df.to_csv(r'tables/class_' + str(number) + '.csv')
    number += 1

import pandas as pd
import docx
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import math
from sklearn.metrics import accuracy_score
import warnings
import pymorphy2
import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate("hackathon-b45a8-firebase-adminsdk-cf72v-9973a89faa.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://hackathon-b45a8-default-rtdb.europe-west1.firebasedatabase.app/"
	})

ref = db.reference("/Documents")
DOCUMENT = ref.get()

warnings.filterwarnings("ignore")


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

train_data = []
train_target = []
test_data = []
test_target = []
for i in range(1, 40):
    data = pd.read_csv('tables/class_' + str(i) + '.csv')
    train_target.append(data['ans'][:120])
    train_data.append(data.drop(columns=['ans', 'Unnamed: 0'])[:120])
    test_target.append(data['ans'][120:])
    test_data.append(data.drop(columns=['ans', 'Unnamed: 0'])[120:])



log_regs = []
for i in range(39):
    log_reg = LinearRegression().fit(train_data[i], train_target[i])
    log_regs.append(log_reg)

accs = []
for i in range(39):
    train_predictions = log_regs[i].predict(train_data[i])
    test_predictions = log_regs[i].predict(test_data[i])

    train_predictions = list(map(sigmoid, train_predictions))
    test_predictions = list(map(sigmoid, test_predictions))

file = DOCUMENT

morph = pymorphy2.MorphAnalyzer()
def lemmatize(text):
    words = text.lower().split()  # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)
    return res


doc = lemmatize(file)
f = open('top.txt')
columns = [word.strip() for word in f]


freq_for_doc = []
for word in columns:
    word_freq = doc.count(word)
    freq_for_doc.append(word_freq)

res = []
df = pd.DataFrame([freq_for_doc], columns=columns)
for i in range(39):
    preds = log_regs[i].predict(df)
    preds = list(map(sigmoid, preds))
    res.append(preds)
print(res)
ref = db.reference("/Python")
i = 0
while i < 39:
    ref = "/Python/" + str(i+1)
    REF = db.reference(ref)
    REF.set(res[i][0])
    i += 1


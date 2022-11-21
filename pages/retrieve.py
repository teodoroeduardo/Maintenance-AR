import pyrebase
import datetime as dt
import time
import pandas as pd
import json


config = {
        "apiKey":"AIzaSyCO8y67WU4iNACVggXFa-bzcaBwM6mBgDs",
        "authDomain":"181797325455-hll7orv98mlu08sve9bo7cudvtb45lec.apps.googleusercontent.com",
        "databaseURL": "https://unirittermanar-default-rtdb.firebaseio.com",
        "storageBucket":"unirittermanar.appspot.com",
        }
firebase = pyrebase.initialize_app(config)
db = firebase.database()


now = dt.datetime.now()
now_str = now.strftime("%d-%m-%Y %H:%M:%S")

temp = []

q = db.child("Logs/Máquina 1/LogVelocidade").order_by_key().limit_to_last(1).get()

r = q.val()

df = pd.DataFrame(r)

print(df)
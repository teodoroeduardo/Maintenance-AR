import pyrebase

class Setup():
    
    config = {
        "apiKey":"AIzaSyCO8y67WU4iNACVggXFa-bzcaBwM6mBgDs",
        "authDomain":"181797325455-hll7orv98mlu08sve9bo7cudvtb45lec.apps.googleusercontent.com",
        "databaseURL": "https://unirittermanar-default-rtdb.firebaseio.com",
        "storageBucket":"unirittermanar.appspot.com",
        }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

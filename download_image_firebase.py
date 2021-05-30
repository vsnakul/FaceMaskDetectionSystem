import pyrebase
import os
import requests

firebaseConfig = {
    "apiKey": "AIzaSyDlaeLQS7Ud2p4kOe_mWIT3sGtMjXy_JcQ",
    "authDomain": "facereg-813c9.firebaseapp.com",
    "databaseURL": "https://facereg-813c9-default-rtdb.firebaseio.com",
    "projectId": "facereg-813c9",
    "storageBucket": "facereg-813c9.appspot.com",
    "messagingSenderId": "62284980449",
    "appId": "1:62284980449:web:52750fc2c687643d7f57a0",
    "measurementId": "G-01P1W24GBX",
    "serviceAccount": "serviceAccountCredentials.json"
  }

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
parent_directory="D:\SampleFlask\known_faces"
users=db.child("Users").get()
i=0
for user in users.each():
    path=os.path.join(parent_directory,user.val()['Name'])
    print(path)
    print(type(path))
    os.mkdir(path)
    print(user.val()['images'])
    for image in user.val()['images'].values():
        response = requests.get(image)
        file = open(path+"\sample_image"+str(i)+".jpeg", "wb")
        file.write(response.content)
        file.close()
        i+=1







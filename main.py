# import packages
from flask import Flask
from flask_restful import Resource, Api
import database
from flask_httpauth import HTTPBasicAuth
from flask import send_file
import datetime
from pathlib import Path
import random, string
import time, threading
from apscheduler.schedulers.background import BackgroundScheduler
import pyqrcode
import png


scheduler = BackgroundScheduler() # init the scheduler

auth = HTTPBasicAuth() # init the auth
app = Flask(__name__) # init flask
api = Api(app)

# Make the secret string
def makeSecretStr():
    characterPool = string.ascii_letters + string.digits + string.punctuation
    ret = ''.join(random.choice(characterPool)for i in range(4096))
    return ret

# Make secret key
def makeSecretKey():
    with open(Path('/home/pi/Desktop/pydoor/')/'secret.key','w') as f:
        f.write(makeSecretStr())


# Refresh the key every hour
scheduler.add_job(makeSecretKey, 'interval',minutes=60)
scheduler.start()

# Make qr-code from the secret key
def makeQrCode():
    with open(Path('/home/pi/Desktop/pydoor/')/'secret.key','r') as f:
        key = pyqrcode.create(f.read(), error='L', version=40,mode='binary')
        s = time.ctime()
        key.png(s+'.png', scale = 8)
        return str(s) + '.png'


# Log every opening
def logging(user):
    with open(Path('/home/pi/Desktop/pydoor')/'door.log','a') as f:
        f.write(f'{user} was opened the door at : {datetime.datetime.now().strftime("%A %H:%M")}\n')

# Door class wich determine the door can be opened and give back the qr-version of the current secret key
class Door(Resource):
    @auth.login_required 
    def get(self):
        if database.db.DoorCanBeOpened(auth.current_user()):
            logging(auth.current_user())
            s = makeQrCode()
            return send_file(f'/home/pi/{s}', attachment_filename=f'{s}')
        else:
            return {'Msg':'Access denide'}


# Verify password
@auth.verify_password
def verify_password(username, password):
    if database.db.login(username, password):
        return True
    return False


api.add_resource(Door,'/')
if __name__ == '__main__':
    app.run(host='0.0.0.0')

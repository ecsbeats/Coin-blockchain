from turtle import update
from numpy import block
import pyrebase
from flask import Flask
import hashlib
import time 
firebaseConfig = {
  'apiKey': "AIzaSyCcL8gYMfRnhnnUGp9cFDrhW1-JDTjn1ZY",
  'authDomain': "blockchain-project1-c7c92.firebaseapp.com",
  'databaseURL': "https://blockchain-project1-c7c92-default-rtdb.firebaseio.com",
  'projectId': "blockchain-project1-c7c92",
  'storageBucket': "blockchain-project1-c7c92.appspot.com",
  'messagingSenderId': "307271852524",
  'appId': "1:307271852524:web:a137bab6540bb3483aa0c9"
}
db = pyrebase.initialize_app(firebaseConfig)
db = db.database()

class Blockchain_for_coins:
    def __init__(self):
        self.genesisblockpresence = db.child('genesisblockthere').get().val()
        if self.genesisblockpresence=="False":
            self.genesis_block = {
                "proof_ofblock":1,
                "prev_hash":'0',
                "hash_ofblock":hashlib.sha256(str(1).encode()).hexdigest()
            }
            db.child('chain/'+str(time.strftime('%H:%M:%S'))).set(self.genesis_block)
            db.child('/').update({
                'genesisblockthere':'True'
            })

    def create_block(self,proof,prev_hash,hash):
        block_content={
            "proof_ofblock":proof,
            "prev_hash":prev_hash,
            "hash_ofblock":hash
        }
        db.child('chain/'+str(time.strftime('%H:%M:%S'))).set(block_content)
    def validate(self):
        features = db.child('chain').get().val()
        feature_array = []
        proof = 0
        for i in features:
            feature_array.append(i)
        for i in range(0,len(feature_array)-1,1):
            if features[feature_array[i+1]]['prev_hash']==features[feature_array[i]]['hash_ofblock']:
                proof+=1
        last_block = feature_array[len(feature_array)-1]
        total_proof=db.child("chain/"+last_block).get().val()['proof_ofblock']+proof
        db.child("chain/"+last_block).update({
           'proof_ofblock':total_proof
        })
        return proof


    def get_last_block(self):
        features = db.child('chain').get().val()
        features_array = []
        for i in features:
            features_array.append(i)
        last_block = features_array[len(features_array)-1]
        return([last_block,features[last_block]['proof_ofblock'],features[last_block]['hash_ofblock']])
Blockchain_for_coins()
app = Flask(__name__)
@app.route('/mine_block')
def mine_block():
    last_block,proof,hashofblock = Blockchain_for_coins().get_last_block()
    proof_after_validation=Blockchain_for_coins().validate()
    hashval = hashlib.sha256(str(2*(int(proof_after_validation)**2) +2).encode()).hexdigest()
    Blockchain_for_coins().create_block(proof_after_validation,hashofblock,hashval)
    return {
        "amountaftermining":2*(proof**2)+2
    }
@app.route('/validate')
def validation():
    return {'valid blocks':Blockchain_for_coins().validate()}
@app.route('/numberofblocks')
def noblocks():

    features = db.child('chain').get().val()
    features_array = []
    for i in features:
        features_array.append(i)
    return {'total blocks':len(features_array)}

if __name__=='__main__':
    app.run(debug=True,host='localhost',port='8000')

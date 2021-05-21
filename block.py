import hashlib
import time

from PySide2.QtCore import Signal
from transaction import Transaction
from key import verify_signature


class Block:
    def __init__(self, name, informations, index, previousHash, miner = "TheoMarini", transactions = [], timestamp = 0, nonce = 0):
        self.name = name
        self.info = informations
        self.id = index
        self.nonce = nonce
        self.timestamp = time.time()
        self.hash = previousHash
        self.previousHash = previousHash
        self.transactionsList = []
        for el in transactions :
            self.transactionsList.append(el)
        self.miner = miner
        self.merkleroot = ""
        self.signature = None

    def __repr__(self):
        stringTrans = "Transaction:\n"
        for el in self.transactionsList:
            stringTrans += "    " + el.__repr__() + "\n"
        string  = "Block name: " + str(self.name) + "\n" + \
        "Information: " + str(self.info) + "\n" + \
        "Index: " + str(self.id) + "\n" + \
        "Nonce: " + str(self.nonce) + "\n" + \
        "Timestamp: " + str(self.timestamp) + "\n" + \
        "hash: " + str(self.hash) + "\n" + \
        "previousHash: " + str(self.previousHash) + "\n" + \
        "Miner: " + str(self.miner) +  "\n " + \
        stringTrans + "\n"
        return string
    
    def to_dict(self):
        block_dict = {}
        block_dict["index"] = self.id
        block_dict["nonce"] = self.nonce
        block_dict["timestamp"] = self.timestamp
        block_dict["miner"] = self.miner
        block_dict["transactions"] = []
        for elem in self.transactionsList:
            block_dict["transactions"].append(elem.to_dict())
        block_dict["previous_hash"] = self.previousHash
        block_dict["hashval"] = self.hash
        block_dict["Signature"] = str(self.signature)
        return block_dict

    def addTransaction(self, trans, wallet):
        tx = trans
        tx.number = len(self.transactionsList)
        tx.transactionSignature(wallet)
        self.transactionsList.append(tx)

    def hashFunction(self, nonce):
        sha = hashlib.sha256()
        temp = ""
        temp2 = ""
        temp = str(self.timestamp) + str(self.id) + str(self.miner) + \
        str(self.previousHash) + str(self.name) + str(nonce)
        for el in self.transactionsList:
            temp2 = str(el.amount) + str(el.sender) + str(el.receiver) + str(el.number) + str(el.timestamp)
            sha.update(temp.encode())
            el.hash = sha.hexdigest()
            temp += temp2
        sha.update(temp.encode())
        return sha.hexdigest()

    """ def computeMerkleroot(self):
        sha = hashlib.sha256()
        tmp=""
        tmp2=""
        i=0
        if len(self.transactionsList)%2 == 0:
            while i < len(self.transactionsList):
                tmp += self.transactionsList[i]+self.transactionsList[i+1]
                sha.update(temp.encode())
                el.hash = sha.hexdigest()
                i += 2 """


    def mine(self, difficult, condition, wallet):
        self.timestamp = time.time()
        tmp1 = ""
        for i in range(difficult):
            tmp1 += str(condition)
        tmp2 = str(self.hash[:difficult])
        while tmp1 != tmp2:
            self.nonce += 1
            self.hash = self.hashFunction(self.nonce)
            tmp2 = str(self.hash[:difficult])
        sig = str(self.id) + str(self.timestamp) + str(self.name) + \
                str(self.previousHash) + str(self.miner) + str(self.hash) + str(self.nonce)
        signature = wallet.sign(sig)
        self.signature = signature
    
    def verify(self, nonce):
        sig = self.signature
        hash = self.previousHash
        msg = str(self.id) + str(self.timestamp) + str(self.name) + \
                str(self.previousHash) + str(self.miner) + str(self.hash) + str(self.nonce)
        address = self.miner
        if verify_signature(sig.hex(), msg, address) == False:
            print(f"Error Signature sur block: {self.id}")
            return False
        for el in self.transactionsList:
            if el.verifySignature() == False:
                print(f"Error Signature sur transaction: {el.hash}")
                return False
        for i in range(nonce):
            hash = self.hashFunction(nonce)
        if hash != self.hash:
            return False
        return True


            
        
    def blockValide(self, previousHash):
        if self.previousHash == previousHash:
            return True
        return False
        
    pass

"""
@MessariCrypto
@TheBlock__
@gregory_raymond
@lawmaster
@yassineARK
@hasufl
@nic__carter@RyanWatkins_
@Darrenlautf
@mrjasonchoi  
@ydemombynes
@JustineDesto
En bonus pour ceux qui ont terminé :

Stocker la chaîne dans un fichier JSON
(Bonus) : Écrire le bloc sous la forme d’un arbre de Merkle
(Bonus) : Implémenter votre propre fonction de hachage
(Bonus) : Implémenter votre propre algorithme de consensus (en remplacement de la preuve de travail)
"""
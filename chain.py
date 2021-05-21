import time
import copy
import random
from block import Block
from transaction import Transaction
import os

condition=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]


class Blockchain:
    def __init__(self, difficult, reward=0, chain = []):
        self.chain = chain
        self.nbBlock = 1
        self.difficult = difficult
        self.reward = reward
        self.waitingTransactions = []

    def to_dict(self):
        chainDict = {}
        chainDict["blocks"]=[]
        for el in self.chain:
            chainDict["blocks"].append(el.to_dict())
        return chainDict
    
    def __repr__(self):
        string = "Blockchain Created by TheoMarini: \n"
        for el in self.chain:
            string += el.__repr__()  + "\n"
        #string += self.chain[self.nbBlock].__repr__()
        return string

    def create_genesis_block(self, wallet):
        # Manually construct the first block
        block = Block("Admin", "info", self.nbBlock-1, "", wallet.to_address(), [], time.time())
        new_tx = Transaction(self.reward, wallet.to_address(),"me", time.time())
        self.add_transaction("me", wallet.to_address(), self.reward, wallet)
        block.mine(self.difficult, random.choice(condition), wallet)
        sig = str(block.id) + str(block.timestamp) + str(block.name) + \
                str(block.previousHash) + str(block.miner) + str(block.hash) + str(block.nonce)
        signature = wallet.sign(sig)
        block.signature = signature
        self.chain.append(block)
        #self.nbBlock +=1 


    def addBlock(self, block):
        if(block.timestamp < self.chain[-1].timestamp):
            raise ValueError("Error timestamp")
        if(block.id != self.chain[-1].id+1):
            raise ValueError("Error index")
        if(block.previousHash != self.chain[-1].hash):
            raise ValueError("Block not aligned")
        """ if block.verify(block.nonce) != True:
            raise ValueError("Block not valid") """
        self.chain.append(block)
        self.nbBlock +=1
    
    def add_transaction(self, receiver, sender, amount, wallet):
        nb = len(self.waitingTransactions)
        trans = Transaction(amount, sender, receiver, time.time(), nb)
        trans.transactionSignature(wallet)
        self.waitingTransactions.append(trans)
    

    def mine_block(self, wallet):
        self.add_transaction(self.chain[-1].miner, self.chain[-1].miner, self.reward, wallet)
        for i in self.waitingTransactions:
            self.chain[-1].transactionsList.append(i)
        self.waitingTransactions = []
        self.chain[-1].mine(self.difficult, random.choice(condition), wallet)
        #info = "Block " + str(self.nbBlock)
        #self.chain.append(Block("Admin", info, self.nbBlock-1, self.chain[self.nbBlock-2].hash))

    def verifyChain(self):
        for el in self.chain:
            if el.verify(el.nonce) == False:
                return False
        return True


    pass

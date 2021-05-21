from key import verify_signature


class Transaction:
    def __init__(self, amount, sender, receiver, timestamp, number = 0):
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.number = number
        self.timestamp = timestamp
        self.hash = ""
        self.signature = None

    def __repr__(self): 
        string = "Transaction number: " + str(self.number) + "\n" + \
        "Hash: " + str(self.hash) + "\n" + \
        "Sender: " + str(self.sender) + "\n" + \
        "Receiver: " + str(self.receiver) + "\n" + \
        "Amount: " + str(self.amount) + "\n" + \
        "Timestamp: " + str(self.timestamp) + "\n" + \
        "Signature: " + str(self.signature)
        return string
    

    def to_dict(self): 
        transDict = {}
        transDict["number"] = self.number
        transDict["sender"] = self.sender
        transDict["receiver"] = self.receiver
        transDict["amount"] = self.amount
        transDict["timestamp"] = self.timestamp
        transDict["hash"] = self.hash
        transDict["signature"] = str(self.signature)
        return transDict

    def transactionSignature(self, wallet):
        msg = str(self.sender) + str(self.receiver) + str(self.amount)
        signature = wallet.sign(msg)
        self.signature = signature
        #return signature

    def verifySignature(self):
        msg = str(self.sender) + str(self.receiver) + str(self.amount)
        signature = self.signature
        adresse = self.sender
        return verify_signature(signature.hex(), msg, adresse)
    pass

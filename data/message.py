class Message :
    def __init__(self,id:int,reception_date:str,sender_id:str,channel:str,content:str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
        
    def __repr__(self):
        return(f'Message(id={self.id},reception_date={self.reception_date},sender_id={self.sender_id},channel={self.channel},content={self.content})')
    
    def to_dico(self):
        message_dico = {"id": self.id, "reception_date": self.reception_date, "sender_id": self.sender_id, "channel": self.channel, "content": self.content}
        return(message_dico)
    
    @classmethod
    def from_dico(cls,message_dico:dict):
        message_Message = cls(message_dico['id'],message_dico['reception_date'],message_dico['sender_id'],message_dico['channel'],message_dico['content'])
        return(message_Message)
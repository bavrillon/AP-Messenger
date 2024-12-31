class Channel :
    def __init__(self,id:int,name:str,members_ids:list):
        self.id = id
        self.name = name
        self.members_ids = members_ids
    
    def __repr__(self):
        return(f'Channel(id={self.id},name={self.name},members_ids={self.members_ids})')
  
    def to_dico(self):
        channel_dico = {"id": self.id, "name": self.name, "member_ids": self.members_ids}
        return(channel_dico)
    
    @staticmethod
    def from_dico(channel_dico:dict):
        channel_Channel = Channel(channel_dico['id'],channel_dico['name'],channel_dico['member_ids'])
        return(channel_Channel)
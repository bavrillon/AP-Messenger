class Channel :
    def __init__(self,id:int,name:str,members_ids:list[int]):
        self.id = id
        self.name = name
        self.members_ids = members_ids
    
    def __repr__(self):
        return(f'Channel(id={self.id},name={self.name},members_ids={self.members_ids})')
  
    def to_dico(self) -> dict:
        channel_dico = {"id": self.id, "name": self.name, "member_ids": self.members_ids}
        return(channel_dico)
    
    @classmethod
    def from_dico(cls,channel_dico:dict):
        channel_Channel = cls(channel_dico['id'],channel_dico['name'],channel_dico['member_ids'])
        return(channel_Channel)
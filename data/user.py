class User :
    def __init__(self,id:int,name:str):
        self.id = id
        self.name = name

    def __repr__(self):
        return(f'User(id={self.id},name={self.name})')
  
    def to_dico(self) -> dict:
        user_dico = {"id": self.id, "name": self.name}
        return(user_dico)
    
    @classmethod
    def from_dico(cls,user_dico:dict) :
        user_User = cls(user_dico['id'],user_dico['name'])
        return(user_User)
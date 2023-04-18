from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re

DATABASE = 'project'


class Character:
    def __init__(self, data: dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.race = data['race']
        self.age = data['age']
        self.sex = data['sex']
        self.strength = data['strength']
        self.intelligence = data['intelligence']
        self.wisdom = data['wisdom']
        self.dexterity = data['dexterity']
        self.background_story = data['background_story']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data: dict) -> int:
        query = "INSERT INTO project.characters (first_name,last_name,race,age,sex,strength,intelligence,wisdom,dexterity,background_story,user_id) VALUES (%(first_name)s,%(last_name)s,%(race)s,%(age)s,%(sex)s,%(strength)s,%(intelligence)s,%(wisdom)s,%(dexterity)s,%(background_story)s,%(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        return result

    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM characters;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        characters = []
        for dictionary in results:
            characters.append( cls(dictionary))
        return characters
    
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM Characters WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE characters SET first_name=%(first_name)s,last_name=%(last_name)s,race=%(race)s,age=%(age)s,sex=%(sex)s,strength=%(strength)s,intelligence=%(intelligence)s,wisdom=%(wisdom)s,dexterity=%(dexterity)s,background_story=%(background_story)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM characters WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
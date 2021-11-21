DB_FILE = 'Monstres'

from datetime import datetime

def time():
    
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    s1 = now.strftime("%H:%M-%d/%m/%Y")
    return s1
    
    
def consultation_monster(dictionnaire):
    return -1


def add_monster(dictionnaire):
    """
    Specs : Ajouter un nouveau monstre (t-uplet) à la table Monstres
    Preconditions : Le dictionnaire est composé d'un nom(str), niveau(int), un type(str), une valeur d'attaque(int), un nombre de points de vie(int) et une rareté(str)
    Postconditions : Un t-uplet a été ajouté à la table si le nom de monstre n'est pas déjà utilisé, la fonction renvoie 1 si tout s'est bien passé, -1 si un montre avec ce nom existe déjà, et 0 si un paramètre est mal saisi
    """
    
    conn = creer_connexion(DB_FILE+'.db')

    if consultation_monster(dictionnaire['nom']) == -1:
        if type(dictionnaire['nom']) == str and type(dictionnaire['niveau']) == int and type(dictionnaire['type']) == str and type(dictionnaire['attaque']) == int and type(dictionnaire['vie']) == int and type(dictionnaire['rarete']) == str:
            cur = conn.cursor()
            date = time()
            cur.execute(f"INSERT INTO Monstres(nom, niveau, date_creation, type, attaque, vie, rarete) \
            VALUES('{dictionnaire['nom']}', '{dictionnaire['niveau']}', '{date}', '{dictionnaire['type']}', \
            '{dictionnaire['attaque']}', '{dictionnaire['vie']}', '{dictionnaire['rarete']}');")
            rows = cur.fetchall()
            conn.commit()
            conn.close()
            return 1
        else:
            conn.close()
            return 0
    else:
        conn.close()
        return -1
    
    
    
    
if __name__ == "__main__":

    DB_FILE = 'test'
    conn = creer_connexion(DB_FILE+'.db')
    majBD(conn, DB_FILE+'.sql')
    dictionnaire1 = {'nom': 'NouveauMonstre', 'date_creation': '11:40-15/11/2021', 'niveau': 2, 'type': 'feu', 'attaque': 4, 'vie': 10, 'rarete': 'rare'}
    dictionnaire2 = {'nom': 'NouveauMonstreEncore', 'date_creation': '11:40-15/11/2021', 'niveau': 4, 'type': 'feu', 'attaque': 2, 'vie': 50, 'rarete': 'commun'}
    # dictionnaire3['nom'] est déjà dans la base de donnée
    dictionnaire3 = {'nom' : 'Pikachu', 'date_creation': '02:20:12-12/02/2004', 'niveau': 5, 'type': 'feu', 'attaque': 10, 'vie':1, 'rarete': 'commun'}
    # dictionnaire4 comporte des erreurs, exemple le niveau est une chaîne de caractères
    dictionnaire4 = {'nom' : 10, 'date_creation': '09:12-01/12/1980', 'niveau': 'unechainedecharacteres', 'type': 78, 'attaque': 'salut', 'vie':'non', 'rarete': 42}

    assert add_monster(dictionnaire1) == 1
    assert consultation_monster('NouveauMonstre') == dictionnaire1

    assert add_monster(dictionnaire2) == 1
    assert consultation_monster('NouveauMonstreEncore') == dictionnaire2

    assert add_monster(dictionnaire3) == -1
    assert add_monster(dictionnaire4) == 0

conn.close()
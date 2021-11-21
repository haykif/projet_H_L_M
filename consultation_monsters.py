import sqlite3
DB_FILE = 'Monstres'

def creer_connexion(DB_FILE):
    """ cree une connexion a la base de donnees SQLite
        specifiee par db_file
        le fichier est créé s'il n'existe pas.
    :param db_file: fichier BD (.db)
    :return: objet connexion ou None
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        #On active les foreign keys
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except sqlite3.Error as e:
        print(e)

    return None

def majBD(conn, file):
    """ execute les requêtes SQL de file pour modifier la DB conn
    :param conn: objet connexion
    :param file: fichier SQL (.SQL)
    :return: 
    """
    # Lecture du fichier et placement des requetes dans un tableau
    createFile = open(file, 'r')
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Execution de toutes les requetes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        cursor.execute(query)

    # commit des modifications
    conn.commit()

def consultation_monster(nom_M):
    """
    Consulter les informations d'un monstre présentes dans la table Monstres à partir de son nom.
    Pré-Condition : nom_M est une chaine de caractères et nom est un attribut déjà présent dans la table Monstres (nom). 
    Post-Condition : Le t-uplet correspondant au nom va être renvoyé sous forme de dictionnaire ayant comme clées : nom (str), date_creation (str), niveau (int), type (str), attaque (int), vie (int), rarete (str). 
    Si le nom demmandé n'existe pas, -1 est renvoyé. 
    """
    #On récupère la liste de tout les noms provenant de la base de données, dans la table "Monstres".

    conn = creer_connexion(DB_FILE+'.db')
    cur1 = conn.cursor()
    cur1.execute("SELECT nom\
                  FROM Monstres")
    rows1 = cur1.fetchall()
    #On vérifie que le nom choisit en argument en appelant la fonction est bien présent dans la base de données, dans la table "Monstres".
    erreur = True

    for i in range(len(rows1)-1):
        if nom_M != rows1[i][0]:
            pass
        else:
            erreur = False
    #S'il n'y a pas d'erreur, l'éxécution du programme continue. 
    if erreur == False:
        cur = conn.cursor()
        cur.execute(f"SELECT *\
                    FROM Monstres\
                    WHERE nom = '{nom_M}'")
        
        rows = cur.fetchall()
        dict_renvoi = {'nom':rows[0][0],'date_creation':rows[0][1],'niveau':rows[0][2],'type':rows[0][3],'attaque':rows[0][4],\
            'vie':rows[0][5],'rarete':rows[0][6]}
        conn.close()
        return dict_renvoi #Le dictionnaire correspondant au t-uplet est renvoyé.
    else:
        #S'il y a une erreur, -1 est renvoyé.
        conn.close()
        return -1

from datetime import datetime

def time():
    
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    s1 = now.strftime("%H:%M-%d/%m/%Y")
    return s1
    
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
    conn = creer_connexion(DB_FILE +'.db')
    #majBD(conn, DB_FILE+'.sql')
    dictionnaire1 = {'nom': 'NouveauMonstre', 'date_creation': '11:40-15/11/2021', 'niveau': 2, 'type': 'feu', 'attaque': 4, 'vie': 10, 'rarete': 'rare'}
    dictionnaire2 = {'nom': 'NouveauMonstreEncore', 'date_creation': '11:40-15/11/2021', 'niveau': 4, 'type': 'feu', 'attaque': 2, 'vie': 50, 'rarete': 'commun'}
    # dictionnaire3['nom'] est déjà dans la base de donnée
    dictionnaire3 = {'nom' : 'Pikachu', 'date_creation': '02:20:12-12/02/2004', 'niveau': 5, 'type': 'feu', 'attaque': 10, 'vie':1, 'rarete': 'commun'}
    # dictionnaire4 comporte des erreurs, exemple le niveau est une chaîne de caractères
    dictionnaire4 = {'nom' : 10, 'date_creation': '09:12-01/12/1980', 'niveau': 'unechainedecharacteres', 'type': 78, 'attaque': 'salut', 'vie':'non', 'rarete': 42}
    
    assert add_monster(dictionnaire1) == 1
    print(consultation_monster('NouveauMonstre'))
    assert consultation_monster('NouveauMonstre') == dictionnaire1

    assert add_monster(dictionnaire2) == 1
    assert consultation_monster('NouveauMonstreEncore') == dictionnaire2
    
    assert add_monster(dictionnaire3) == -1
    assert add_monster(dictionnaire4) == 0


    assert consultation_monster("Pikachu") == {'nom': 'Pikachu', 'date_creation': '11:40-15/11/2021', 'niveau': 35, 'type': 'electrique', 'attaque': 10, 'vie': 20, 'rarete': 'epique'}
    assert consultation_monster("Florizzare") == {'nom': 'Florizzare', 'date_creation': '11:40-06/11/2021', 'niveau': 20, 'type': 'plante', 'attaque': 10, 'vie': 20, 'rarete': 'rare'}
    assert consultation_monster("ah") == -1
    assert consultation_monster("") == -1
    conn.close()

add_monster({'nom': 'Toggepi', 'date_creation': '11:40-15/11/2021', 'niveau': 2, 'type': 'feu', 'attaque': 4, 'vie': 10, 'rarete': 'rare'})

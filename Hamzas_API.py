import sqlite3
from consultation_monsters import consultation_monster

DB_FILE = 'Monstres'

def creer_connexion(db_file):
    """ cree une connexion a la base de donnees SQLite
        specifiee par db_file
        le fichier est créé s'il n'existe pas.
    :param db_file: fichier BD (.db)
    :return: objet connexion ou None
    """
    try:
        conn = sqlite3.connect(db_file)
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


def update(nom, dict_change):
    '''
    Cette fontion permet de modifier un t-uplet dans la table Monstres
    Pré-condition: Avoir l'attribut "nom"(str) et le dictionnaire pré-créé(dict_change) possèdant les clés:
    "niveau"(int), "type"(str), "attaque"(int), "vie"(int), "rarete"(str).
    Post-condition: Avec l'attribut "nom"(str) la fonction détecte quel monstre elle doit changer
    et donc la change dans la BDD selon le dictionnaire, la fonction renvoie 1 si tout s'est bien passé
    et 0 si un paramètre est mal saisi.
    '''
    #On récupère la liste de tout les noms provenant de la base de données, dans la table "Monstres".
    conn = creer_connexion(DB_FILE+'.db')
    cur1 = conn.cursor()
    cur1.execute("SELECT nom\
                  FROM Monstres")
    rows1 = cur1.fetchall()
    #On vérifie que le nom choisit en argument en appelant la fonction est bien présent dans la base de données, dans la table "Monstres".
    erreur = True
    for i in range(len(rows1)-1):
        if nom != rows1[i][0]:
            pass
        else:
            erreur = False
    #S'il n'y a pas d'erreur, le programme continue à s'exécuter.
    if erreur == False:
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE Monstres
            SET niveau = "{dict_change['niveau']}",
            type = "{dict_change['type']}",
            attaque = "{dict_change['attaque']}",
            vie = "{dict_change['vie']}",
            rarete = "{dict_change['rarete']}"
            """)

        rows = cur.fetchall()
        conn.commit()
        conn.close()
        renvoi_dict = {'niveau': rows[0][2], 'type': rows[0][3], 'attaque': rows[0][4], 'vie': rows[0][5], 'rarete': rows[0][6]}
        return renvoi_dict #T-uplet renvoyé sous forme de dictionnaire.
    else:
        #Le programme retourne 0 si une erreur est présente.
        conn.close()
        return 0

if __name__ == "__main__":
        DB_FILE = 'test'
        conn = creer_connexion(DB_FILE+'.db')
        majBD(conn, 'test.sql')
        
        Pikachu_dict = {'niveau': 1, 'type': 'electrique', 'attaque': 10, 'vie': 20, 'rarete': 'epique'}
        Pikachu_dictnom = {'nom': 'Pikachu', 'niveau': 1, 'type': 'electrique', 'attaque': 10, 'vie': 20, 'rarete': 'epique'}
        
        assert update('Pikachu', Pikachu_dict) == 1
        assert consultation_monster('Pikachu') == Pikachu_dictnom
        
        Dracaufeu_dict = {'niveau': 96, 'type': 'eau', 'attaque': 1000, 'vie': 99999, 'rarete': 'commun'}
        Dracaufeu_dictnom = {'nom': 'Dracaufeu', 'niveau': 96, 'type': 'eau', 'attaque': 1000, 'vie': 99999, 'rarete': 'commun'}
        
        assert update('Dracaufeu', Dracaufeu_dict) == 1
        assert consultation_monster('Dracaufeu') == Dracaufeu_dictnom
        
        assert update(5, {'niveau': 1, 'type': 'electrique', 'attaque': 10, 'vie': 20, 'rarete': 'epique'}) == 0
        
        Salamèche_dict = {'niveau': 1, 'type': 'electrique', 'attaque': 10, 'vie': 20, 'rarete': 'epique'}
        Salamèche_dictnom = {'nom': 'Salamèche', 'niveau': 1, 'type': 'electrique', 'attaque': 10, 'vie': 20, 'rarete': 'epique'}
       
        assert update('Salamèche', Salamèche_dict) == 1
        assert consultation_monster('Salamèche') == Salamèche_dictnom
        
        conn.close()
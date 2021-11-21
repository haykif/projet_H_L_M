DROP TABLE IF EXISTS Monstres;

CREATE TABLE Monstres(
    nom TEXT,
    date_creation TEXT,
    niveau INT,
    type TEXT,
    attaque INT,
    vie INT,
    rarete TEXT,
    CONSTRAINT PK_Monstres PRIMARY KEY(nom)
);

INSERT INTO Monstres VALUES ('Pikachu', '11:40-15/11/2021', 1, 'electrique', 10, 20, 'epique')
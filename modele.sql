CREATE TABLE Capteurs (
    capteur_id VARCHAR(50) PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    piece VARCHAR(50) NOT NULL,
    emplacement VARCHAR(100)
);

CREATE TABLE Relevés (
    releve_id INT PRIMARY KEY AUTO_INCREMENT,
    capteur_id VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature FLOAT,
    FOREIGN KEY (capteur_id) REFERENCES Capteurs(capteur_id)
);

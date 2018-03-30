CREATE TABLE clients (ID int NOT NULL, Name varchar(255) NOT NULL, Email varchar(255), CEP int, Phone1 varchar(32), Phone2 varchar(32), CPF varchar(16) NOT NULL, Password varchar(255) NOT NULL, Birthday varchar(16), Sex boolean, PRIMARY KEY (ID));

CREATE TABLE client_access (access_token varchar(255) NOT NULL, ID int NOT NULL, PRIMARY KEY (access_token), FOREIGN KEY (ID) REFERENCES clients(ID));

INSERT INTO clients (ID, Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (1, 'John', 'john@mail.jonh', '13456-098', '(19)987654321', '08965632154', 'ohlala', '01121998');

INSERT INTO clients (ID, Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (2, 'Capitu', 'capi1876@casmurro.com', '13456-098', '(19)678543109', '098543788611', 'ja08786', '23061822');

INSERT INTO clients (ID, Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (3, 'Rockman', 'mega@man.com', '76541-198', '(71)33457165', '12371766522', '0986151', '01011991');

INSERT INTO clients (ID, Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (4, 'Genghis Khan', 'khan@mongolia.dom', '34561-198', '(71)123456789', '09876512345', 'europesucks', '190121001')

INSERT INTO clients (ID, Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (5, 'Genghis Khan', 'khan@mongolia.dom', '34561-198', '(71)123456789', '09876512345', 'europesucks', '190121001')
CREATE TABLE public.clients (ID SERIAL PRIMARY KEY, Name varchar(255) NOT NULL, Email varchar(255) NOT NULL UNIQUE, CEP int, Phone1 varchar(32), Phone2 varchar(32), CPF varchar(16) NOT NULL, Password varchar(32) NOT NULL, Birthday varchar(16), Sex boolean, Active boolean default TRUE);

INSERT INTO clients (Name, Email, CEP, Phone1, CPF, Password, Birthday) VALUES ('John', 'john@mail.jonh', '13456098', '(19)987654321', '08965632154', 'ohlala', '01121998');

INSERT INTO clients (Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES ('Capitu', 'capi1876@casmurro.com', '13456098', '(19)678543109', '098543788611', 'ja08786', '23061822');

INSERT INTO clients (Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (3, 'Rockman', 'mega@man.com', '76541198', '(71)33457165', '12371766522', '0986151', '01011991');

INSERT INTO clients (Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (4, 'Genghis Khan', 'khan@mongolia.dom', '34561198', '(71)123456789', '09876512345', 'europesucks', '190121001');

INSERT INTO clients (Name, Email, CEP, Phone1, CPF, Password, Birthday)
VALUES (5, 'Genghis Khan', 'khan2@mongolia.dom', '34561198', '(71)123456789', '09876512345', 'europesucks', '190121001');

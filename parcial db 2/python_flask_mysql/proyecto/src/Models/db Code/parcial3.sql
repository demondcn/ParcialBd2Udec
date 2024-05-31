CREATE DATABASE parcial3;
USE parcial3;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nom` varchar(50) DEFAULT NULL,
  `cro` varchar(50) DEFAULT NULL,
  `usu` varchar(50) DEFAULT NULL,
  `cnt` varchar(150) DEFAULT NULL
)

CREATE TABLE Articulos (
    codart INT AUTO_INCREMENT PRIMARY KEY,
    nomart VARCHAR(255) NOT NULL
);

CREATE TABLE Proveedores (
    idprov INT AUTO_INCREMENT  PRIMARY KEY,
    nomprov VARCHAR(255) NOT NULL
);

CREATE TABLE Proveedores_Telefonos (
    idprov INT,
    telprov VARCHAR(20),
    PRIMARY KEY (idprov, telprov),
    FOREIGN KEY (idprov) REFERENCES Proveedores(idprov)
);

CREATE TABLE Articulos_Proveedores (
    codart INT,
    idprov INT,
    precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (codart, idprov),
    FOREIGN KEY (codart) REFERENCES Articulos(codart),
    FOREIGN KEY (idprov) REFERENCES Proveedores(idprov) 
);

--- insercion de datos de ejemplo
INSERT INTO Articulos (nomart) VALUES
('Artículo 1'),
('Artículo 2'),
('Artículo 3');

INSERT INTO Proveedores (nomprov) VALUES
('Proveedor 4'),
('Proveedor 5'),
('Proveedor 6'),
('Proveedor 7'),
('Proveedor 8'),
('Proveedor 9'),
('Proveedor 10');

INSERT INTO Proveedores_Telefonos (idprov, telprov) VALUES
(1, '123-456-7890'),
(2, '987-654-3210'),
(3, '555-555-5555');

INSERT INTO Articulos_Proveedores (codart, idprov, precio) VALUES
(1, 1, 10.00),
(2, 2, 15.00),
(3, 3, 20.00);

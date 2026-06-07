USE SGA_Database
GO

-- ============================================================================
-- 1. CONTROL DE ELIMINACIÓN PREVIA (DROP TABLES INVERSO)
-- ============================================================================
DROP TABLE IF EXISTS Organiza_Bien;
DROP TABLE IF EXISTS Gestion_CuentaBanco;
DROP TABLE IF EXISTS Organiza_FacturaTesorero;
DROP TABLE IF EXISTS Organiza_FacturaPresidente;
DROP TABLE IF EXISTS Gestion_PresidenteJefeDep;
DROP TABLE IF EXISTS Gestion_PresidenteTesorero;
DROP TABLE IF EXISTS Gestion_PresidenteSecretario;
DROP TABLE IF EXISTS Gestion_SecretarioContrato;
DROP TABLE IF EXISTS Crea_Reunion;
DROP TABLE IF EXISTS Guarda_Acta;
DROP TABLE IF EXISTS Visualiza_Archivo;
DROP TABLE IF EXISTS Encargado_Departamento;
DROP TABLE IF EXISTS Organiza_Grupo;
DROP TABLE IF EXISTS Gestion_Sesion;
DROP TABLE IF EXISTS Crea_Tarea;
DROP TABLE IF EXISTS Gestion_JefeMiembro;
DROP TABLE IF EXISTS TieneSesion;
DROP TABLE IF EXISTS TieneTarea;
DROP TABLE IF EXISTS EstaEnGrupo;
DROP TABLE IF EXISTS EstaEnDepartamento;
DROP TABLE IF EXISTS Gestion_MiemArch;
DROP TABLE IF EXISTS Bienes;
DROP TABLE IF EXISTS Tareas;
DROP TABLE IF EXISTS Sesiones;
DROP TABLE IF EXISTS Grupos;
DROP TABLE IF EXISTS Departamentos;
DROP TABLE IF EXISTS Facturas;
DROP TABLE IF EXISTS Actas;
DROP TABLE IF EXISTS Reuniones;
DROP TABLE IF EXISTS Contratos;
DROP TABLE IF EXISTS Cuenta_Banco;
DROP TABLE IF EXISTS Archivos;
DROP TABLE IF EXISTS Secretarios;
DROP TABLE IF EXISTS Tesoreros;
DROP TABLE IF EXISTS Jefes_de_Departamento;
DROP TABLE IF EXISTS Presidentes;
DROP TABLE IF EXISTS LoginUsuario;
DROP TABLE IF EXISTS Miembros;
GO

-- ============================================================================
-- 2. CREACIÓN DE TABLAS MAESTRAS Y ESQUEMAS DE HERENCIA
-- ============================================================================
SET DATEFORMAT ymd;

CREATE TABLE Miembros(
    UsuarioID INT identity(1, 1) not null,
    DNI char(9) not null,
    [Name] nvarchar(30) not null,
    NombreUsuario nvarchar(30) not null,
    Surname nvarchar(80) not null,
    Rol varchar(20) not null DEFAULT ('MIEMBRO'), 
    Aceptado bit DEFAULT 0,
    Telefono INT not null,
    Email varchar(100) not null,

    CONSTRAINT PK_UsuarioID PRIMARY KEY (UsuarioID),
    CONSTRAINT UQ_Usuario_DNI UNIQUE (DNI),
    CONSTRAINT UQ_Miembros_NombreUsuario UNIQUE (NombreUsuario), 
    CONSTRAINT CK_Passengers_DNI CHECK (DNI LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][A-Z]'),
    CONSTRAINT CK_Usuario_Rol CHECK (UPPER(Rol) IN ('PRESIDENTE', 'SECRETARIO', 'TESORERO', 'JEFE DEPARTAMENTO', 'MIEMBRO'))
);

CREATE TABLE LoginUsuario(
    NombreUsuario nvarchar(30) not null,
    Contrasena nvarchar(30) not null,
    CONSTRAINT PK_NombreUsuario PRIMARY KEY (NombreUsuario),
    CONSTRAINT FK_LoginUsuario_Miembros FOREIGN KEY (NombreUsuario) 
        REFERENCES Miembros(NombreUsuario) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Secretarios(
	SecretarioID INT not null,
	Pin_secretario INT identity(1,1) not null,
	CONSTRAINT PK_Secretarios PRIMARY KEY (SecretarioID),
	CONSTRAINT FK_Secretarios_SecretarioID FOREIGN KEY (SecretarioID) REFERENCES Miembros(UsuarioID) ON DELETE CASCADE
);

CREATE TABLE Tesoreros(
	TesoreroID INT not null,
	Pin_tesorero INT identity(1,1) not null,
	CONSTRAINT PK_Tesoreros PRIMARY KEY (TesoreroID),
	CONSTRAINT FK_Tesoreros_TesoreroID FOREIGN KEY (TesoreroID) REFERENCES Miembros(UsuarioID) ON DELETE CASCADE
);

CREATE TABLE Jefes_de_Departamento(
	JefeDepID INT not null,
	Pin_jefedep INT identity(1,1) not null CONSTRAINT UQ_Pin_JefeDep UNIQUE,
	CONSTRAINT PK_Jefes_de_Departamento PRIMARY KEY (JefeDepID),
	CONSTRAINT FK_Jefes_de_Departamento_JefeDepID FOREIGN KEY (JefeDepID) REFERENCES Miembros(UsuarioID) ON DELETE CASCADE
);

CREATE TABLE Presidentes(
	AdminID INT not null,
	Pin_admin INT identity(1,1) not null,
	CONSTRAINT PK_Presidentes PRIMARY KEY (AdminID),
	CONSTRAINT FK_Presidentes_AdminID FOREIGN KEY (AdminID) REFERENCES Miembros(UsuarioID) ON DELETE CASCADE
);

CREATE TABLE Archivos(
	ArchivoID INT identity(1,1) not null CONSTRAINT PK_ArchivoID PRIMARY KEY,
	Tipo varchar(15) not null CONSTRAINT CK_Tipo CHECK (UPPER(Tipo) IN ('PDF', 'EXCEL', 'CSV', 'RAR', 'TXT', 'JPG', 'PNG')),
	Num_download INT not null,
	Num_view INT not null
);

CREATE TABLE Tareas(
	[Name] varchar(100) not null CONSTRAINT PK_Tareas PRIMARY KEY,
	Fecha_limite datetime not null,
	Descripcion varchar(150)
);

CREATE TABLE Sesiones(
	[Name] varchar(100) not null CONSTRAINT PK_Sesiones PRIMARY KEY,
	Ubicacion varchar(80) not null
);

CREATE TABLE Grupos(
    GrupoID INT identity(1,1) not null CONSTRAINT PK_GroupID PRIMARY KEY,
    Num_miembros INT not null DEFAULT 0,
    [Name] varchar(50) not null, 
    Pin_jefedep INT NULL CONSTRAINT FK_Grupos_Pin_jefedep FOREIGN KEY (Pin_jefedep) REFERENCES Jefes_de_Departamento(Pin_jefedep)
);

CREATE TABLE Departamentos(
	Num_Dep INT identity(1,1) not null CONSTRAINT PK_Num_Dep PRIMARY KEY,
	tipo varchar(50) not null
);

CREATE TABLE Facturas(
	FacturaID INT identity(1,1) not null CONSTRAINT PK_FacturaID PRIMARY KEY,
	fecha date not null,
	cantidad DECIMAL(10,2) not null
);

CREATE TABLE Actas(
	ActasID INT identity(1,1) not null CONSTRAINT PK_ActasID PRIMARY KEY,
	fecha date not null
);

CREATE TABLE Reuniones(
	ReunionID INT identity(1,1) not null CONSTRAINT PK_ReunionID PRIMARY KEY,
	fecha datetime not null,
	tipo varchar(50) not null
);

CREATE TABLE Contratos(
	ContratoID INT identity(1,1) not null CONSTRAINT PK_ContratoID PRIMARY KEY,
	fecha date not null,
	duracion varchar(50)
);

CREATE TABLE Cuenta_Banco(
	IBAN char(20) not null,
	Saldo DECIMAL(12,2) not null,
	CONSTRAINT PK_IBAN PRIMARY KEY (IBAN),
	CONSTRAINT CK_IBAN CHECK (UPPER(IBAN) LIKE ('[A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'))
);

CREATE TABLE Bienes(
	BienID INT identity(1,1) not null CONSTRAINT PK_BienID PRIMARY KEY,
	tipo varchar(30) not null,
	precio DECIMAL(10,2) not null CONSTRAINT CK_Bienes_precio CHECK (precio > 0),
	cantidad INT not null CONSTRAINT CK_Bienes_cantidad CHECK (cantidad > 0)
);

-- ============================================================================
-- 3. CREACIÓN DE TABLAS INTERMEDIAS / RELACIONES
-- ============================================================================

CREATE TABLE Gestion_MiemArch(
	UsuarioID INT not null,
	ArchivoID INT not null,
	CONSTRAINT PK_Gestion_MiemArch PRIMARY KEY (UsuarioID, ArchivoID), 
    CONSTRAINT FK_Miembro_UsuarioID FOREIGN KEY (UsuarioID) REFERENCES Miembros(UsuarioID),
    CONSTRAINT FK_Archivos_ArchivoID FOREIGN KEY (ArchivoID) REFERENCES Archivos(ArchivoID)
);

CREATE TABLE Gestion_JefeMiembro (
    JefeDepID INT NOT NULL,
    UsuarioID INT NOT NULL,
    CONSTRAINT PK_Gestion_JefeMiembro PRIMARY KEY (JefeDepID, UsuarioID),
    CONSTRAINT FK_GJM_Jefe FOREIGN KEY (JefeDepID) REFERENCES Jefes_de_Departamento(JefeDepID),
    CONSTRAINT FK_GJM_Miembro FOREIGN KEY (UsuarioID) REFERENCES Miembros(UsuarioID)
);

CREATE TABLE Crea_Tarea (
    JefeDepID INT NOT NULL,
    TareaName varchar(100) NOT NULL,
    CONSTRAINT PK_Crea_Tarea PRIMARY KEY (JefeDepID, TareaName),
    CONSTRAINT FK_CT_Jefe FOREIGN KEY (JefeDepID) REFERENCES Jefes_de_Departamento(JefeDepID),
    CONSTRAINT FK_CT_Tarea FOREIGN KEY (TareaName) REFERENCES Tareas([Name])
);

CREATE TABLE Gestion_Sesion (
    JefeDepID INT NOT NULL,
    SesionName varchar(100) NOT NULL,
    CONSTRAINT PK_Gestion_Sesion PRIMARY KEY (SesionName), 
    CONSTRAINT FK_GS_Jefe FOREIGN KEY (JefeDepID) REFERENCES Jefes_de_Departamento(JefeDepID),
    CONSTRAINT FK_GS_Sesion FOREIGN KEY (SesionName) REFERENCES Sesiones([Name])
);

CREATE TABLE Organiza_Grupo (
    JefeDepID INT NOT NULL,
    GrupoID INT NOT NULL,
    CONSTRAINT PK_Organiza_Grupo PRIMARY KEY (GrupoID), 
    CONSTRAINT FK_OG_Jefe FOREIGN KEY (JefeDepID) REFERENCES Jefes_de_Departamento(JefeDepID),
    CONSTRAINT FK_OG_Grupo FOREIGN KEY (GrupoID) REFERENCES Grupos(GrupoID)
);

CREATE TABLE Encargado_Departamento (
    JefeDepID INT NOT NULL,
    Num_Dep INT NOT NULL,
    CONSTRAINT PK_Encargado_Departamento PRIMARY KEY (JefeDepID), 
    CONSTRAINT FK_ED_Jefe FOREIGN KEY (JefeDepID) REFERENCES Jefes_de_Departamento(JefeDepID),
    CONSTRAINT FK_ED_Departamento FOREIGN KEY (Num_Dep) REFERENCES Departamentos(Num_Dep)
);

CREATE TABLE Visualiza_Archivo (
    GrupoID INT NOT NULL,
    ArchivoID INT NOT NULL,
    CONSTRAINT PK_Visualiza_Archivo PRIMARY KEY (GrupoID, ArchivoID),
    CONSTRAINT FK_VA_Grupo FOREIGN KEY (GrupoID) REFERENCES Grupos(GrupoID),
    CONSTRAINT FK_VA_Archivo FOREIGN KEY (ArchivoID) REFERENCES Archivos(ArchivoID)
);

CREATE TABLE Guarda_Acta (
    SecretarioID INT NOT NULL,
    ActasID INT NOT NULL,
    CONSTRAINT PK_Guarda_Acta PRIMARY KEY (SecretarioID, ActasID),
    CONSTRAINT FK_GA_Secretario FOREIGN KEY (SecretarioID) REFERENCES Secretarios(SecretarioID),
    CONSTRAINT FK_GA_Acta FOREIGN KEY (ActasID) REFERENCES Actas(ActasID)
);

CREATE TABLE Crea_Reunion (
    SecretarioID INT NOT NULL,
    ReunionID INT NOT NULL,
    CONSTRAINT PK_Crea_Reunion PRIMARY KEY (SecretarioID, ReunionID),
    CONSTRAINT FK_CR_Secretario FOREIGN KEY (SecretarioID) REFERENCES Secretarios(SecretarioID),
    CONSTRAINT FK_CR_Reunion FOREIGN KEY (ReunionID) REFERENCES Reuniones(ReunionID)
);

CREATE TABLE Gestion_SecretarioContrato (
    SecretarioID INT NOT NULL,
    ContratoID INT NOT NULL,
    CONSTRAINT PK_Gestion_SecretarioContrato PRIMARY KEY (SecretarioID, ContratoID),
    CONSTRAINT FK_GSC_Secretario FOREIGN KEY (SecretarioID) REFERENCES Secretarios(SecretarioID),
    CONSTRAINT FK_GSC_Contrato FOREIGN KEY (ContratoID) REFERENCES Contratos(ContratoID)
);

CREATE TABLE Gestion_PresidenteSecretario (
    AdminID INT NOT NULL,
    SecretarioID INT NOT NULL,
    CONSTRAINT PK_Gestion_PresidenteSecretario PRIMARY KEY (AdminID, SecretarioID),
    CONSTRAINT FK_GPS_Admin FOREIGN KEY (AdminID) REFERENCES Presidentes(AdminID),
    CONSTRAINT FK_GPS_Secretario FOREIGN KEY (SecretarioID) REFERENCES Secretarios(SecretarioID)
);

CREATE TABLE Gestion_PresidenteTesorero (
    AdminID INT NOT NULL,
    TesoreroID INT NOT NULL,
    CONSTRAINT PK_Gestion_PresidenteTesorero PRIMARY KEY (AdminID, TesoreroID),
    CONSTRAINT FK_GPT_Admin FOREIGN KEY (AdminID) REFERENCES Presidentes(AdminID),
    CONSTRAINT FK_GPT_Tesorero FOREIGN KEY (TesoreroID) REFERENCES Tesoreros(TesoreroID)
);

CREATE TABLE Gestion_PresidenteJefeDep (
    AdminID INT NOT NULL,
    JefeDepID INT NOT NULL,
    CONSTRAINT PK_Gestion_PresidenteJefeDep PRIMARY KEY (AdminID, JefeDepID),
    CONSTRAINT FK_GPJD_Admin FOREIGN KEY (AdminID) REFERENCES Presidentes(AdminID),
    CONSTRAINT FK_GPJD_Jefe FOREIGN KEY (JefeDepID) REFERENCES Jefes_de_Departamento(JefeDepID)
);

CREATE TABLE Organiza_FacturaPresidente (
    AdminID INT NOT NULL,
    FacturaID INT NOT NULL,
    CONSTRAINT PK_Organiza_FacturaPresidente PRIMARY KEY (AdminID, FacturaID),
    CONSTRAINT FK_OFP_Admin FOREIGN KEY (AdminID) REFERENCES Presidentes(AdminID),
    CONSTRAINT FK_OFP_Factura FOREIGN KEY (FacturaID) REFERENCES Facturas(FacturaID)
);

CREATE TABLE Organiza_FacturaTesorero (
    TesoreroID INT NOT NULL,
    FacturaID INT NOT NULL,
    CONSTRAINT PK_Organiza_FacturaTesorero PRIMARY KEY (TesoreroID, FacturaID),
    CONSTRAINT FK_OFT_Tesorero FOREIGN KEY (TesoreroID) REFERENCES Tesoreros(TesoreroID),
    CONSTRAINT FK_OFT_Factura FOREIGN KEY (FacturaID) REFERENCES Facturas(FacturaID)
);

CREATE TABLE Gestion_CuentaBanco (
    TesoreroID INT NOT NULL,
    IBAN char(20) NOT NULL,
    CONSTRAINT PK_Gestion_CuentaBanco PRIMARY KEY (TesoreroID), 
    CONSTRAINT FK_GCB_Tesorero FOREIGN KEY (TesoreroID) REFERENCES Tesoreros(TesoreroID),
    CONSTRAINT FK_GCB_Banco FOREIGN KEY (IBAN) REFERENCES Cuenta_Banco(IBAN)
);

CREATE TABLE Organiza_Bien (
    TesoreroID INT NOT NULL,
    BienID INT NOT NULL,
    CONSTRAINT PK_Organiza_Bien PRIMARY KEY (TesoreroID, BienID),
    CONSTRAINT FK_OB_Tesorero FOREIGN KEY (TesoreroID) REFERENCES Tesoreros(TesoreroID),
    CONSTRAINT FK_OB_Bien FOREIGN KEY (BienID) REFERENCES Bienes(BienID)
);

CREATE TABLE EstaEnDepartamento (
    UsuarioID INT NOT NULL,
    DepartamentoID INT NOT NULL,
    FechaVinculacion DATE DEFAULT GETDATE(),
    PRIMARY KEY (UsuarioID, DepartamentoID),
    CONSTRAINT FK_EstaEnDepto_Miembro FOREIGN KEY (UsuarioID) REFERENCES Miembros(UsuarioID) ON DELETE CASCADE,
    CONSTRAINT FK_EstaEnDepto_Depto FOREIGN KEY (DepartamentoID) REFERENCES Departamentos(Num_Dep) ON DELETE CASCADE
);

CREATE TABLE EstaEnGrupo (
    UsuarioID INT NOT NULL,
    GrupoID INT NOT NULL,
    FechaIngreso DATE DEFAULT GETDATE(),
    PRIMARY KEY (UsuarioID, GrupoID),
    CONSTRAINT FK_EstaEnGrupo_Miembro FOREIGN KEY (UsuarioID) REFERENCES Miembros(UsuarioID) ON DELETE CASCADE,
    CONSTRAINT FK_EstaEnGrupo_Grupo FOREIGN KEY (GrupoID) REFERENCES Grupos(GrupoID) ON DELETE CASCADE
);

CREATE TABLE TieneTarea (
    GrupoID INT NOT NULL,
    TareaID VARCHAR(100) NOT NULL,
    EstadoTarea VARCHAR(20) DEFAULT 'Pendiente',
    PRIMARY KEY (GrupoID, TareaID),
    CONSTRAINT FK_TieneTarea_Grupo FOREIGN KEY (GrupoID) REFERENCES Grupos(GrupoID) ON DELETE CASCADE,
    CONSTRAINT FK_TieneTarea_Tarea FOREIGN KEY (TareaID) REFERENCES Tareas([Name]) ON DELETE CASCADE
);

CREATE TABLE TieneSesion (
    GrupoID INT NOT NULL,
    SesionID VARCHAR(100) NOT NULL,
    AsistenciaObligatoria BIT DEFAULT 1,
    PRIMARY KEY (GrupoID, SesionID),
    CONSTRAINT FK_TieneSesion_Grupo FOREIGN KEY (GrupoID) REFERENCES Grupos(GrupoID) ON DELETE CASCADE,
    CONSTRAINT FK_TieneSesion_Sesion FOREIGN KEY (SesionID) REFERENCES Sesiones([Name]) ON DELETE CASCADE
);
GO


GO
CREATE TRIGGER TR_ActualizarNumMiembros
ON EstaEnGrupo
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM inserted)
    BEGIN
        UPDATE Grupos
        SET Num_miembros = (SELECT COUNT(*) FROM EstaEnGrupo WHERE EstaEnGrupo.GrupoID = Grupos.GrupoID)
        WHERE GrupoID IN (SELECT DISTINCT GrupoID FROM inserted);
    END

    IF EXISTS (SELECT 1 FROM deleted)
    BEGIN
        UPDATE Grupos
        SET Num_miembros = (SELECT COUNT(*) FROM EstaEnGrupo WHERE EstaEnGrupo.GrupoID = Grupos.GrupoID)
        WHERE GrupoID IN (SELECT DISTINCT GrupoID FROM deleted);
    END
END;
GO

-- ============================================================================
-- 4. POBLACIÓN DE REGISTROS (INSERTS) - CON SANGRE LIMPIA ANTI-ERRORES
-- ============================================================================

-- Forzamos la interpretación global del formato de fecha de inserción
SET DATEFORMAT ymd;

INSERT INTO Miembros (DNI, [Name], NombreUsuario, Surname, Rol, Telefono, Email, Aceptado) VALUES 
('12345678A', 'Carlos','carlitos', 'García', 'PRESIDENTE', 600123456, 'carlos@sga.com', 1),
('87654321B', 'Ana','ana', 'Martínez', 'TESORERO', 600654321, 'ana@sga.com', 1),
('11111111C', 'David','deivid', 'López', 'JEFE DEPARTAMENTO', 611223344, 'david@sga.com', 1),
('22222222D', 'Elena','Gnomo', 'Sánchez', 'SECRETARIO', 622334455, 'elena@sga.com', 1),
('33333333E', 'Lucas','luck', 'Pérez', 'MIEMBRO', 633445566, 'lucas@sga.com', 0),
('44444444F', 'Laura','lauri', 'Gómez', 'MIEMBRO', 644556677, 'laura@sga.com', 1);

INSERT INTO LoginUsuario (NombreUsuario, Contrasena) VALUES 
('carlitos', 'AdminPres123!'),
('ana', 'TesoroPass456!'),
('deivid', 'JefeDep789!'),
('Gnomo', 'Secretario321!'),
('luck', 'MiembroBasico3'),
('lauri', 'MiembroFijo2');

INSERT INTO Presidentes (AdminID) VALUES (1);
INSERT INTO Tesoreros (TesoreroID) VALUES (2);
INSERT INTO Jefes_de_Departamento (JefeDepID) VALUES (3);
INSERT INTO Secretarios (SecretarioID) VALUES (4);

INSERT INTO Archivos (Tipo, Num_download, Num_view) VALUES 
('PDF', 12, 45),
('EXCEL', 5, 20);

INSERT INTO Departamentos (tipo) VALUES 
('Mecanica'),
('Fabricación'),
('Aerodinámica'),
('Redes'),
('Electronica y Seguridad');

INSERT INTO Grupos (Name) VALUES 
('Grupo A - Motor'),
('Grupo B - Chasis'),
('Grupo C - Telemetria');

-- CORRECCIÓN: Nombres de Tareas limpios (sin tildes ni caracteres extraños)
INSERT INTO Tareas (Name, Descripcion, Fecha_limite) VALUES 
('Gestion del carburador', 'Rediseniar la entrada de aire del motor principal aplicando dinamica de fluidos.', '2026-06-15 00:00:00'),
('Decisiones estructurales', 'Validar los puntos de torsion mecanica y soldaduras del eje trasero.', '2026-06-18 00:00:00'),
('Configuracion de antenas', 'Solucionar la perdida de paquetes en el modulo de transmision de 2.4GHz.', '2026-06-22 00:00:00'),
('Firma de balance anual', 'Revision obligatoria del estado de cuentas y facturas del segundo trimestre.', '2026-06-10 00:00:00');

INSERT INTO Sesiones (Name, Ubicacion) VALUES 
('Sesion Tecnica Especial de Motores', 'Laboratorio de Motores A-102'),
('Asamblea de Presupuesto General', 'Sala de Juntas Principal'),
('Sprint Planning 1', 'Sala de Desarrollo B');

INSERT INTO Facturas (fecha, cantidad) VALUES 
('2026-05-10', 1250.75),
('2026-05-28', 340.00);

INSERT INTO Actas (fecha) VALUES 
('2026-05-01'),
('2026-05-15');

INSERT INTO Reuniones (fecha, tipo) VALUES 
('2026-06-05 10:00:00', 'Ordinaria Semanal'),
('2026-06-20 16:30:00', 'Extraordinaria');

INSERT INTO Contratos (fecha, duracion) VALUES 
('2026-01-01', '1 Anio'),
('2026-03-15', '6 Meses');

INSERT INTO Cuenta_Banco (IBAN, Saldo) VALUES 
('ES123456789012345678', 25450.80);

INSERT INTO Bienes (tipo, precio, cantidad) VALUES 
('Portatiles i7', 850.00, 10),
('Pizarras digitales', 420.50, 3);

INSERT INTO Gestion_MiemArch (UsuarioID, ArchivoID) VALUES (5, 1), (6, 2);
INSERT INTO Gestion_JefeMiembro (JefeDepID, UsuarioID) VALUES (3, 5), (3, 6);

-- CORRECCIÓN: Relaciones adaptadas a los textos limpios
INSERT INTO Crea_Tarea (JefeDepID, TareaName) VALUES 
(3, 'Gestion del carburador'), 
(3, 'Decisiones estructurales');

INSERT INTO Gestion_Sesion (JefeDepID, SesionName) VALUES (3, 'Sprint Planning 1');

INSERT INTO Organiza_Grupo (JefeDepID, GrupoID) VALUES (3, 1), (3, 2);
INSERT INTO Encargado_Departamento (JefeDepID, Num_Dep) VALUES (3, 1);
INSERT INTO Visualiza_Archivo (GrupoID, ArchivoID) VALUES (1, 1), (2, 2);
INSERT INTO Guarda_Acta (SecretarioID, ActasID) VALUES (4, 1), (4, 2);
INSERT INTO Crea_Reunion (SecretarioID, ReunionID) VALUES (4, 1), (4, 2);
INSERT INTO Gestion_SecretarioContrato (SecretarioID, ContratoID) VALUES (4, 1), (4, 2);

INSERT INTO Gestion_PresidenteSecretario (AdminID, SecretarioID) VALUES (1, 4);
INSERT INTO Gestion_PresidenteTesorero (AdminID, TesoreroID) VALUES (1, 2);
INSERT INTO Gestion_PresidenteJefeDep (AdminID, JefeDepID) VALUES (1, 3);
INSERT INTO Organiza_FacturaPresidente (AdminID, FacturaID) VALUES (1, 1);

INSERT INTO Organiza_FacturaTesorero (TesoreroID, FacturaID) VALUES (2, 2);
INSERT INTO Gestion_CuentaBanco (TesoreroID, IBAN) VALUES (2, 'ES123456789012345678');
INSERT INTO Organiza_Bien (TesoreroID, BienID) VALUES (2, 1), (2, 2);

INSERT INTO EstaEnDepartamento (UsuarioID, DepartamentoID) VALUES 
(3, 1), (6, 1), (1, 1), (2, 2);

INSERT INTO EstaEnGrupo (UsuarioID, GrupoID) VALUES 
(3, 1), (6, 1), (1, 1), (6, 2), (2, 3);

-- CORRECCIÓN: Vinculaciones de relaciones seguras sin caracteres especiales
INSERT INTO TieneTarea (GrupoID, TareaID, EstadoTarea) VALUES 
(1, 'Gestion del carburador', 'En Progreso'), 
(1, 'Decisiones estructurales', 'Pendiente'),    
(2, 'Decisiones estructurales', 'En Progreso'), 
(3, 'Configuracion de antenas', 'Pendiente');   

INSERT INTO TieneSesion (GrupoID, SesionID, AsistenciaObligatoria) VALUES 
(1, 'Sesion Tecnica Especial de Motores', 1), 
(2, 'Sesion Tecnica Especial de Motores', 0), 
(3, 'Asamblea de Presupuesto General', 1);

INSERT INTO Grupos (Name) VALUES ('Tesorería');

DECLARE @GrupoTesoreriaID INT;
SELECT @GrupoTesoreriaID = GrupoID FROM Grupos WHERE Name = 'Tesorería';

-- Vincular a Ana (Tesorera, UsuarioID = 2) y a Carlos (Presidente, UsuarioID = 1)
INSERT INTO EstaEnGrupo (UsuarioID, GrupoID) VALUES (2, @GrupoTesoreriaID);
INSERT INTO EstaEnGrupo (UsuarioID, GrupoID) VALUES (1, @GrupoTesoreriaID);

-- 3. Asignar la tarea financiera que tenías creada pero sin grupo asignado
INSERT INTO TieneTarea (GrupoID, TareaID, EstadoTarea) 
VALUES (@GrupoTesoreriaID, 'Firma de balance anual', 'Pendiente');
GO

-- ============================================================================
-- 5. CONSULTAS DE COMPROBACIÓN COMPLETAS
-- ============================================================================
SELECT * FROM Tareas;
SELECT * FROM TieneTarea;
SELECT * FROM Sesiones;
SELECT * FROM TieneSesion;
GO
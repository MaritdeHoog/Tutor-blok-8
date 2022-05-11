-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-05-11 10:05:17.135

-- tables
-- Table: Personen
CREATE TABLE Personen (
    z_id int NOT NULL,
    z_score int NOT NULL,
    namen_naam_id int NOT NULL,
    CONSTRAINT Personen_pk PRIMARY KEY (z_id)
);

-- Table: Table_7
CREATE TABLE Table_7 (
    namen_naam_id int NOT NULL,
    pathways_pathway_id int NOT NULL
);

-- Table: Table_8
CREATE TABLE Table_8 (
    namen_naam_id int NOT NULL,
    fluids_fluid_id int NOT NULL
);

-- Table: Ziektes
CREATE TABLE Ziektes (
    ziekte_id int NOT NULL,
    ziekte varchar(100) NOT NULL,
    CONSTRAINT Ziektes_pk PRIMARY KEY (ziekte_id)
);

-- Table: fluids
CREATE TABLE fluids (
    fluid_id int NOT NULL,
    fluid varchar(100) NOT NULL,
    CONSTRAINT fluids_pk PRIMARY KEY (fluid_id)
);

-- Table: namen
CREATE TABLE namen (
    naam_id int NOT NULL,
    naam varchar(100) NOT NULL,
    descerption varchar(500) NOT NULL,
    HMDB_code text NOT NULL,
    Ziektes_ziekte_id int NOT NULL,
    CONSTRAINT namen_pk PRIMARY KEY (naam_id)
);

-- Table: pathways
CREATE TABLE pathways (
    pathway_id int NOT NULL,
    pathway varchar(250) NOT NULL,
    CONSTRAINT pathways_pk PRIMARY KEY (pathway_id)
);

-- foreign keys
-- Reference: Personen_namen (table: Personen)
ALTER TABLE Personen ADD CONSTRAINT Personen_namen FOREIGN KEY Personen_namen (namen_naam_id)
    REFERENCES namen (naam_id);

-- Reference: Table_7_namen (table: Table_7)
ALTER TABLE Table_7 ADD CONSTRAINT Table_7_namen FOREIGN KEY Table_7_namen (namen_naam_id)
    REFERENCES namen (naam_id);

-- Reference: Table_7_pathways (table: Table_7)
ALTER TABLE Table_7 ADD CONSTRAINT Table_7_pathways FOREIGN KEY Table_7_pathways (pathways_pathway_id)
    REFERENCES pathways (pathway_id);

-- Reference: Table_8_fluids (table: Table_8)
ALTER TABLE Table_8 ADD CONSTRAINT Table_8_fluids FOREIGN KEY Table_8_fluids (fluids_fluid_id)
    REFERENCES fluids (fluid_id);

-- Reference: Table_8_namen (table: Table_8)
ALTER TABLE Table_8 ADD CONSTRAINT Table_8_namen FOREIGN KEY Table_8_namen (namen_naam_id)
    REFERENCES namen (naam_id);

-- Reference: namen_Ziektes (table: namen)
ALTER TABLE namen ADD CONSTRAINT namen_Ziektes FOREIGN KEY namen_Ziektes (Ziektes_ziekte_id)
    REFERENCES Ziektes (ziekte_id);

-- End of file.


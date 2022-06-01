-- Making the tables
-- Table: Personen
CREATE TABLE Personen (
    persoon_id int NOT NULL AUTO_INCREMENT,     -- the persoon_id can't be zero
    patient_id varchar(20) NOT NULL UNIQUE ,        -- patient_id has to be unique
    CONSTRAINT Personen_pk PRIMARY KEY (persoon_id)
);

-- Table: Table_7
CREATE TABLE Table_7 (
    pathways_pathway_id int NOT NULL,
    metabolieten_met_id int NOT NULL
);

-- Table: Table_8
CREATE TABLE Table_8 (
    fluids_fluid_id int NOT NULL,
    metabolieten_met_id int NOT NULL
);

-- Table: Table_9
CREATE TABLE Table_9 (
    voorspelde_ziektes_vziekte_id int NOT NULL,
    methaboliten_met_id int NOT NULL,
    hoeveelehid int NOT NULL
);

-- Table: Ziektes
CREATE TABLE Ziektes (
    ziekte_id int NOT NULL AUTO_INCREMENT,
    ziekte varchar(100) NOT NULL UNIQUE ,
    CONSTRAINT Ziektes_pk PRIMARY KEY (ziekte_id)
);

-- Table: fluids
CREATE TABLE fluids (
    fluid_id int NOT NULL AUTO_INCREMENT,
    fluid varchar(100) NOT NULL UNIQUE ,
    CONSTRAINT fluids_pk PRIMARY KEY (fluid_id)
);

-- Table: methaboliten
CREATE TABLE metabolieten (
    met_id int NOT NULL AUTO_INCREMENT,
    naam varchar(100) NOT NULL UNIQUE ,
    description varchar(500) NOT NULL,
    HMDB_code text NOT NULL UNIQUE ,
    Ziektes_ziekte_id int,
    CONSTRAINT metabolieten_pk PRIMARY KEY (met_id)
);

-- Table: pathways
CREATE TABLE pathways (
    pathway_id int NOT NULL AUTO_INCREMENT,
    pathway varchar(250) NOT NULL UNIQUE ,
    CONSTRAINT pathways_pk PRIMARY KEY (pathway_id)
);

-- Table: z
CREATE TABLE z (
    score_id int NOT NULL AUTO_INCREMENT,
    z_score float NOT NULL,
    metabolieten_met_id int NOT NULL,
    Personen_persoon_id int NOT NULL,
    CONSTRAINT z_pk PRIMARY KEY (score_id)
);

-- Table: voorspelde_ziektes
CREATE TABLE voorspelde_ziektes (
    vziekte_id int NOT NULL AUTO_INCREMENT,
    vziekte varchar(150) NOT NULL UNIQUE ,
    CONSTRAINT voorspelde_ziektes_pk PRIMARY KEY (vziekte_id)
);



-- foreign keys
-- Reference: Table_7_methaboliten (table: Table_7)
ALTER TABLE Table_7 ADD CONSTRAINT Table_7_metabolieten FOREIGN KEY Table_7_metabolieten (metabolieten_met_id)
    REFERENCES metabolieten (met_id);

-- Reference: Table_7_pathways (table: Table_7)
ALTER TABLE Table_7 ADD CONSTRAINT Table_7_pathways FOREIGN KEY Table_7_pathways (pathways_pathway_id)
    REFERENCES pathways (pathway_id);

-- Reference: Table_8_fluids (table: Table_8)
ALTER TABLE Table_8 ADD CONSTRAINT Table_8_fluids FOREIGN KEY Table_8_fluids (fluids_fluid_id)
    REFERENCES fluids (fluid_id);

-- Reference: Table_8_methaboliten (table: Table_8)
ALTER TABLE Table_8 ADD CONSTRAINT Table_8_metabolieten FOREIGN KEY Table_8_methaboliten (metabolieten_met_id)
    REFERENCES metabolieten (met_id);

-- Reference: Table_9_methaboliten (table: Table_9)
ALTER TABLE Table_9 ADD CONSTRAINT Table_9_methaboliten FOREIGN KEY Table_9_methaboliten (methaboliten_met_id)
    REFERENCES metabolieten (met_id);

-- Reference: Table_9_voorspelde_ziektes (table: Table_9)
ALTER TABLE Table_9 ADD CONSTRAINT Table_9_voorspelde_ziektes FOREIGN KEY Table_9_voorspelde_ziektes (voorspelde_ziektes_vziekte_id)
    REFERENCES voorspelde_ziektes (vziekte_id);

-- Reference: namen_Ziektes (table: methaboliten)
ALTER TABLE metabolieten ADD CONSTRAINT namen_Ziektes FOREIGN KEY namen_Ziektes (Ziektes_ziekte_id)
    REFERENCES Ziektes (ziekte_id);

-- Reference: z_Personen (table: z)
ALTER TABLE z ADD CONSTRAINT z_Personen FOREIGN KEY z_Personen (Personen_persoon_id)
    REFERENCES Personen (persoon_id);

-- Reference: z_methaboliten (table: z)
ALTER TABLE z ADD CONSTRAINT z_metabolieten FOREIGN KEY z_metabolieten (metabolieten_met_id)
    REFERENCES metabolieten (met_id);




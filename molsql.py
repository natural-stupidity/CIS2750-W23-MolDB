# Michael Sirna
# 1094947
# 2023-09-10
# CIS2750 Assignment 4 Updated 2

import os
from os.path import exists
import random
import sqlite3
import MolDisplay

class Database():
    
    # The initialization method. If reset is true and the table exists, it deletes the old table
    # From there, it creates a new table
    def __init__(self, reset):
        if (reset and exists("molecules.db")):
            os.remove("molecules.db")
        self.conn = sqlite3.connect("molecules.db")


    # Creates all the tables. Pretty self explanatory
    def create_tables(self):
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements (
            ELEMENT_NO      INTEGER         NOT NULL,
            ELEMENT_CODE    VARCHAR(3)      PRIMARY KEY,
            ELEMENT_NAME    VARCHAR(32)     NOT NULL,
            COLOUR1         CHAR(6)         NOT NULL,
            COLOUR2         CHAR(6)         NOT NULL,
            COLOUR3         CHAR(6)         NOT NULL,
            RADIUS          DECIMAL(3)      NOT NULL)""" 
        )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Atoms (
            ATOM_ID         INTEGER         PRIMARY KEY    AUTOINCREMENT,
            ELEMENT_CODE    VARCHAR(3)      NOT NULL,
            X               DECIMAL(7, 4)   NOT NULL,
            Y               DECIMAL(7, 4)   NOT NULL,
            Z               DECIMAL(7, 4)   NOT NULL,
            FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements )""" 
        )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Bonds (
            BOND_ID         INTEGER     PRIMARY KEY        AUTOINCREMENT,
            A1              INTEGER     NOT NULL,
            A2              INTEGER     NOT NULL,
            EPAIRS          INTEGER     NOT NULL)""" 
        )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Molecules (
            MOLECULE_ID     INTEGER     PRIMARY KEY        AUTOINCREMENT,
            NAME            TEXT        NOT NULL           UNIQUE)""" 
        )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom (
            MOLECULE_ID     INTEGER     NOT NULL,
            ATOM_ID         INTEGER     NOT NULL,
            PRIMARY KEY     (MOLECULE_ID, ATOM_ID),
            FOREIGN KEY     (MOLECULE_ID) REFERENCES Molecules,
            FOREIGN KEY     (ATOM_ID)     REFERENCES Atoms)""" 
        )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond (
            MOLECULE_ID     INTEGER     NOT NULL,
            BOND_ID         INTEGER     NOT NULL,
            PRIMARY KEY     (MOLECULE_ID, BOND_ID),
            FOREIGN KEY     (MOLECULE_ID) REFERENCES Molecules,
            FOREIGN KEY     (BOND_ID)     REFERENCES Bonds)""" 
        )


    # Creates a new entry in the database.
    def __setitem__(self, table, values):

        # Creates a string of question marks for the query (looks like ?,?,...,?)
        value_marks = ",".join("?" * len(values))
        self.conn.executemany( "INSERT INTO " + table + " VALUES(" + value_marks  +")", [values])


    # Adds an atom to the Atoms table and MoleculeAtom table.
    def add_atom(self, molname, atom):

        a = (atom.element, atom.x, atom.y, atom.z)
        self.check_element(atom.element)
        self.conn.execute("INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z) VALUES(?, ?, ?, ?)", a)
        id = self.conn.execute("SELECT LAST_INSERT_ROWID()").fetchone()
        self.conn.execute("""INSERT INTO MoleculeAtom(MOLECULE_ID, ATOM_ID) VALUES((SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?), ?)""", (molname, id[0]))
        

    # Adds a bond to the Bonds table and MoleculeBond table.
    def add_bond(self, molname, bond):
        
        b = (bond.a1, bond.a2, bond.epairs)
        self.conn.execute("INSERT INTO Bonds(A1, A2, EPAIRS) VALUES(?, ?, ?)", b)
        id = self.conn.execute("SELECT LAST_INSERT_ROWID()").fetchone()
        self.conn.execute("""INSERT INTO MoleculeBond(MOLECULE_ID, BOND_ID) VALUES ((SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?), ?)""", (molname, id[0]))


    # Adds a molecule to the table given a name and a file.
    # It parses the file first into a string, the adds a molecule to the molecules table
    # before going through the string and adding each atom and bond.
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        isValid = mol.parse(fp)
        
        if (isValid == False):
            return False

        self.conn.execute("INSERT INTO Molecules (NAME) VALUES (?)", [name])
        for i in range(mol.atom_no):
            self.add_atom(name, mol.get_atom(i))
        for i in range(mol.bond_no):
            self.add_bond(name, mol.get_bond(i))

        #Reinitialize Stuff
        self.update_database()
        return True


    # Loads a molecule into as a mol object so it can be displayed as an SVG
    def load_mol(self, name):
        mol = MolDisplay.Molecule()

        # Combines the Atoms, MoleculeAtom, and Molecules table on their common elements
        # From there, we just need to grab what we need based on the name given.
        atom_info = self.conn.execute("SELECT ELEMENT_CODE, X, Y, Z FROM Atoms INNER JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID INNER JOIN Molecules ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID WHERE (Molecules.NAME = ?)", [name]).fetchall()
        bond_info = self.conn.execute("SELECT A1, A2, EPAIRS FROM Bonds INNER JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.BOND_ID INNER JOIN Molecules ON Moleculebond.MOLECULE_ID = Molecules.MOLECULE_ID WHERE (Molecules.NAME = ?)", [name]).fetchall()
        
        # Loop through the info given and append atoms and mols respectively.
        for i in atom_info:
            self.check_element(i[0])
            mol.append_atom(i[0], i[1], i[2], i[3])

        for i in bond_info:
            mol.append_bond(i[0], i[1], i[2])
            
        self.update_database()

        return mol
    
    # Returns a dictionary for molecules to update the molecule table.
    def get_mols(self):
        mols = self.conn.execute("""SELECT MOLECULE_ID, NAME FROM Molecules""").fetchall()
        molecule_list = []
        for mol in mols:
            molObj = self.load_mol(mol[1])
            molecule_list.append({"id": mol[0], "name": mol[1], "atom_count": molObj.atom_no, "bond_count": molObj.bond_no, "svg": molObj.svg()})
        return sorted(molecule_list, key=lambda d: d['id'])
        
    # Returns a array of dictionaries for molecules. Includes database id, name, atoms, bonds
    def get_elements(self):
        elements = self.conn.execute("""SELECT * FROM Elements""").fetchall()
        element_list = []
        for e in elements:
            atom_svg = """<svg width="100%%" height="100%%" style="margin: auto;">
                            <radialGradient id="%s-card" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                                <stop offset="0%%" stop-color="#%s"/>
                                <stop offset="50%%" stop-color="#%s"/>
                                <stop offset="100%%" stop-color="#%s"/>
                            </radialGradient>
                            <circle cx="50%%" cy="50%%" r="%d" fill="url(#%s-card)"/>
                        </svg>""" % (MolDisplay.element_name[e[1]], e[3], e[4], e[5], 
                                    e[6], MolDisplay.element_name[e[1]])

            element_list.append({"number": e[0], "symbol": e[1], "name": e[2], "c1": e[3], "c2" : e[4], "c3": e[5], "r": e[6], "svg": atom_svg})
        return sorted(element_list, key=lambda d: d['number'])

    def get_elements_from_codes(self, elements):
        value_marks = ",".join("?" * len(elements))
        d = self.conn.execute("SELECT * FROM Elements WHERE ELEMENT_CODE IN (" + value_marks  +")", elements).fetchall()
        return sorted(d)

    # Creates a dictionary from keys made of up element codes and values of the radius we want each element to be.
    def radius(self):
        d = {}
        data = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements").fetchall()
        d = {i[0] : i[1] for i in data}
        return d
    
    # Creates a dictionary from keys made of up element codes and values of the radius we want each element to be.
    def colours(self):
        d = {}
        data = self.conn.execute("SELECT ELEMENT_CODE, COLOUR1 FROM Elements").fetchall()
        d = {i[0] : i[1] for i in data}
        return d

    # Creates a dictionary from keys made up of element ids and values of element codes
    def element_codes(self):
        d = {}
        data = self.conn.execute("SELECT ELEMENT_NO, ELEMENT_CODE FROM Elements").fetchall()
        d = {i[0] : i[1] for i in data}
        return d
    
    # Creates a dictionary from keys made up of element codes and values of element names
    def element_name(self):
        d = {}
        data = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements").fetchall()
        d = {i[0] : i[1] for i in data}
        return d
        

    # Sets the colour of each element as a gradient so it looks more 3D.
    def radial_gradients(self):
        
        radial_gradient_svg = """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                                    <stop offset="0%%" stop-color="#%s"/>
                                    <stop offset="50%%" stop-color="#%s"/>
                                    <stop offset="100%%" stop-color="#%s"/>
                                </radialGradient>"""
        return_string = ""
        data = self.conn.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements").fetchall()
        for i in data:
            return_string += radial_gradient_svg % (str(i[0]),  str(i[1]),  str(i[2]),  str(i[3]))

        return return_string
    
    def update_database(self):
        MolDisplay.radius = self.radius()
        MolDisplay.colours = self.colours()
        MolDisplay.element_name = self.element_name()
        MolDisplay.header = """<svg version="1.1" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">"""
        MolDisplay.header += self.radial_gradients()

    def check_element( self, element_name ):
        if (element_name not in self.element_name()):
            c1 = "%06x" % random.randint(0, 0xFFFFFF)
            c1RGB = []
            for i in (0, 2, 4):
                decimal = int(int(c1[i:i+2], 16) - (int(c1[i:i+2], 16) * 0.75))
                c1RGB.append(decimal)
            c2 =  "%02x%02x%02x" % (c1RGB[0], c1RGB[1], c1RGB[2])
            self.conn.execute("INSERT INTO Elements VALUES(?, ?, ?, ?, ?, ?, ?)", ( 0, element_name, element_name, c1, c2, "000000", 30))

    def reset_elements(self):
        self.conn.execute("DELETE FROM Elements")
        self.set_default_elements()

    def set_default_elements(self):
        self["Elements"] = ( 1, "H", "Hydrogen", "FFFFFF", "050505", "020202", 25 )
        self["Elements"] = ( 6, "C", "Carbon", "808080", "010101", "000000", 40 )
        self["Elements"] = ( 7, "N", "Nitrogen", "0000FF", "000005", "000002", 40 )
        self["Elements"] = ( 8, "O", "Oxygen", "FF0000", "050000", "020000", 40 )
        self["Elements"] = ( 9, "F", "Fluorine", "FFA500", "0F0A00", "020100", 40 )
        self["Elements"] = ( 15, "P", "Phosphorus", "8E77D1", "171321", "040305", 40 )
        self["Elements"] = ( 16, "S", "Sulphur", "FFFF00", "050500", "020200", 40 )
        self["Elements"] = ( 17, "Cl", "Chlorine", "008000", "001F00", "000000", 40 )
        self["Elements"] = ( 35, "Br", "Bromine", "5C4033", "1F1511", "030201", 40 )
        self["Elements"] = ( 53, "I", "Iodine", "311465", "180C1A", "0E070f", 40 )

    def resetDatabase():
        if (exists("molecules.db")):
            os.remove("molecules.db")


        
# Michael Sirna
# 1094947
# 2023-09-10
# CIS2750 Assignment 4 Updated 2

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import MolDisplay
import molsql
import json

PORT = 54947

class Handler(BaseHTTPRequestHandler):

    db = molsql.Database(reset=True)
    db.create_tables()
    db.set_default_elements()
    
    MolDisplay.radius = db.radius()
    MolDisplay.colours = db.colours()
    MolDisplay.element_name = db.element_name()
    MolDisplay.header += db.radial_gradients()

    def do_GET(self):
        if (self.path == "/"):
            fp = open("./static/index.html")
            main_page = fp.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(main_page))
            self.end_headers()
            self.wfile.write(bytes(main_page, "UTF-8"))

        elif (self.path == "/molecule-list.html"):
            stored_mols = self.db.get_mols()
            molecules_list = json.dumps(stored_mols, indent=4)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(molecules_list))
            self.end_headers()
            self.wfile.write(bytes(molecules_list, "UTF-8"))

        elif (self.path == "/element-list.html"):
            stored_elems = self.db.get_elements()
            element_list = json.dumps(stored_elems, indent=4)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(element_list))
            self.end_headers()
            self.wfile.write(bytes(element_list, "UTF-8"))

        elif (self.path.startswith("/static/")):
            if (self.path.endswith(".js")):
                mimetype = "text/javascript"
            elif (self.path.endswith(".css")):
                mimetype = "text/css"
            elif (self.path.endswith(".png") or self.path.endswith(".jpg") or self.path.endswith(".jpeg")):
                mimetype = "image/jpeg"
            elif (self.path.endswith(".ico")):
                mimetype = "image/x-icon"

            with open("." + self.path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            self.wfile.write(content)

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("404: not found", "UTF-8"))

    def do_POST(self):
        if (self.path == "/add-element"):

            data = self.rfile.read(int(self.headers["Content-Length"]))
            new_elem_data = json.loads(data.decode("UTF-8"))

            id = new_elem_data["id"]
            symbol = new_elem_data["symbol"]
            element = new_elem_data["element"]
            colour1 = new_elem_data["colour1"]
            colour2 = new_elem_data["colour2"]
            colour3 = new_elem_data["colour3"]
            radius = new_elem_data["radius"]

            temp_dict = self.db.element_codes()
            if (int(id) != 0 and temp_dict and (int(id) in temp_dict) or (symbol in temp_dict.values())):
                conflict = ""
                if (int(id) in temp_dict):
                    conflict = "ID '" + id + "'"
                if (symbol in temp_dict.values()):
                    conflict = "symbol '" + symbol + "'"
                if ((int(id) in temp_dict) and (symbol in temp_dict.values())):
                    conflict = "ID '" + id + "' and symbol '" + symbol + "'"
                
                self.send_response(409)  # Conflict if it already exists
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(conflict))
                self.end_headers()
                self.wfile.write(bytes(str(conflict), "UTF-8"))
                return

            self.db["Elements"] = (id, symbol, element, colour1, colour2, colour3, radius)

            # Reinitialize Stuff
            self.db.update_database()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        if (self.path == "/edit-element"):

            data = self.rfile.read(int(self.headers["Content-Length"]))
            new_elem_data = json.loads(data.decode("UTF-8"))

            old_symbol = new_elem_data["oldSymbol"]
            id = new_elem_data["id"]
            symbol = new_elem_data["symbol"]
            element = new_elem_data["element"]
            colour1 = new_elem_data["colour1"]
            colour2 = new_elem_data["colour2"]
            colour3 = new_elem_data["colour3"]
            radius = new_elem_data["radius"]

            temp_dict = self.db.element_codes()
            conflict_bool = False
            conflict = ""
            if (int(id) != 0 and temp_dict and (int(id) in temp_dict) and temp_dict[int(id)] != old_symbol):
                conflict_bool = True
                conflict = "ID '" + id + "'"
            
            if (temp_dict and old_symbol != symbol and (symbol in temp_dict.values())):
                if (conflict_bool == True):
                    conflict += "' and symbol '" + symbol + "'"
                else:
                    conflict_bool = True
                    conflict = "symbol '" + symbol + "'"
                
            if (conflict_bool):
                self.send_response(409)  # Conflict if it already exists
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(conflict))
                self.end_headers()
                self.wfile.write(bytes(str(conflict), "UTF-8"))
                return

            self.db.conn.execute(
                f" UPDATE Elements SET ELEMENT_NO=?, ELEMENT_CODE=?, ELEMENT_NAME=?, COLOUR1=?, COLOUR2=?, COLOUR3=?, RADIUS=? WHERE ELEMENT_CODE=?",
                (id, symbol, element, colour1, colour2, colour3, radius, old_symbol),
            )

            # Reinitialize Stuff
            self.db.update_database()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/delete-element"):
            data = self.rfile.read(int(self.headers["Content-Length"]))
            deleteElement = str(repr(data.decode("UTF-8")))
            self.db.conn.execute(f" DELETE FROM Elements WHERE ELEMENT_CODE={deleteElement}")

            # Reinitialize Stuff
            self.db.update_database()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/add-molecule"): 
            data = self.rfile.read(int(self.headers["Content-Length"]))
            molecule_data = json.loads(data.decode("UTF-8"))
            file_data = molecule_data["file"]
            molecule_name = molecule_data["molecule-name"]

            molecule_exists = self.db.conn.execute(f" SELECT NAME FROM Molecules WHERE Molecules.NAME='{molecule_name}'").fetchone()

            if (molecule_exists != None):
                self.send_response(409)  # Conflict if it already exists
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return

            else:
                fp = open("./temp.txt", "wb")
                fp.write(bytes(file_data, "UTF-8"))
                fp.close()

                fp = open("./temp.txt")
                isValid = self.db.add_molecule(molecule_name, fp)
                fp.close()
                os.remove("./temp.txt")
                if (isValid == False):
                    self.send_response(406)  # Not Acceptable if .sdf is not valid
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return

                mol = self.db.load_mol(molecule_name)
                svg = mol.svg()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(svg))
                self.end_headers()
                self.wfile.write(bytes(svg, "UTF-8"))

        elif (self.path == "/view-molecule"):

            data = self.rfile.read(int(self.headers["Content-Length"]))

            molecule_name = str(repr(data.decode("UTF-8")))
            molecule_name = molecule_name.strip("'")
            molecule_name = molecule_name.strip('"')

            mol = self.db.load_mol(molecule_name)
            svg = mol.svg()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(svg))

            self.end_headers()
            self.wfile.write(bytes(svg, "UTF-8"))

        elif (self.path == "/mol-info.html"):

            data = self.rfile.read(int(self.headers["Content-Length"]))
            molecule_name = data.decode("UTF-8")
            temp_mol = self.db.load_mol(molecule_name)

            temp_dict = {}
            elements = []

            for i in range(temp_mol.atom_no):
                a = temp_mol.get_atom(i)
                numberRepresentation = 0
                if (a.element not in elements):
                    elements.append(a.element)
                for j in a.element:
                    numberRepresentation += ord(j)

                temp_dict[numberRepresentation] = a.element

            keys = list(temp_dict.keys())
            keys.sort()
            sorted_dict = {i: temp_dict[i] for i in keys}
            nomenclature = dict.fromkeys(sorted_dict.values(), 0)

            for k in range(temp_mol.atom_no):
                a = temp_mol.get_atom(k)
                nomenclature[a.element] = nomenclature[a.element] + 1

            nomen_string = ""
            for l in nomenclature:
                nomen_string += l
                if nomenclature[l] != 1:
                    nomen_string += "<sub>" + str(nomenclature[l]) + "</sub>"
            
            temp_data = { "name": molecule_name, "nomenclature" : nomenclature, "nomenString": nomen_string, "numAtoms":temp_mol.atom_no, "numBonds": temp_mol.bond_no, "elements": self.db.get_elements_from_codes(elements) }
            data = json.dumps(temp_data, indent=4)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(data))
            self.end_headers()
            self.wfile.write(bytes(data, "UTF-8"))

        elif (self.path == "/edit-molecule"):

            data = self.rfile.read(int(self.headers["Content-Length"]))
            molecule_data = json.loads(data.decode("UTF-8"))
            old_name = molecule_data["oldName"]
            new_name = molecule_data["newName"]
            molecule_exists = self.db.conn.execute(f" SELECT NAME FROM Molecules WHERE Molecules.NAME='{new_name}'").fetchone()
            
            if (old_name != new_name and molecule_exists != None):
                self.send_response(409)  # Conflict if it already exists
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return

            self.db.conn.execute(f" UPDATE Molecules SET NAME=? WHERE NAME=?", (new_name, old_name))

            # Reinitialize Stuff
            self.db.update_database()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/delete-molecule"):

            data = self.rfile.read(int(self.headers["Content-Length"]))
            molecule_name = str(repr(data.decode("UTF-8")))
            molecule_id = self.db.conn.execute(f" SELECT MOLECULE_ID FROM Molecules WHERE NAME={molecule_name}").fetchone()
            atom_ids = self.db.conn.execute(f" SELECT ATOM_ID FROM MoleculeAtom WHERE MOLECULE_ID={molecule_id[0]}").fetchall()
            bond_ids = self.db.conn.execute(f" SELECT BOND_ID FROM MoleculeBond WHERE MOLECULE_ID={molecule_id[0]}").fetchall()
            for atom in atom_ids:
                self.db.conn.execute(f" DELETE FROM Atoms WHERE ATOM_ID={atom[0]}")
            
            for bond in bond_ids:
                self.db.conn.execute(f" DELETE FROM Bonds WHERE BOND_ID={bond[0]}")
            self.db.conn.execute(f" DELETE FROM Molecules WHERE MOLECULE_ID={molecule_id[0]}")
            self.db.conn.execute(f" DELETE FROM MoleculeAtom WHERE MOLECULE_ID={molecule_id[0]}")
            self.db.conn.execute(f" DELETE FROM MoleculeBond WHERE MOLECULE_ID={molecule_id[0]}")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/get-rotations"):
            data = self.rfile.read(int(self.headers["Content-Length"]))
            molecule_name = str(repr(data.decode("UTF-8")))
            molecule_name = molecule_name.strip("'")
            molecule_name = molecule_name.strip('"')

            temp_mol = self.db.load_mol(molecule_name)

            raw_rotations = temp_mol.get_rotations()
            rotations_list = json.dumps(raw_rotations, indent=4)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(rotations_list))

            self.end_headers()
            self.wfile.write(bytes(rotations_list, "UTF-8"))

        elif (self.path == "/reset-elements"):
            self.db.reset_elements()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/delete-all-elements"):
            self.db.conn.execute("DELETE FROM Elements")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/delete-all-molecules"):
            self.db.conn.execute(f" DELETE FROM Bonds")
            self.db.conn.execute(f" DELETE FROM Atoms")
            self.db.conn.execute(f" DELETE FROM Molecules")
            self.db.conn.execute(f" DELETE FROM MoleculeAtom")
            self.db.conn.execute(f" DELETE FROM MoleculeBond")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif (self.path == "/get-svg-mode"):
            temp_mode = str(MolDisplay.svgMode)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(temp_mode))
            self.end_headers()
            self.wfile.write(bytes(temp_mode, "UTF-8"))

        elif (self.path == "/change-svg-mode"):
            data = self.rfile.read(int(self.headers["Content-Length"]))
            new_mode = str(repr(data.decode("UTF-8")))
            new_mode = new_mode.strip("'")
            new_mode = new_mode.strip('"')
            MolDisplay.svgMode = int(new_mode)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("404: not found", "UTF-8"))


httpd = HTTPServer(("localhost", PORT), Handler)
print(f"Server running on http://localhost:{PORT}")
httpd.serve_forever()

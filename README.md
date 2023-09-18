# CIS 2750 W23 Molecule Project
##### Year: 2023
This project was made for CIS\*2750 (Software Systems Development and Integration) at the University of Guelph.

The program takes uploaded .SDF files and then parses, stores, and then creates and displays an SVG image to the user. Users can then rotate, spin, or change the appearance of the molecule as much as they want.

## Technical Details:
**Front End:** HTML, CSS, JavaScript, and jQuery<br/>
**Back End:** C, Python, Swig, and SQLite

Note: The swig file used (*molecule.i*) was created by Professor Kremer. You will need Swig in order to run the program.

## How to Run:
1. Load the project into an IDE, and run:
```
make
```
The expected output should be:
```
clang -Wall -std=c99 -pedantic -c mol.c -fPIC -o mol.o
clang mol.o -shared -o libmol.so
swig -python molecule.i
clang -Wall -std=c99 -pedantic -c molecule_wrap.c -fPIC -I/usr/include/python3.11 -o molecule_wrap.o
clang -Wall -std=c99 -pedantic molecule_wrap.o -shared -L. -lmol -L/usr/lib/python3.11/config-3.11-x86_64-linux-gnu -lmol -dynamiclib -o _molecule.so
clang: warning: argument unused during compilation: '-dynamiclib' [-Wunused-command-line-argument]
````
Note that the clang warning should be ignored as one of the requirements for the project was to use the -dynamiclib line in the makefile, and it doesn't affect the program at all.

2. You need export the library path of the program which can be done by entering:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/libmol.so
```
3. After that, you can run the program using:
```
python3 server.py
```
The program will run on localhost:54947

## [![Click here for a video demonstration](https://msirna.github.io/static/img/detailsImages/moldb/MolDB%20Presentation.mp4)](https://msirna.github.io/static/img/detailsImages/moldb/MolDB%20Presentation.mp4)

## Screenshots:

*The front page without any molecules.*
![Screenshot 2023-09-13 164745](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/e91bbe34-8cd6-43cf-bd9a-515cdfb22b06)

*The elements menu with the default elements.*
![Screenshot 2023-09-13 164804](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/9775c29b-173e-4f48-ba6e-235f5a234600)

*The settings menu.*
![Screenshot 2023-09-13 164823](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/d4da771a-8331-4f03-9416-4554d6131cde)

*A Caffeine molecule being shown in the editor using the new nightmare SVG mode.*
![Screenshot 2023-09-13 164857](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/181bdfa9-246c-417f-87ba-a79ed2d96d7f)

*A Caffeine molecule being shown in the editor using the original nightmare SVG mode.*
![Screenshot 2023-09-13 164920](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/85266098-961b-4c97-b9d8-4fe9470144c8)

*A Caffeine molecule being shown in the editor using the non-nightmare SVG mode.*
![Screenshot 2023-09-13 164939](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/00db069a-b019-4052-8dad-809234223354)

*The front page with some example molecules.*
![Screenshot 2023-09-13 165108](https://github.com/mSirna/W23-CIS2750-MolDB/assets/91761269/0dbf32fd-f3ab-4f95-9dd1-6000b7d233a8)




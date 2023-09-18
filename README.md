# CIS 2750 W23 Molecule Project
### Year: 2023
This project was made for CIS\*2750 (Software Systems Development and Integration) at the University of Guelph.

The program takes uploaded .SDF files and then parses, stores, and then creates and displays an SVG image to the user. Users can then rotate, spin, or change the appearance of the molecule as much as they want.

This is an updated version of the app that I worked on throughout the Summer because I was disappointed in how the original project turned out (Although it was complete to specification), and I wanted to see if I could figure out Dr. Kremer's "Nightmare Mode". This version not only has Nightmare mode added, but a ton of other features that were not present in the original.

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

## [![Video Demo](https://msirna.github.io/static/videos/MolDB%20Demo.mp4)

## Screenshots:

*The front page without any molecules.*

*The elements menu with the default elements.*

*The settings menu.*

*A Caffeine molecule being shown in the editor using the new nightmare SVG mode.*

*A Caffeine molecule being shown in the editor using the original nightmare SVG mode.*

*A Caffeine molecule being shown in the editor using the non-nightmare SVG mode.*

*The front page with some example molecules.*




// Michael Sirna
// 1094947
// 2023-09-10
// CIS2750 Assignment 4 Updated 2

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Definitions
#ifndef M_PI
    #define M_PI 3.14159265358979323846264338327950288
#endif
#define ONE_DEGREE M_PI / 180

#ifndef _MOL_H_
#define _MOL_H_

// Structs
typedef struct atom {
    char element[3];
    double x, y, z;
} atom;

typedef struct bond {
    unsigned short a1, a2;
    unsigned char epairs;
    atom *atoms;
    double x1, x2, y1, y2, z, len, len2D, dx, dy;
} bond;

typedef struct molecule {
    unsigned short atom_max, atom_no;
    atom *atoms, **atom_ptrs;
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
} molecule;

typedef double xform_matrix[3][3];

typedef struct mx_wrapper {
    xform_matrix xform_matrix;
} mx_wrapper;


// Function Declarations / Prototypes

/** Takes an atom and sets it's element array, x, y, and z values based on values passed through it.
 *
 *  @param a - the pointer of the atom whose values we are setting.
 *  @param element - the element array that we want our atom to have.
 *  @param x - the pointer of the x value that we want our atom to have.
 *  @param y - the pointer of the y value that we want our atom to have.
 *  @param z - the pointer of the z value that we want our atom to have.
 */
void atomset(atom *a, char element[3], double *x, double *y, double *z);

/** The opposite of atomset; takes an element array, x, y, and z values and sets them to the values in the given atom.
 *
 *  @param a - the pointer of the atom whose values we will be copying.
 *  @param element - the element array that will be set to a->element.
 *  @param x - the pointer of the x value that will be set to a->x.
 *  @param y - the pointer of the y value that will be set to a->y.
 *  @param z - the pointer of the z value that will be set to a->z.
 */
void atomget(atom *a, char element[3], double *x, double *y, double *z);

/** Takes a bond and sets its atoms and electron-pairs based on values passed through it.
 *
 *  @param b - the pointer of the bond whose values we are setting.
 *  @param a1 - the pointer of indicies of the first atom
 *  @param a2 - the pointer of indicies of the second atom
 *  @param atoms - the double pointer of the atom array.
 *  @param epairs - the electron-pairs of the atoms in the bond.
 */
void bondset(bond *b, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

/** The opposite of bondset; takes two atoms and electron-pairs and sets them to the values in a given bond.
 *
 *  @param b - the pointer of the bond whose values we are copying.
 *  @param a1 - the pointer of indicies of the first atom that will be set to b->a1.
 *  @param a2 - the pointer of indicies of the second atom that will be set to b->a2.
 *  @param atoms - the double pointer of the atom array  that will be set to b->atoms.
 *  @param epairs - the pointer electron-pairs that will be set to b->epairs
 */
void bondget(bond *b, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);


/**  Methods that get the respective atoms in a bond.
 *
 *  @param b - the pointer of the bond where we will get A1 or A2 from.
 */
atom* getA1(bond* b);
atom* getA2(bond* b);

/** Takes a bond and calculates and assigns its atoms x, y, and z.
 *  Also calculates len, len2D, dx, and dy.
 *
 * @param b - The bond that we will use to assign values.
 */
void compute_coords(bond *b);

/** Creates and initializes a new molecule..
 *
 *  @param atom_max - The maximum amount of atoms that the molecule will have.
 *  @param bond_max - The maximum amount of bonds that the molecule will have.
 *
 *  @returns The memory address of the new molecule.
 */
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);

/** Copies values from one molecule and uses molmalloc to create and store those values into a new molecule.
 *
 *  @param src - The pointer of the molecule that we want to copy values from.
 *
 *  @returns The memory address of the new molecule if successfull; NULL if not-successful.
 */
molecule *molcopy(molecule *src);

/** Frees all the memory associated to a pointer (i.e. atoms, atom_ptrs, bonds, bond_ptrs, then the molecule).
 *
 *  @param ptr - The pointer of the molecule that we are going to free.
 */
void molfree(molecule *ptr);

/** Copies data from an atom into the first empty atom slot in the molecule.
 *  Increases the atom max and reallocates atom and atom_ptr size if necessary.
 *  Returns if reallocation failed.
 *
 *  @param mol - The pointer of the molecule that we will put the atom into.
 *  @param a - The pointer of the atom that we will copy data from.
 */
void molappend_atom(molecule *mol, atom *a);

/** Copies data from a bond into the first empty bond slot in the molecule.
 *  Increases the bond max and reallocates bond and bond_ptr size if necessary.
 *  Returns if reallocation failed.
 *
 *  @param mol - The pointer of the molecule that we will put the atom into.
 *  @param b - The pointer of the bond that we will copy data from.
 */
void molappend_bond(molecule *mol, bond *b);

/** Atom comparison function for molsort (which uses qsort).
 *  Compares the z-values between two atoms.
 *
 *  @param a - The The pointer of the first atom.
 *  @param b - The The pointer of the second atom.
 *
 *  @returns 0 if a == b, < 0 if the a < b, > 0 if the a > b.
 */
int atom_comp(const void *a, const void *b);

/** Bond comparison function for molsort (which uses qsort).
 *  Compares the average z-values between two bonds.
 *
 *  @param a - The pointer of the first bond.
 *  @param b - The pointer of the second bond.
 *
 *  @returns 0 if a == b, < 0 if the a < b, > 0 if the a > b.
 */
int bond_comp(const void *a, const void *b);

/** Sorts atom_ptrs and bond_ptrs in increasing order.
 *  Uses qsort and the atomCompare and bondCompare functions.
 *
 *  @param m - The pointer of the molecule that will have its atom_ptrs and bond_ptrs sorted.
 */
void molsort(molecule *m);

/** Sets the values of a matrix based on x-axis rotation.
 *  @link https://en.wikipedia.org/wiki/Rotation_matrix
 *
 *  @param matrix - The matrix that we will rotate on the x-axis.
 *  @param degrees - The amount of degrees we will rotate by.
 */
void xrotation(xform_matrix matrix, unsigned short degrees);

/** Sets the values of a matrix based on y-axis rotation.
 *  @link https://en.wikipedia.org/wiki/Rotation_matrix
 *
 *  @param matrix - The matrix that we will rotate on the y-axis.
 *  @param degrees - The amount of degrees we will rotate by.
 */
void yrotation(xform_matrix matrix, unsigned short degrees);

/** Sets the values of a matrix based on z-axis rotation.
 *  @link https://en.wikipedia.org/wiki/Rotation_matrix
 *
 *  @param matrix - The matrix that we will rotate on the z-axis.
 *  @param degrees - The amount of degrees we will rotate by.
 */
void zrotation(xform_matrix matrix, unsigned short degrees);

/** Applies rotations to a molecule through matrix multiplication.
 *
 * @param mol - The pointer of the molecule we want to rotate.
 * @param matrix - The matrix with transformations applied to it.
 */
void mol_xform(molecule *molecule, xform_matrix matrix);

#endif

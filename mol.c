// Michael Sirna
// 1094947
// 2023-09-10
// CIS2750 Assignment 4 Updated 2

#include "mol.h"

void atomset(atom *a, char element[3], double *x, double *y, double *z) {
    strncpy(a->element, element, 3);
    a->x = *x;
    a->y = *y;
    a->z = *z;
}

void atomget(atom *a, char element[3], double *x, double *y, double *z) {
    strncpy(element, a->element, 3);
    *x = a->x;
    *y = a->y;
    *z = a->z;
}

void bondset(bond *b, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs) {
    b->a1 = *a1;
    b->a2 = *a2;
    b->atoms = *atoms;
    b->epairs = *epairs;
    compute_coords(b);
}

void bondget(bond *b, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs) {
    *a1 = b->a1;
    *a2 = b->a2;
    *atoms = b->atoms;
    *epairs = b->epairs;
}

atom* getA1(bond* b){
	return &(b->atoms[b->a1]);
}

atom* getA2(bond* b){
	return &(b->atoms[b->a2]);
}

void compute_coords(bond *b) {
    atom *a1 = &b->atoms[b->a1];
    atom *a2 = &b->atoms[b->a2];

    b->x1 = a1->x;
    b->y1 = a1->y;
    b->x2 = a2->x;
    b->y2 = a2->y;
    b->z = (a1->z + a2->z) / 2;
    b->len = sqrt(pow(a2->x - a1->x, 2) + pow(a2->y - a1->y, 2) + pow(a2->z - a1->z, 2));
    b->len2D = sqrt(pow(a2->x - a1->x, 2) + pow(a2->y - a1->y, 2));
    b->dx = (a2->x - a1->x) / b->len2D;
    b->dy = (a2->y - a1->y) / b->len2D;
}

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
    molecule *newMolecule = (molecule *)malloc(sizeof(molecule));
    if (!newMolecule) {
        fprintf(stderr, "molmalloc: Allocation failed.\n");
        return NULL;
    }
    newMolecule->atom_max = atom_max;
    newMolecule->bond_max = bond_max;
    newMolecule->atom_no = 0;
    newMolecule->bond_no = 0;
    newMolecule->atoms = malloc(atom_max * sizeof(atom));
    newMolecule->atom_ptrs = malloc(atom_max * sizeof(atom *));
    newMolecule->bonds = malloc(bond_max * sizeof(bond));
    newMolecule->bond_ptrs = malloc(bond_max * sizeof(bond *));

    // Before we return, we have to make sure nothing is null. If it is, we have to free stuff and return null.
    if (newMolecule->atoms == NULL || newMolecule->atom_ptrs == NULL || newMolecule->bonds == NULL || newMolecule->bond_ptrs == NULL) {
        free(newMolecule);
        if (newMolecule->atoms != NULL) free(newMolecule->atoms);
        if (newMolecule->atom_ptrs != NULL) free(newMolecule->atom_ptrs);
        if (newMolecule->bonds != NULL) free(newMolecule->bonds);
        if (newMolecule->bond_ptrs != NULL) free(newMolecule->bond_ptrs);
        fprintf(stderr, "molmalloc: Allocation failed.\n");
        return NULL;
    }
    return newMolecule;
}

molecule *molcopy(molecule *src) {
    // We first allocate memory and copy values over.
    molecule *dst = molmalloc(src->atom_max, src->bond_max);
    dst->atom_max = src->atom_max;
    dst->bond_max = src->bond_max;

    // Add atoms and bonds to the molecule.
    for (int i = 0; i < src->atom_no; i++) {
        molappend_atom(dst, &src->atoms[i]);
    }
    for (int j = 0; j < src->bond_no; j++) {
        molappend_bond(dst, &src->bonds[j]);
    }
    return dst;
}

void molfree(molecule *ptr) {
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
    ptr = NULL;
}

void molappend_atom(molecule *mol, atom *a) {
    // First, check if we need to increase the number of atoms.
    // If we do, reallocate the atoms and atom_ptrs. If either one is null, return.
    // If successful, assign the atom_ptrs to the proper atoms.
    if (mol->atom_max == 0 || mol->atom_no >= mol->atom_max) {
        if (mol->atom_max == 0)
            mol->atom_max = 1;
        else
            mol->atom_max *= 2;

        mol->atoms = realloc(mol->atoms, mol->atom_max * sizeof(*a));
        mol->atom_ptrs = realloc(mol->atom_ptrs, mol->atom_max * sizeof(*a));
        if (mol->atoms == NULL || mol->atom_ptrs == NULL) {
            if (mol->atoms != NULL) free(mol->atoms);
            fprintf(stderr, "molappend_atom: Reallocation failed.\n");
            return;
        }
        for (int i = 0; i < mol->atom_no; i++) {
            mol->atom_ptrs[i] = &mol->atoms[i];
        }
    }
    // Setting the first empty slots to atoms and atom_ptrs.
    atomset(mol->atoms + mol->atom_no, a->element, &a->x, &a->y, &a->z);
    mol->atom_ptrs[mol->atom_no] = &(mol->atoms[mol->atom_no]);
    mol->atom_no++;
}

void molappend_bond(molecule *mol, bond *b) {
    // First, check if we need to increase the number of bonds.
    // If we do, reallocate the bonds and bond_ptrs. If either one is null, return.
    // If successful, assign the bond_ptrs to the proper bonds.
    if (mol->bond_max == 0 || mol->bond_no >= mol->bond_max) {
        if (mol->bond_max == 0)
            mol->bond_max = 1;
        else
            mol->bond_max *= 2;

        mol->bonds = realloc(mol->bonds, mol->bond_max * sizeof(*b));
        mol->bond_ptrs = realloc(mol->bond_ptrs, mol->bond_max * sizeof(*b));
        if (mol->bonds == NULL || mol->bond_ptrs == NULL) {
            if (mol->bonds != NULL) free(mol->bonds);
            fprintf(stderr, "molappend_bond: Reallocation failed.\n");
            return;
        }

        for (int i = 0; i < mol->bond_no; i++) {
            mol->bond_ptrs[i] = &mol->bonds[i];
        }
    }

    // Setting the first empty slots to bonds and bond_ptrs.
    bondset(mol->bonds + mol->bond_no, &b->a1, &b->a2, &b->atoms, &b->epairs);
    mol->bond_ptrs[mol->bond_no] = &(mol->bonds[mol->bond_no]);
    mol->bond_no++;
}

int atom_comp(const void *a, const void *b) {
    atom *a1 = (atom *)a;
    atom *a2 = (atom *)b;

    return a1->z - a2->z;
}

int bond_comp(const void *a, const void *b) {
    bond *b1 = (bond *)a;
    bond *b2 = (bond *)b;

    return b1->z - b2->z;
}

void molsort(molecule *mol) {
    qsort(mol->atom_ptrs, mol->atom_no, sizeof(atom *), atom_comp);
    qsort(mol->bond_ptrs, mol->bond_no, sizeof(bond *), bond_comp);
}

void xrotation(xform_matrix matrix, unsigned short degrees) {
    // Set a temporaryMatrix to the rotation matrix formula for x-rotation.
    xform_matrix tempMatrix = {
        {1, 0,                         0                         },
        {0, cos(degrees * ONE_DEGREE), -sin(degrees * ONE_DEGREE)},
        {0, sin(degrees * ONE_DEGREE), cos(degrees * ONE_DEGREE) }
    };
    // Use memcpy to copy the tempMatrix over to the original matrix.
    memcpy(matrix, tempMatrix, sizeof(xform_matrix));
}

void yrotation(xform_matrix matrix, unsigned short degrees) {
    // Set a temporaryMatrix to the rotation matrix formula for y-rotation.
    xform_matrix tempMatrix = {
        {cos(degrees * ONE_DEGREE),  0, sin(degrees * ONE_DEGREE)},
        {0,                          1, 0                        },
        {-sin(degrees * ONE_DEGREE), 0, cos(degrees * ONE_DEGREE)}
    };
    // Use memcpy to copy the tempMatrix over to the original matrix.
    memcpy(matrix, tempMatrix, sizeof(xform_matrix));
}

void zrotation(xform_matrix matrix, unsigned short degrees) {
    // Set a temporaryMatrix to the rotation matrix formula for z-rotation.
    xform_matrix tempMatrix = {
        {cos(degrees * ONE_DEGREE), -sin(degrees * ONE_DEGREE), 0},
        {sin(degrees * ONE_DEGREE), cos(degrees * ONE_DEGREE),  0},
        {0,                         0,                          1}
    };
    // Use memcpy to copy the tempMatrix over to the original matrix.
    memcpy(matrix, tempMatrix, sizeof(xform_matrix));
}

void mol_xform(molecule *molecule, xform_matrix matrix) {
    // Set up temporary variables
    double tempX, tempY, tempZ;

    // Loop through the molecules atoms and apply the transformations in the matrix to each coordinate.
    for (int i = 0; i < molecule->atom_no; i++) {
        atom *a = &molecule->atoms[i];
        tempX = a->x, tempY = a->y, tempZ = a->z;
        a->x = matrix[0][0] * tempX + matrix[0][1] * tempY + matrix[0][2] * tempZ;
        a->y = matrix[1][0] * tempX + matrix[1][1] * tempY + matrix[1][2] * tempZ;
        a->z = matrix[2][0] * tempX + matrix[2][1] * tempY + matrix[2][2] * tempZ;
    }

    for (int i = 0; i < molecule->bond_no; i++) {
        compute_coords(&molecule->bonds[i]);
    }
}

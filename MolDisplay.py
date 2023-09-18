# Michael Sirna
# 1094947
# 2023-09-10
# CIS2750 Assignment 4 Updated 2

import itertools
import math
import molecule

header = """<svg version="1.1" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500
svgMode = 1

class Atom():
    # Initializes an atom and its z-value.
    def __init__(self, a):
        self.atom = a 
        self.z = a.z

    # A method that prints out the atom's info for debugging
    def __str__(self):
        return """Element: %s, x: %f, y: %f, z: %f""" % (self.atom.element, self.atom.x,  self.atom.y,  self.atom.z)

    # A method that returns the formatting for the the atom / what the atom will look like in the svg.
    # Atoms will appear as circles, and their center, size, and colour is set through this.
    def svg(self):
        cx = (self.atom.x * 100) + offsetx
        cy = (self.atom.y * 100) + offsety
        r = radius[self.atom.element]
        colour = element_name[self.atom.element]
        return """ <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n""" % (cx, cy, r, colour)


class Bond():
    bid = itertools.count(start=1)

    # Inititalizes a bond and its z-values
    def __init__(self, b):
        self.bond = b
        self.z = b.z
        self.id = next(Bond.bid)

    # A method that prints out the bond's info for debugging.
    def __str__(self):
        return """a1: %d, a2: %d, e-pairs: %d, x1: %f ,x2: %f, y1: %f, y2: %f, z: %f, len: %f, dx: %f, dy: %f""" % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.x2, self.bond.y1, self.bond.y2, self.bond.z, self.bond.len, self.bond.dx, self.bond.dy)

    # The original, non-nightmare SVG mode. It just draws a green line between atoms.
    # The variables 1-4 define the points of each corner of the rectangle that makes up the bond
    # The gradientVersion is the one I demonstrated to Dr. Kremer. It's not nightmare mode, but it makes a gradient so it's not just green.
    def original_svg(self, gradientVersion = False):

        x1 = (self.bond.x1 * 100 + offsetx) + self.bond.dy * 10
        y1 = (self.bond.y1 * 100 + offsety) - self.bond.dx * 10

        x2 = (self.bond.x1 * 100 + offsetx) - self.bond.dy * 10
        y2 = (self.bond.y1 * 100 + offsety) + self.bond.dx * 10

        x3 = (self.bond.x2 * 100 + offsetx) - self.bond.dy * 10
        y3 = (self.bond.y2 * 100 + offsety) + self.bond.dx * 10

        x4 = (self.bond.x2 * 100 + offsetx) + self.bond.dy * 10
        y4 = (self.bond.y2 * 100 + offsety) - self.bond.dx * 10

        if (gradientVersion):
            bid = "bond" + str(self.id)
            gradCoords = (x1, y1, x2, y2)

            if (y1 > y2):
                gradCoords = (x2, y2, x1, y1)

            return """  
                <linearGradient xmlns="http://www.w3.org/2000/svg" id="%s" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" gradientUnits="userSpaceOnUse">
                    <stop offset="0%%" stop-color="#454545"/>
                    <stop offset="25%%" stop-color="#606060"/>
                    <stop offset="50%%" stop-color="#454545"/>
                    <stop offset="100%%" stop-color="#252525"/>
                </linearGradient>
                <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="url(#%s)"/>\n
            """ % (bid, gradCoords[0], gradCoords[1], gradCoords[2], gradCoords[3],
                x1, y1, x2, y2, x3, y3, x4, y4, bid) 
        
        return """<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n""" % (x1, y1, x2, y2, x3, y3, x4, y4) 
            
    
    # The original nightmare mode svg method for bonds. Draws them exactly as Dr.Kremer's example.
    def nightmare_mode_svg(self):
        bid = self.id
        bondWidth = 15
        atom1 = Atom(molecule.getA1(self.bond)).atom
        atom2 = Atom(molecule.getA2(self.bond)).atom
        radiusA1 = radius[atom1.element]
        radiusA2 = radius[atom2.element]

        angle = math.asin((atom2.x - atom1.x) / self.bond.len2D)
        angleInDegrees = math.degrees(angle)

        lenRatio = self.bond.len2D / self.bond.len

        sinMultiplier = math.sin(-angle)
        cosMultiplier = math.cos(angle)

        if(atom1.y < atom2.y):
            cosMultiplier = -cosMultiplier
            angleInDegrees = -angleInDegrees
        else:
            if (angleInDegrees > 0):
                angleInDegrees = angleInDegrees - 180
            else:
                angleInDegrees = angleInDegrees + 180
            
        minLengthA1 = math.sqrt(radiusA1**2 - bondWidth**2)
        minLengthA2 = math.sqrt(radiusA2**2 - bondWidth**2)

        x1 = atom1.x * 100 + offsetx - minLengthA1 * lenRatio * sinMultiplier
        y1 = atom1.y * 100 + offsety - minLengthA1 * lenRatio * cosMultiplier
        x2 = atom2.x * 100 + offsetx + minLengthA2 * lenRatio * sinMultiplier
        y2 = atom2.y * 100 + offsety + minLengthA2 * lenRatio * cosMultiplier
        
        dx = self.bond.dx * bondWidth 
        dy = self.bond.dy * bondWidth 

        cx = x1
        cy = y1

        if(atom1.z > atom2.z):
            cx = x2
            cy = y2

        gradCoords = [cx - dy, cy + dx, cx + dy, cy - dx]

        # Normal Version
        gradientColours = ["252525", "454545", "606060", "454545"]
        stopOffsets = ["0", "50", "75", "100"]
        quadrant = int((angleInDegrees/90) % 4 + 1)

        if(atom1.y < atom2.y):
            gradientColours = ["454545", "606060", "454545", "252525"]
            stopOffsets = ["0", "25", "50", "100"]
            
        # Shadowed darker version
        if(quadrant == 2 or quadrant == 4):
            gradientColours = ["252525", "404040", "252525", "050505"]
            stopOffsets = ["0", "25", "50", "100"]
            gradCoords = [x1 - dy, y1 + dx, x1 + dy * 3, y1 - dx * 3]
            if(atom1.y > atom2.y):
                gradCoords = [x1 + dy, y1 - dx, x1 - dy * 3, y1 + dx * 3]

        returnStr = """<linearGradient id="bond{:d}" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" gradientUnits="userSpaceOnUse">\n""".format(bid, gradCoords[0], gradCoords[1], gradCoords[2], gradCoords[3])
        returnStr += """    <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                        </linearGradient>\n""".format(stopOffsets[0], gradientColours[0], stopOffsets[1], gradientColours[1], stopOffsets[2], gradientColours[2], stopOffsets[3], gradientColours[3])
        returnStr += """<linearGradient id="cap{:d}" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" gradientUnits="userSpaceOnUse" gradientTransform="rotate({:.2f},{:.2f},{:.2f})">\n""".format(bid, gradCoords[0], gradCoords[1], gradCoords[2], gradCoords[3], -angleInDegrees, cx, cy)
        returnStr += """    <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                        </linearGradient>\n""".format(stopOffsets[0], gradientColours[0], stopOffsets[1], gradientColours[1], stopOffsets[2], gradientColours[2], stopOffsets[3], gradientColours[3])
        returnStr += """<polygon points="{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}" fill="url(#bond{:d})"/>\n""".format(x1 - dy, y1 + dx, x1 + dy, y1 - dx, x2 + dy, y2 - dx, x2 - dy, y2 + dx, bid)
        returnStr += """<ellipse cx="{:.2f}" cy="{:.2f}" rx="{:.2f}" ry="{:.2f}" transform="rotate({:.2f},{:.2f},{:.2f})" fill="url(#cap{:d})" />\n""".format(cx, cy, bondWidth, bondWidth * math.sqrt(1 - (lenRatio**2)), angleInDegrees, cx, cy, bid)
        
        return returnStr
    

    # The new svg method. Instead, it now creates bonds depending on the number of bonds on the atom.
    def svg(self):
        returnStr = ""
        if (self.bond.epairs == 1):
            returnStr += self.createBond()
        elif (self.bond.epairs == 2):
            returnStr += self.createBond(8, "a", 1)
            returnStr += self.createBond(8, "b", 3)
        elif (self.bond.epairs == 3):
            returnStr += self.createBond(8, "a", 1)
            returnStr += self.createBond(8, "b", 2)
            returnStr += self.createBond(8, "c", 3)
        else:
            returnStr +=self.createBond(bondWidth = 5 * self.bond.epairs)
        return returnStr

    def createBond(self, bondWidth = 8, bidext = "", position = 2):
        bid = self.id
        #bondWidth = 8 -- This used to be 5 + 5 * self.bond.epairs
        atom1 = Atom(molecule.getA1(self.bond)).atom
        atom2 = Atom(molecule.getA2(self.bond)).atom
        colourA1 = colours[atom1.element]
        colourA2 = colours[atom2.element]
        radiusA1 = radius[atom1.element]
        radiusA2 = radius[atom2.element]
        ogBondWidth = bondWidth

        angle = math.asin((atom2.x - atom1.x) / self.bond.len2D)
        angleInDegrees = math.degrees(angle)

        lenRatio = self.bond.len2D / self.bond.len
        
        # Max length from the center of an atom to its edge. It's essentially the max distance the edge of a bond can be drawn.
        maxLengthA1 = math.sqrt(radiusA1**2 - bondWidth**2)
        maxLengthA2 = math.sqrt(radiusA2**2 - bondWidth**2)

        sinMultiplier = math.sin(-angle)
        cosMultiplier = math.cos(angle)

        dx = self.bond.dx * bondWidth 
        dy = self.bond.dy * bondWidth 

        if (atom1.y < atom2.y):
            cosMultiplier = -cosMultiplier
            angleInDegrees = -angleInDegrees
        else:
            if (angleInDegrees > 0):
                angleInDegrees -= 180
            else:
                angleInDegrees += 180
        ogAngleInDegrees = angleInDegrees

        quadrant = int((angleInDegrees/90) % 4 + 1)

        # If the bond is centered, we don't do anything different
        if (position == 2):
                
            x1 = atom1.x * 100 + offsetx - maxLengthA1 * lenRatio * sinMultiplier
            y1 = atom1.y * 100 + offsety - maxLengthA1 * lenRatio * cosMultiplier
            x2 = atom2.x * 100 + offsetx + maxLengthA2 * lenRatio * sinMultiplier
            y2 = atom2.y * 100 + offsety + maxLengthA2 * lenRatio * cosMultiplier

        # If the bond is not centered, we need to calculate everything differently to place the bond "above" or "below" centre.
        # Essentially, we take the center of each atom and add a padding to it 90 degrees from the original bond angle
        # That way, we get a new centre for the atom to go off of. Of course, this means we also need a new maximum length from the center to the edge.
        else:
            minLengthA1 = abs(maxLengthA1 * math.sin(math.radians(60)))
            minLengthA2 = abs(maxLengthA2 * math.sin(math.radians(60)))

            paddingA1 = math.sqrt(maxLengthA1**2 - minLengthA1**2)
            paddingA2 = math.sqrt(maxLengthA2**2 - minLengthA2**2)

            newMaxLengthA1 = math.sqrt(maxLengthA1**2 - paddingA1**2) - 0.25
            newMaxLengthA2 = math.sqrt(maxLengthA2**2 - paddingA2**2) - 0.25

            # To keep the bond the same length as it would be if it was centered, we have to divide by sin(60)
            bondWidth /= math.sin(math.radians(60))

            # This version switches A and B depending on the current rotation. 
            # If atom1 is to the right of atom2, bondA will start on the bottom, but as you rotate on the x axis, it will eventually switch to the top
            # Technically this one makes more sense in a 3D space
            """if (position == 1):
                angleA = angle + math.radians(90)
                angleB = angle - math.radians(90)
            else:
                angleA = angle - math.radians(90)
                angleB = angle + math.radians(90)
            """

            # This version keeps bond A as the top most bond. This one makes ellipse rotation easier
            if ((position == 1 and (quadrant == 1 or quadrant == 4)) or (position == 3 and (quadrant == 2 or quadrant == 3))):
                angleA = angle - math.radians(90)
                angleB = angle + math.radians(90)
            if ((position == 1 and (quadrant == 2 or quadrant == 3)) or (position == 3 and (quadrant == 1 or quadrant == 4))):
                angleA = angle + math.radians(90)
                angleB = angle - math.radians(90)

            # We have to change the angleInDegrees so the ellipse is angled. It looks ugly if it's straight.
            # Each side is pointed in opposite directions, hence why 30 degrees is either added or subtracted depending on the side.
            angleChange = 30
            if (position == 1):
                if (atom1.z < atom2.z):
                    angleInDegrees += angleChange
                else:
                    angleInDegrees -= angleChange
            if (position == 3):
                if (atom1.z < atom2.z):
                    angleInDegrees -= angleChange
                else:
                    angleInDegrees += angleChange

            sinMultiplierA = math.sin(-angleA)
            cosMultiplierA = math.cos(angleA)
            sinMultiplierB = math.sin(-angleB)
            cosMultiplierB = math.cos(angleB)
            if (atom2.y > atom1.y):
                cosMultiplierA = -cosMultiplierA
                cosMultiplierB = -cosMultiplierB

            x1 = (atom1.x * 100 + offsetx - paddingA1 * sinMultiplierA) - newMaxLengthA1 * lenRatio * sinMultiplier
            y1 = (atom1.y * 100 + offsety - paddingA1 * cosMultiplierA) - newMaxLengthA1 * lenRatio * cosMultiplier
            x2 = (atom2.x * 100 + offsetx + paddingA2 * sinMultiplierB) + newMaxLengthA2 * lenRatio * sinMultiplier
            y2 = (atom2.y * 100 + offsety + paddingA2 * cosMultiplierB) + newMaxLengthA2 * lenRatio * cosMultiplier
            
        cx = x1
        cy = y1

        ellipseWidth = bondWidth * math.sqrt(1 - (lenRatio**2))
        ellipseColour = colourA1
        middleEllipseColour = colourA2

        if (atom1.z > atom2.z):
            cx = x2
            cy = y2
            ellipseColour = colourA2
            middleEllipseColour = colourA1

        bondCoords = [x1 - dy, y1 + dx, x1 + dy, y1 - dx, x2 + dy, y2 - dx, x2 - dy, y2 + dx]

        # This entire chunk is for changing the angle of the end of the bond that attaches to the ellipse so it doesn't stick out.
        if (position != 2):
            if (atom1.z < atom2.z):
                newDxA1 = bondWidth * math.sin(math.radians(-angleInDegrees))
                newDyA1 = bondWidth * math.cos(math.radians(angleInDegrees))

                if (position == 1):
                    newDxA2 = bondWidth * math.sin(math.radians(-angleInDegrees + 60))
                    newDyA2 = bondWidth * math.cos(math.radians(-angleInDegrees + 60))
                else:
                    newDxA2 = bondWidth * math.sin(math.radians(-angleInDegrees - 60))
                    newDyA2 = bondWidth * math.cos(math.radians(-angleInDegrees - 60))

            else:
                if (position == 1):
                    newDxA1 = bondWidth * math.sin(math.radians(-angleInDegrees - 60))
                    newDyA1 = bondWidth * math.cos(math.radians(-angleInDegrees - 60))
                else:
                    newDxA1 = bondWidth * math.sin(math.radians(-angleInDegrees + 60))
                    newDyA1 = bondWidth * math.cos(math.radians(-angleInDegrees + 60))

                newDxA2 = bondWidth * math.sin(math.radians(-angleInDegrees))
                newDyA2 = bondWidth * math.cos(math.radians(-angleInDegrees))

            bondCoords = [x1 - newDyA1, y1 + newDxA1, x1 + newDyA1, y1 - newDxA1, x2 + newDyA2, y2 - newDxA2, x2 - newDyA2, y2 + newDxA2]            
            
        gradCoords = [cx - dy, cy + dx, cx + dy, cy - dx]

        # Normal Version
        gradientColours = ["2D2D2D", "535353", "737373", "535353"]
        stopOffsets = ["0", "50", "75", "100"]

        if (atom1.y < atom2.y):
            gradientColours = ["535353", "737373", "535353", "2D2D2D"]
            stopOffsets = ["0", "25", "50", "100"]
            
        # Shadowed darker version
        if (quadrant == 2 or quadrant == 4):
            gradientColours = ["2F2F2F", "4C4C4C", "2F2F2F", "0E0E0E"]
            stopOffsets = ["0", "25", "50", "100"]
            gradCoords = [x1 - dy, y1 + dx, x1 + dy * 3 , y1 - dx * 3]
            if(atom1.y > atom2.y):
                gradCoords = [x1 + dy, y1 - dx, x1 - dy * 3, y1 + dx * 3]

        # Main Bond Gradient
        returnStr = """<linearGradient id="bond{:d}{:s}" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" gradientUnits="userSpaceOnUse">\n""".format(bid, bidext, gradCoords[0], gradCoords[1], gradCoords[2], gradCoords[3])
        returnStr += """    <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                        </linearGradient>\n""".format(stopOffsets[0], gradientColours[0], stopOffsets[1], gradientColours[1], stopOffsets[2], gradientColours[2], stopOffsets[3], gradientColours[3])
        
        # Bond Overlay Gradient
        returnStr += """<linearGradient id="bondColour{:d}{:s}" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" gradientUnits="userSpaceOnUse">
                            <stop offset="50%" stop-color="#{:s}" />
                            <stop offset="50%" stop-color="#{:s}" />
                        </linearGradient>\n""".format(bid, bidext, x1, y1, x2, y2, colourA1, colourA2)
        
        # Main Ellipse Gradient
        returnStr += """<linearGradient id="cap{:d}{:s}" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" gradientUnits="userSpaceOnUse" gradientTransform="rotate({:.2f},{:.2f},{:.2f})">\n""".format(bid, bidext, gradCoords[0], gradCoords[1], gradCoords[2], gradCoords[3], -angleInDegrees, cx, cy)
        returnStr += """    <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                            <stop offset="{:s}%" stop-color="#{:s}" />
                        </linearGradient>\n""".format(stopOffsets[0], gradientColours[0], stopOffsets[1], gradientColours[1], stopOffsets[2], gradientColours[2], stopOffsets[3], gradientColours[3])
        
        # Main Bond Drawing
        returnStr += """<polygon points="{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}" fill="url(#bond{:d}{:s})"/>\n""".format(bondCoords[0], bondCoords[1], bondCoords[2], bondCoords[3], bondCoords[4], bondCoords[5], bondCoords[6], bondCoords[7], bid, bidext)
        # Main Ellipse Drawing
        returnStr += """<ellipse cx="{:.2f}" cy="{:.2f}" rx="{:.2f}" ry="{:.2f}" transform="rotate({:.2f},{:.2f},{:.2f})" fill="url(#cap{:d}{:s})" />\n""".format(cx, cy, bondWidth, ellipseWidth, angleInDegrees, cx, cy, bid, bidext)
              

        # Overlay. If the colours or not the same, it adds a middle ellipse
        if (colourA1 != colourA2):
            middleEllipseX = (x1 + x2) / 2
            middleEllipseY = (y1 + y2) / 2
            returnStr += """<g id="overlay">
                                <polygon points="{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}" fill="url(#bondColour{:d}{:s})"/>
                                <ellipse cx="{:.2f}" cy="{:.2f}" rx="{:.2f}" ry="{:.2f}" transform="rotate({:.2f},{:.2f},{:.2f})" fill="#{:s}" />
                                <ellipse cx="{:.2f}" cy="{:.2f}" rx="{:.2f}" ry="{:.2f}" transform="rotate({:.2f},{:.2f},{:.2f})" fill="#{:s}" />
                            </g>\n""".format(bondCoords[0], bondCoords[1], bondCoords[2], bondCoords[3], bondCoords[4], bondCoords[5], bondCoords[6], bondCoords[7], bid, bidext,
                                             cx, cy, bondWidth, ellipseWidth, angleInDegrees, cx, cy, ellipseColour,
                                             middleEllipseX, middleEllipseY, ogBondWidth, ellipseWidth, ogAngleInDegrees, middleEllipseX, middleEllipseY, middleEllipseColour)
        else:
            returnStr += """<g id="overlay">
                                <polygon points="{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}" fill="url(#bondColour{:d}{:s})"/>
                                <ellipse cx="{:.2f}" cy="{:.2f}" rx="{:.2f}" ry="{:.2f}" transform="rotate({:.2f},{:.2f},{:.2f})" fill="#{:s}" />
                            </g>\n""".format(bondCoords[0], bondCoords[1], bondCoords[2], bondCoords[3], bondCoords[4], bondCoords[5], bondCoords[6], bondCoords[7], bid, bidext,
                                             cx, cy, bondWidth, ellipseWidth, angleInDegrees, cx, cy, ellipseColour)

        return returnStr


    
class Molecule(molecule.molecule):

    # A method that prints all the molecule's info for debugging.
    # Uses the __str__ methods defined in each class to print info.
    def __str__(self):
        returnStr = ""

        for i in range(self.atom_no):
            returnStr += self.get_atom(i).__str__() + "\n"

        for i in range(self.bond_no):
            returnStr += self.get_bond(i).__str__() + "\n"

        return returnStr


    # A method that displays the entire molecule to the user using the svg() methods in the Atom and Bond classes.
    def svg(self):
        
        string = ""
        string += header

        # For loops that get every atom and bond in the molecule
        # Once this is done, we sort them accordingly
        atoms = [Atom(self.get_atom(i)) for i in range(self.atom_no)]
        bonds = [Bond(self.get_bond(i)) for i in range(self.bond_no)]
        items = sorted((atoms + bonds), key=lambda item: item.z)

        # Loop through every item in the list and print it to the screen
        for item in items:
            if (isinstance(item, Bond)):
                if (svgMode == 1):
                    string += item.svg()
                if (svgMode == 2):
                    string += item.nightmare_mode_svg()
                if (svgMode == 3):
                    string += item.original_svg()
            else:
                string += item.svg()

        string += footer
        return string
            
    # A method that takes the contents of a file and parses it so it can be printed
    def parse(self, file): 

        # First read the entire file into a list and split it's contents by spaces.
        file = file.readlines()

        # The third line is where all the initial information about the molecule is located.
        # We need to get the total number of atoms and bonds from this line so we can use it for the next part.
        if (len(file) < 3):
            return False
        molInfo = file[3].split(" ")
        molInfo[:] = [item for item in molInfo if item != ""]
        
        try:
            totalAtoms = int(molInfo[0])
            totalBonds = int(molInfo[1])
        except (ValueError, IndexError):
            return False

        # A loop that goes from 0 to the totalAtoms - 1
        # Take each line, split it into its x, y, z, and element, then create a new atom using those values.
        for i in range(totalAtoms):
            line = file[i + 4].split(" ")

            try:
                line[:] = [item for item in line if item != ""]
                x, y, z = map(float, line[:3])
                element = line[3]
            except (ValueError, IndexError):
                return False
            self.append_atom(element, x, y, z)

        # A loop that goes from 0 to the totalBonds - 1
        # Take each line, split it into a1, a2, and epairs, then create a bond using those values.
        for i in range(totalBonds):
            line = file[i + 4 + totalAtoms].split(" ")
            
            try:
                line[:] = [item for item in line if item != ""]
                a1, a2, epairs = map(int, line[:3])
            except (ValueError, IndexError):
                return False
            self.append_bond(a1 - 1, a2 - 1, epairs)


    def get_rotations(self):

        self.xRotations = []
        self.yRotations = []
        self.zRotations = []

        self.xRotations.append(self.svg())
        self.yRotations.append(self.svg())
        self.zRotations.append(self.svg())

        mx = molecule.mx_wrapper(1,0,0)
        my = molecule.mx_wrapper(0,1,0)
        mz = molecule.mx_wrapper(0,0,1)

        for i in range(361):
            self.xRotations.append(self.svg())
            self.xform(mx.xform_matrix)
        for i in range(361):
            self.yRotations.append(self.svg())
            self.xform(my.xform_matrix)
        for i in range(361):
            self.zRotations.append(self.svg())
            self.xform(mz.xform_matrix)
        
        return { "x" : self.xRotations, "y" : self.yRotations, "z" : self.zRotations }

"""
Student Author Name: Campbell Gilbert
Project 2
Fall 2022
COMP 313: Computer Graphics
Professor Schiffer
"""
import matplotlib.pyplot as plt
from math import sin, cos, radians
import sys
import numpy as np

# Add aspect ratio, to prevent distortion
figure, axes = plt.subplots()
axes.set_aspect(1)
# Set up axis
plt.axis([-10, 10, -10, 10])

#Because I hated typing [0, 0, 0] over and over again
CENTER_COORDS = [0, 0, 0]

#Functions are arranged in ascending order; if one function calls another, the second will be above it, and so on. main() is at the bottom.

#Plots the shape.
def plot_shape(faces, local_coords):
    for face in faces:
        for i in range(len(face)):
            #print("i: ", i)
            current = local_coords[face[i] - 1]
            next = local_coords[face[(i+1) % len(face)] - 1]
            plt.plot([current['x'] + CENTER_COORDS[0], next['x'] + CENTER_COORDS[0]], [current['y'] + CENTER_COORDS[1], next['y'] + CENTER_COORDS[1]], color='k')

#Given an axis (x, y, or z) and an angle, generates a matrix we can then use to rotate a set of coordinates.
def generate_matrix(axis, angle):
    matrices = {
        'x': [
                [1,          0,           0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle) ]
        ],
        'y': [
                [ cos(angle), 0, sin(angle)],
                [0,           1,          0],
                [-sin(angle), 0, cos(angle)]
        ],
        'z': [
                [cos(angle), -sin(angle),  0],
                [sin(angle),  cos(angle),  0],
                [          0,           0, 1]
        ]
    }
    return matrices[axis]

#Multiply a set of coordinates by a matrix
def rotate(local_coords, matrix):
    final_coords = []
    for i in range(len(matrix)):
        final_coords.append(np.inner(matrix[i], local_coords))
    return final_coords

#These two do exactly what they say on the tin
def convert_coord_to_list(coord):
    return [coord['x'], coord['y'], coord['z']]

def convert_list_to_coord(list_coord):
    return {'x': list_coord[0], 'y': list_coord[1], 'z': list_coord[2]}

#rotating coordinates by 1 angle on 1 axis
def rotate_list(all_coords, init_angle, axis):
    angle = radians(int(init_angle))
    coord_list = []
    for i in range(len(all_coords)):
        coord_list.append(convert_list_to_coord(rotate(convert_coord_to_list(all_coords[i]), generate_matrix(axis, angle))))
    # print(coord_list)
    return coord_list

#rotating coordinates multiple times
#Center isn't actually needed for this function call since I made it a global var but having it as a param is part of the assignment so it stays.
def rotate_sequence(center, angles, rotseq, obj_coords):
    for rot in rotseq:
        prev_coords = obj_coords
        obj_coords = rotate_list(prev_coords, angles[rot], rot)
    return obj_coords

#read OBJ file and translate it into something we can plot
def read_file():
    obj_coords = []
    obj_faces = []
    obj = "GilbertCPlaneFINAL"
    
    print(obj)

    with open("{object}.obj".format(object = obj), 'r') as f:
        lines = f.readlines()
    f.close()

    for line in lines:
        if 'v' in line:
            coord = handle_vertices(line)
            if coord is not None:
                obj_coords.append(coord)
        if 'f' in line:
            faces = handle_faces(line)
            if faces is not None:
                obj_faces.append(faces)

    return obj_coords, obj_faces

#turn verticies from OBJ file into list that we can plot
def handle_vertices(line):
    vertices = line.split(" ")
    if vertices[0] != 'v':
        return None
    return {'x': vertice_to_float(vertices[1]), 'y': vertice_to_float(vertices[2]), 'z': vertice_to_float(vertices[3])}

#turn faces from OBJ file into list of which verticies are connected
def handle_faces(line):
    faces = line.split(" ")
    if faces[0] != 'f':
        return None
    faces.pop(0)
    final_faces = []
    for face in faces:
        final_faces.append(face_to_int(face))
    return final_faces

#turn verticies from obj file into floats
def vertice_to_float(vertex):
    # For z values, remove the \n
    vert = vertex.replace("\n", "")
    return float(vert)

#turn faces from obj file into ints for iteration
def face_to_int(face):
    face = face.replace("\n", "")
    return int(face)

#Verify that inputted rotation sequence is valid.
def verify_rotseq(dir):
    if set(dir) <= set('xyz'):
        return dir
    return 'x'

#If extra time figure out a way to handle duplicates; otherwise, fine as is. 
def main():
    obj_coords, faces = read_file()
    dir = input("Input order of rotations (1-3 rotations, no duplicates, in form 'xzy', 'zyx', etc. Don't use 'R'. Default is x.): ")
    
    rotseq = verify_rotseq(dir)

    xangle, yangle, zangle = [0, 0, 0]

    if 'x' in rotseq:
        xangle = input("X-rotation angle (default 0): ")
    if 'y' in rotseq:
        yangle = input("Y-rotation angle (default 0): ")
    if 'z' in rotseq:
        zangle = input("Z-rotation angle (default 0): ")
    
    angles = {'x': xangle, 'y': yangle, 'z': zangle}
    
    rotdcoords = rotate_sequence(CENTER_COORDS, angles, rotseq, obj_coords)

    plot_shape(faces, rotdcoords)

    plt.show()


main()
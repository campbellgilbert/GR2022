import bpy
import math
import numpy as np
"""
Student Author Name: Campbell Gilbert
Project 3
Fall 2022
COMP 313: Computer Graphics
Professor Schiffer
""" 

def circle_rotation(starter, axis, dir, rad=0.3, numFrames=10, inwardChange=0):
    #generating positions of an item (toy airplane) rotating around a point on the X-axis
    #starter: tuple. position item is starting at.
    #axis: X, Y, or Z
    #direc: clock or count (clockwise or counterclockwise)
    #rad: radius
    if axis == 'X':
        rotdic = {
            'tow': 0,
            'horiz': 1, 
            'vert': 2
        }   
    elif axis == 'Z':
        rotdic = {
            'tow': 2,
            'horiz': 0,
            'vert': 1
        }

    elif axis == 'Y':
        rotdic = {
            'tow': 1,
            'horiz': 2,
            'vert': 0
        }

    posses = (starter,)
    holder = (0, starter[1], starter[2])
    
    a = 0 #points on a circle
    q = numFrames / 2
    for i in range(numFrames):
        t = 2.*np.pi*float(i/(numFrames - 1.))
            
        if dir == 'count':
            holddic = {
                rotdic['horiz']: int(holder[rotdic['horiz']] - ((rad * np.sin(t)) * 60)),
                rotdic['vert']: int(holder[rotdic['vert']] - ((rad * np.cos(t)) * 60)),
                rotdic['tow']: int(holder[rotdic['tow']] - inwardChange)
            }
        elif dir == 'clock':
            holddic = { 
                rotdic['horiz']: int(holder[rotdic['horiz']] + ((rad * np.sin(t)) * 50)),
                rotdic['vert']: int(holder[rotdic['vert']] + ((rad * np.cos(t)) * 50)),
                rotdic['tow']: int(holder[rotdic['tow']] + inwardChange)
            }
        holder = (holddic[0], holddic[1], holddic[2])
        
        if holder[2] == starter[2] and ((holder[1] + 5 > starter[1]) and (holder[1] - 5 < starter[1])):
            posses = posses + (starter,)
            break
        
        posses = posses + (holder,)

    return posses[1:]


def circle_rotation_multi(numRots, starter, axis, dir, rad=0.3, numFrames=10, inwardChange = 0):
    #Do multiple circle rotations, such as spiraling downwards.
    #numRots: number of full rotations to make.
    posses = circle_rotation(starter, axis, dir, rad, numFrames, inwardChange)
    currStart = posses(posses.length - 1)
    
    for i in range(numRots):
        posses += circle_rotation(currStart, axis, dir, rad - (rad / numFrames), numFrames, inwardChange)
        currStart = posses(posses.length - 1)
        
    return posses

def simple_forward(numFrames, startPoint, endPoint, axis1=1, axis2=2):
    #Simply move the plane forward for a given direction a given axis. 
    
    #numFrames: number of keyframes to generate
    #startPoint: starting position
    #endPoint: ending position
    #rot: starting rotation (since this is simple we just hold the same rotation for the whole time)
    #axis1: which axis to move on. 0 for x, 1 for y, 2 for z
    #axis2: which axis to move on. 0 for x, 1 for y, 2 for z
    #dir1: pos or neg; determines if we add or subtract for axis 1
    #dir2: pos or neg; determines if we add or subtract for axis 2

    numFrames -= 1
    
    adder1 = (endPoint[axis1] - startPoint[axis1]) / numFrames
    adder2 = (endPoint[axis2] - startPoint[axis2]) / numFrames

    posses = (startPoint,)
    prevPoint = startPoint
    
    for k in range(numFrames):
        currPoint = [prevPoint[0], prevPoint[1], prevPoint[2]]
        
        currPoint[axis1] += adder1
        currPoint[axis2] += adder2
        
        prevPoint = tuple(currPoint)
        posses += prevPoint,
    
    return tuple([(int(i[0]), int(i[1]), int(i[2])) for i in posses])

  
def spin_rots(startRot, xChange, upTilt=30, numRots=1, dir="clockwise"):
    #Creates rotation for a spin movement, specifically on the line (0, 1, 1)/(0, -1, 1)
    #startRot: starting (and ending) rotation.
    #xChange: amount to change x by listen i couldnt figure this out ok gimme a break
    #upTilt: z-axis displacement.
    #numRots: amount of full rotations being done.
    
    #numFramesPerRot: ALWAYS 4; will return rotations*4 + 1 frames

    z_add = [90, 90]
    if dir == "counterclockwise":
        upTilt = upTilt * -1
        z_add = [-90, -90]
        
    x_vals = (startRot[0] + xChange, startRot[0] * -1, (startRot[0] + xChange) * -1, startRot[0])
    y_vals = (startRot[1] - upTilt, startRot[1], startRot[1] + upTilt, startRot[1])
    
    rots = (startRot),
    prevRot = startRot
    index = 0
    
    for q in range(numRots):
        prevZ = prevRot[2]
        z_add[0] = z_add[1]
        j = 0
        while abs(z_add[0]) < 450: #1 full rotation
            if index > 3:
                index = 0
            
            x_add = x_vals[index]
            y_add = y_vals[index]
    
            currRot = [x_vals[index], y_vals[index], prevZ + z_add[0]]
            prevRot = tuple(currRot)
            rots += prevRot,
            
            z_add[0] += z_add[1]
            index += 1
            j+=1

    return rots


# Initialize lists of tuples

#Plane
    #go up
positions = (0,3,2), (-3, 27, 30), (-7, 32, 120),
rotations = (90, 0, 180), (90, 0, 180), (90, 0, 180)


#SAMPLE 6

    #do a little spin up and forwards
#hardcoding this bc its weird
#1) go straight up
#2) spin on z
#3) move a little forward
#4) rinse repeat
#simpleForward(5, startPoint, endPoint, axis1=1, axis2=2, dir1='neg', dir2='neg'):
positions += simple_forward(5,  (-8, 40, 135), (-8, 80, 195)) 
rotations += spin_rots((30, 0, 180), -25, 30)
#print("possie1: ", len(simple_forward(5,  (-8, 40, 135), (-8, 80, 195))))
#print("rotsie1: ", len(spin_rots((30, 0, 180), -25, 30)))
#print()

    #go straight ahead a tiny bit
positions += (-8, 90, 196), (-8, 120, 200),
rotations += (90, 0, 540), (90, 0, 540), 

    #go straight up a teeny tiny bit & flip
positions += (-8, 125, 205), (-8, 130, 220)
rotations += (0, 0, 540), (0, 0, 360)

    #CIRCLE
positions += circle_rotation((-8, 130, 220), 'X', 'clock', 0.4, 7)
rotations += (-30, 0, 360), (-120, 0, 360), (-160, 0, 360), (-200, 0, 360), (-300, 0, 360), (-300, 0, 360)

    #go forwards a little while pointing up
positions += (-8, 90, 230),
rotations += (-300, 0, 360),

    #done
startSample4 = len(positions)


#SAMPLE 4

#get back in place (offcamera)
positions += (-8, 100, 230), (-8, 70, 230),
rotations += (80, 0, 0), (80, 0, 0),

    #turn around in the air on the z-axis -- go from pointing forward to pointing to the side
    #hold that side point for a frame
positions += (-8, 55, 250), (-8, 55, 250), (-9, 55, 250), (-9, 55, 250), (-9, 55, 250), 
rotations += (80, 10, 0), (80, 40, 25), (82, 40, 45), (84, 33, 55), (86, 25, 80), 
    
    #then point back forward 
positions += (-6, 55, 250), (-3, 55, 248), (0, 55, 246), (1, 55, 246), (0, 55, 244),
rotations += (85, 20, 45), (86, 12, 30), (93, -12, 0), (95, -23, 0), (95, -35, 0),

    #and spin forward + down. 
positions += (0, 50, 240),  
rotations += (30, -110, 70),

    #7 full spins
    #let's say 4 frames PER rotation, so that'll generate...35 frames WTF
spinStart = len(rotations)
rotsie = spin_rots((45, -180, 0), xChange=-45, upTilt=-50, numRots=7, dir="counterclockwise")
rotations += rotsie[:(len(rotsie) - 1)]

    #spin a tiny bit more (tilted a little bit to the side, going down
    #straighten out and go forward
    #then go SLIGHTLY up
possie = simple_forward(29, (0, 45, 235), (0, -70, 160), 1, 2)
positions += possie[:(len(possie) - 1)]
spinEnd = len(rotations)

positions += (-7, -80, 155), (-16, -92, 144), (-30, -155, 102), (-50, -240, 102),
rotations += (-40, -140, -2400), (-65, -155, -2390), (-80, -160, -2380), (-100, -180, -2384),

positions += (-50, -282, 108), (-50, -290, 115), 
rotations += (-105, -180, -2384), (-106, -180, -2384), 

endSample4 = len(positions) - 1


#END
#circle down and land
positions += (-50, -225, 115), (-25, -126, 115), (-25, -87, 70), (0,3,2),
rotations += (-100, -180, 0), (-80, -180, 0), (-80, -180, 0), (-90, -180, 0), 



#Cameras
cameraAPos = [(0, 6.5, 3.3) for i in positions]
cameraARots = [(90, 0, 0) for i in rotations]


cameraBPos = (-40, 0, 7)
cameraBRots = (90, 0, -90)


camCPos = (37, 30, 120), (39, 15, 119), (30, 15, 136), (28, 20, 142), (22, 27, 150), (22, 33, 155)
camCRots = (90, 0, 90), (108, 0, 60), (108, 0, 45), (115, 10, 45), (123, 13, 45), (122, 17, 45) 

camCPos += (22, 43, 190), (14, 78, 194), (14, 83, 197), (14, 83, 200), (14, 83, 206), (13, 82, 205), 
camCRots += (105, 0, 30), (100, 0, 30), (100, 0, 30), (115, 0, 25), (120, 0, 20), (125, 0, 16), 

camCPos += (14, 83, 206), (14, 79, 206), (12, 77, 204), (8, 75, 204), (10, 63, 204),
camCRots += (110, 0, 15), (100, 0, 15), (98, 0, 15), (105, 0, 15), (130, 0, 30),


#frames 380-620
camDPos = (-8, 0, 210), (-8, -20, 220), (-8, -20, 220), (-8, -20, 220), (-8, -20, 220),
camDRots = (120, 0, 0), (110, 0, 0), (110, 0, -5), (109, 0, -3), (108, 0, -4), 

camDPos += (-8, -20, 220), (-8, -20, 220), (-8, -20, 220), (-8, -20, 220), (-8, -20, 220),
camDRots += (108, 0, -5), (109, 0, -5), (109, 0, -6), (108, 0, -6), (109, 0, -5),

camDPos += (-8, -20, 220), (-15, -20, 220), (-15, -20, 220)
camDRots += (109, 0, -6), (108, 0, -8), (105, 0, -8),

#frames 640-
for i in range(5):
    prev = len(camDPos) - 1
    camDPos += (-15, camDPos[prev][1] - 10, 220),
    camDRots += (camDRots[prev][0] - 2, 0, -10),

camDPos += (-20, -70, 215), (-20, -80, 212), (-20, -90, 210),
camDRots += (95, 0, -12), (92, 0, -12), (92, 0, -13), 

for i in range(11):
    prev = len(camDPos) - 1
    camDPos += (-20, camDPos[prev][1] - 2, camDPos[prev][2] - 3),
    camDRots += (92, 0, -13),

for i in range(9):
    prev = len(camDPos) - 1
    camDPos += (camDPos[prev][0] - 2, camDPos[prev][1] - 10, camDPos[prev][2] - 3),
    camDRots += (92, 0, -13),

camDPos += (-40, -200, 145), (-40, -200, 145), (-30, -250, 108), #(-30, -220, 100),
camDRots += (92, 0, -13), (92, 0, -10), (92, 0, 0), #(95, 0, 0), 

camDPos += (-30, -280, 100), (-25, -275, 100), (-30, -270, 100),
camDRots += (92, 0, 30), (105, 0, 102), (120, 0, 130),

    
# Initialize object references
plane = bpy.data.objects["Plane"]
prop = bpy.data.objects["propeller"]
cameraA = bpy.data.objects["CameraA"]
cameraB = bpy.data.objects["CameraB"]
cameraC = bpy.data.objects["CameraC"]
cameraD = bpy.data.objects["CameraD"]

# Declare function
def set_keyframes():
    frame_num = 0
    
    cameraA.location = (0, 6.5, 3.3) #relative to plane
    cameraA.rotation_euler = (math.radians(90), 0, 0)
    cameraA.keyframe_insert(data_path='location', index=-1)
    cameraA.keyframe_insert(data_path='rotation_euler', index=-1)
    
    prevPropRot = 0
    
    for index,position in enumerate(positions):
        bpy.context.scene.frame_set(frame_num)

        #Camera C activate
        if index >= 2 and index <= 18:
            currCamIndex = index - 2
            cameraC.location =  camCPos[currCamIndex]
            cameraC.rotation_euler = (math.radians(camCRots[currCamIndex][0]), math.radians(camCRots[currCamIndex][1]), math.radians(camCRots[currCamIndex][2]))
            cameraC.keyframe_insert(data_path='location', index=-1)
            cameraC.keyframe_insert(data_path='rotation_euler', index=-1)
        
        if index >= startSample4 and index - startSample4 < len(camDPos):
            currCamIndex = index - startSample4
            cameraD.location =  camDPos[currCamIndex]
            cameraD.rotation_euler = (math.radians(camDRots[currCamIndex][0]), math.radians(camDRots[currCamIndex][1]), math.radians(camDRots[currCamIndex][2]))
            cameraD.keyframe_insert(data_path='location', index=-1)
            cameraD.keyframe_insert(data_path='rotation_euler', index=-1)
        
        # Record location coords
        plane.location = position
        
        # Record rotation angles in XYZ Euler
        plane.rotation_euler = (math.radians(rotations[index][0]), math.radians(rotations[index][1]), math.radians(rotations[index][2]))
        prop.rotation_euler = (math.radians(90), math.radians(prevPropRot), 0)
        prevPropRot += 630
        
        # Record keyframes
        plane.keyframe_insert(data_path='location', index=-1)
        plane.keyframe_insert(data_path='rotation_euler', index=-1)
        
        prop.keyframe_insert(data_path='rotation_euler', index=-1)

        if (index >= spinStart and index < spinEnd):
            frame_num += 10
        elif index > spinEnd:
            frame_num += 40
        else:
            frame_num += 15

    pass

def main():
    set_keyframes()
    pass
    
main()


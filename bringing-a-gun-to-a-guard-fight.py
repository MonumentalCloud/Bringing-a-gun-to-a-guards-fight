from itertools import cycle
from math import sqrt, atan2

def solution(dimensions, your_position, guard_position, distance):
    #So my approach here was to create a vitural mirrored "rooms" that infinitely mirrors (I can provide diagrams upon request)
    #Then I went on to calculate all the reflected virtual me's and enemy's x and y coordinates within the radius = distance
    #And then I converted the given x,y coordinates and converted them into dictionary, the radian angle value as its key and the "length" of the vector as its EnemyXValues
    #The reason why the "length" of the beam is important is to determine if the beam will hit the enemy before it hits me, in which case it will still be valid
    #Finally, I extracted the keys of the enemies dictionary that's either not in "me" dictionary or if it is, has shorter length as its value.
    #fyi, the corner cases are omitted here because in an infinitely mirrored rooms, the set of vectors that will hit corner is a subset of the set of vectors that will hit myself.
    def getCoordinates(dimensionX, meX, enemyX, distance):
        #this is the function to get the x and y coordinates within the radius of distance given.
        #this essentially makes sure to only count the coordinates at are within default position(me)-distance < either x or y coordinates < default position(me)+distance
        posStep = cycle([2*(dimensionX - enemyX), 2* enemyX])
        negStep = cycle([2* enemyX,2*(dimensionX - enemyX)])
        #because of the mirroring effect, the distance between each x and y coordinates will alternate between 2* enemyX and 2*(dimensionX - enemyX
        #simply put, those two numbers are just two times the distance of how far the given point is from either end of the room.
        final = set()
        posX = enemyX
        negX = enemyX
        while enemyX <= meX + distance:
            posX = enemyX
            final.add(posX)
            enemyX += next(posStep)
        while negX>= meX - distance:
            final.add(negX)
            negX -= next(negStep)
        #These two while loops calculate the coordinates in the opposite direction from the same default point
        return final

    #The following two functions (enemyDictionary, meDictionary) will utilize the getCoordinates tunction above to
    #compile the x and y coordinates that are given separately, into a dictionary with radian value of the vector as its key and the length of the beam before it hits the target as its value
    def enemyDictionary(dimensions, your_position, guard_position, distance):
        x = getCoordinates(dimensions[0], your_position[0], guard_position[0],distance)
        y = getCoordinates(dimensions[1], your_position[1], guard_position[1],distance)
        # x, y is a set of possible x and y coordinates within a cube that perfectly fits in a circle of radius = distance
        final = {}
        for i in x:
            for j in y:
                angle = atan2(i-your_position[0],j-your_position[1])#radian as a key of "final" dictionary
                length = sqrt((your_position[0]-i)**2+(your_position[1]-j)**2)#length as a value of "final" dictionary
                if length <= distance:#this narrows down the coordinates within the aforementioned cube to the circle
                    if angle not in final:
                        final[angle] = length
                    elif length < final[angle]:#these two if, elif chain makes sure the angle is unique, and if it's not, it saves the shortest length of the beam of the angle
                        final[angle] = length
        return final
    #same exact mechanism is used in the medictionary!
    def meDictionary(dimensions, your_position, guard_position, distance):
        x = getCoordinates(dimensions[0], your_position[0], your_position[0],distance)
        y = getCoordinates(dimensions[1], your_position[1], your_position[1],distance)
        final = {}
        for i in x:
            for j in y:
                angle = atan2(i-your_position[0],j-your_position[1])
                length = sqrt((your_position[0]-i)**2+(your_position[1]-j)**2)
                if length <= distance:
                    if angle not in final:
                        final[angle] = length
                    elif length < final[angle]:
                        final[angle] = length
        return final

    #as the name suggest, this function subtract "me" dictionary containing all mirrored me's within the range from "enemy" dictionary.
    def subtract(dimensions, your_position, guard_position, distance):
        me = meDictionary(dimensions, your_position, guard_position, distance)
        enemy = enemyDictionary(dimensions, your_position, guard_position, distance)
        Number1Vector = (your_position[0]-guard_position[0], your_position[1]-guard_position[1])
        if sqrt(Number1Vector[0]**2+Number1Vector[1]**2) > float(distance):#this is in case the enemy is not within the beam's range
            return []
        else:
            for i in me:
                if i in enemy and me[i]<=enemy[i]:#this conditional for loop gets rid of angles from enemy only if the length is longer than the corresponding length in me meDictionary
                #this efffectively means that if the length is longer in enemy than me, the beam will hit me before enemy, and we don't want that
                    enemy.pop(i)
            return set([i for i in enemy.keys()])



    return len(subtract(dimensions, your_position, guard_position, distance))

print solution([3,2], [1,1], [2,1], 4)

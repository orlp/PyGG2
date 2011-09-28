from functions import place_free, sign, point_direction
import pygame
import math

def objectCheckCollision(character):
    # Check if a the Character has hit the wall:

    hasCollided = False

    character.rect.centerx = character.x-character.xRectOffset
    character.rect.centery = character.y-character.yRectOffset

    clip = character.rect.clip(character.root.map.rect)

    # find where clip's top-left point is in both rectangles
    x1 = clip.left - character.root.map.rect.left
    y1 = clip.top  - character.root.map.rect.top
 
    # cycle through clip's area of the hitmasks
    for x in range(clip.width):
        for y in range(clip.height):
            # returns True if neither pixel is blank
            if character.root.map.mask.get_at((x1+x, y1+y)) == 1:
                hasCollided = True

    if hasCollided:
        return True
    else:
        return False



def characterHitObstacle(character):


# THIS IS THE NEW VERSION; STILL WITH x/y


    newX = character.x
    newY = character.y

    hspeed = character.hspeed
    vspeed = character.vspeed

    length = math.hypot(hspeed, vspeed)

    if length == 0:# You haven't moved; if this happens something went wrong

        print "You haven't moved, yet managed to collide with something."
        return False


    # hs and vs is the normalized vector of hspeed and vspeed.
    hs = character.hspeed/length
    vs = character.vspeed/length

    while True:
        if not objectCheckCollision(character):
            break

        character.x -= hs
        character.y -= vs
   
    if hspeed == 0 or vspeed == 0:
    	return True

    # This is the left-over velocity.
    hs = hspeed
    vs = vspeed

    # The character got pushed out, but now we need to let him move in the directions he's allowed to move.


    character.x += sign(hs)

    if not objectCheckCollision(character) and abs(hs) > 0:

        # There's still room to move on the left/right

        i = 1
        while i <= abs(hs) and not objectCheckCollision(character):

            character.x += sign(hs)
            i += 1


        if objectCheckCollision(character):
            character.x -= sign(hs)

        return True

    else:

        # Stop horizontal movement
        character.hspeed = 0
        character.hs = 0
        character.x -= sign(hs)


    character.y += sign(vs)

    if not objectCheckCollision(character) and abs(vs) > 0:

        # There's still room to move on the left/right


        i = 1
        while i <= abs(vs) and not objectCheckCollision(character):

            character.y += sign(vs)
            i += 1

        if objectCheckCollision(character):
            character.y -= sign(vs)

        return True

    else:

        # INSERT STAIR CODE; SEE BELOW

        # Stop vertical movement
        character.vspeed = 0
        character.vs = 0
        character.y -= sign(vs)

    return True









# STAIRS CODE; INSERT IN "STAIR CODE" ONCE FIXED
'''

        character.y -= 6

        if not objectCheckCollision(character):

            character.y += 6# This is to compensate for the loop.
            character.x -= sign(character.hspeed)*6

            while hs*sign(character.hspeed) > 0:

                character.y -= 6
                character.x += sign(character.hspeed)*6
                hs -= sign(character.hspeed)*6

                if objectCheckCollision(character):

                    character.y += 6
                    character.x -= sign(character.hspeed)*6
                    break

        else:'''

















'''



# THIS IS THE ORIGNAL GG2 COLLISION CODE, PORTED FRESH FROM GMK. Not needed.

	# The Character has collided; Push him back out:

	# This code was written for a situation before the character actually moved, but I want to keep this compatible with our structure.
	# Hence; move everything back, and move forward as far as we can.

	character.x -= character.hspeed
	character.y -= character.vspeed

	hleft = character.hspeed
	vleft = character.vspeed

	loopCounter = 0
	stuck = 0
	collisionRectified = True
	while((abs(hleft) >= 1 or abs(vleft) >= 1) and stuck == 0): # while we still have distance to travel
		loopCounter += 1
		if(loopCounter > 10):
		    # After 10 loops, it's assumed we're stuck. Stop all vertical movement.
			stuck = 1

		collisionRectified = False # set this to true when we fix a collision problem
		# (eg. detect hitting the ceiling and setting vspeed = 0)
		# if, after checking for all our possible collisions, we realize that we haven't
		# been able to fix a collision problem, then we probably hit a corner or something,
		# and we should try to fix that

		prevX = character.x
		prevY = character.y


		# move as far as we can without hitting something
		# In GMK, this was "move_contact_solid(point_direction(x, y, x + hleft, y + vleft), point_distance(x, y, x + hleft, y + vleft))"

		length = functions.lengthdir(hleft, vleft)
		distance = 0

		while distance < length:

			character.x = character.x+hleft*distance
			character.y = character.y+vleft*distance

			if objectCheckCollision(character, wallmask):
				character.x = character.x-hleft*distance
				character.y = character.y-vleft*distance
				break

			distance += length/20


		# deduct that movement from our remaining movement
		hleft -= (character.x - prevX)
		vleft -= (character.y - prevY)

		# determine what we hit, and act accordingly

		if(vleft != 0 and not functions.place_free(character.x, character.y + functions.sign(vleft), wallmask)):  # we hit a ceiling or floor
			if(vleft>0):
				moveStatus = 0 # floors, not ceilings, reset moveStatus
		
			vleft = 0 # don't go up or down anymore
			character.vspeed = 0 # don't try it next frame, either
			collisionRectified = True
	

		if(hleft != 0 and not functions.place_free(character.x + functions.sign(hleft), character.y, wallmask)):  # we hit a wall on the left or right
			moveStatus = 0
			if(functions.place_free(character.x + functions.sign(hleft), character.y - 6, wallmask)):  # if we could just walk up the step
				character.y -= 6 # hop up the step.
			collisionRectified = True
	
#		elif(functions.place_free(character.x + functions.sign(hleft), character.y + 6, wallmask) and abs(character.hspeed) >= abs(character.vspeed)): # ceiling sloping
#	
#			character.y += 6
#			collisionRectified = True
	
		else: # it's not just a step, we've actually gotta stop
	
			hleft = 0 # don't go left or right anymore
			characterhspeed = 0 # don't try it next frame, either
			collisionRectified = True
	

	if(not collisionRectified and (abs(hleft) >= 1 or abs(vleft) >= 1)):
		# uh-oh, no collisions fixed, try stopping all vertical movement and see what happens
		charactervspeed = 0
		vleft = 0'''

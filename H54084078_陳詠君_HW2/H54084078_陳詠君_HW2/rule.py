"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    import random
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False    
        self.side = side
        self.ball_x = 0
        self.last_ball_x = 0
        self.ball_y = 0
        self.last_ball_y = 0
        self.des_x = 80             #75 is initial place

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"

        #if self.ball_served is False, serve the ball
        if not self.ball_served:    
            if scene_info["frame"] == 149:
                self.ball_served = True
                rand = self.random.randint(0, 1)
                if rand == 0:
                    #print("left")
                    return "SERVE_TO_LEFT"
                    #???command = "SERVE_TO_RIGHT"
                else:
                    return "SERVE_TO_RIGHT"
                    #print("right")
                    #???command = "SERVE_TO_RIGHT"

        #if self.ball_serve is true, move the plate
        else:                       
            #update the parmeters
            self.last_ball_x = self.ball_x
            self.last_ball_y = self.ball_y
            self.ball_x = scene_info["ball"][0]
            self.ball_y = scene_info["ball"][1]
            ball_vx = self.ball_x - self.last_ball_x
            ball_vy = self.ball_y - self.last_ball_y

            if self.side == "1P":
                #judge the ball's x destination
                if ball_vy > 0:                                             #ball go down
                    if ball_vx < 0:                                         #ball move left
                        self.des_x = self.ball_x - (420 - self.ball_y)
                    else:                                                       #ball move right
                        self.des_x = self.ball_x + (420 - self.ball_y)
                else:                                                           #ball move up  
                    if ball_vx < 0:
                        self.des_x = self.ball_x - (680 - (420 - self.ball_y))
                    else:
                        self.des_x = self.ball_x + (680 - (420 - self.ball_y))
                #adjest the destination into the scene
                while self.des_x > 200 or self.des_x < 0:
                    if self.des_x > 200:
                        self.des_x = (200 - (self.des_x - 200))
                    else:
                        self.des_x = -self.des_x
                #judge the cammand
                #print(scene_info["platform_1P"][0], self.des_x)
                if scene_info["frame"] <= 150:                                  
                    return "NONE"
                elif (scene_info["platform_1P"][1] > 410 and scene_info["platform_1P"][0] + 15 + 10 > self.des_x and scene_info["platform_1P"][0] + 15 - 10 < self.des_x):
                    return "NONE"                                               #when plate in the des_x plate don't move 
                elif scene_info["platform_1P"][0] + 15 < self.des_x:            #plate at ball's right, plate move left
                    return "MOVE_RIGHT"
                elif scene_info["platform_1P"][0] + 15 > self.des_x:
                    return "MOVE_LEFT"
                #else:
                    #return "NONE"
                #return command
            
            else:                                                               #if self.side == 2P
                #judge the ball's x destination
                if ball_vy < 0:                                             #ball move up
                    if ball_vx < 0:                                         #ball move left
                        self.des_x = self.ball_x - (self.ball_y - 80)
                    else:                                                       #ball move right   
                        self.des_x = self.ball_x + (self.ball_y - 80)
                else:                                                           #ball move down  
                    if ball_vx < 0:                                         #ball move left
                        self.des_x = self.ball_x - (680 - (self.ball_y - 80))
                    else:                                                       #ball move right
                        self.des_x = self.ball_x + (680 - (self.ball_y - 80))
                #adjest the destination into the scene
                while self.des_x > 200 or self.des_x < 0:
                    if self.des_x > 200:
                        self.des_x = (200 - (self.des_x - 200))
                    else:
                        self.des_x = -self.des_x
                #judge the cammand
                if scene_info["frame"] <= 150:
                    return "NONE"
                elif (scene_info["platform_2P"][1] < 60 and scene_info["platform_2P"][0] + 15 + 10 > self.des_x and scene_info["platform_2P"][0] + 15 - 10 < self.des_x):
                #elif scene_info["platform_1P"][1] <
                    return "NONE"                                               #when plate in the des_x plate don't move
                elif scene_info["platform_2P"][0] + 15 < self.des_x:            #plate at ball's right, plate move left
                    return "MOVE_RIGHT"
                elif scene_info["platform_2P"][0] + 15 > self.des_x:
                    return "MOVE_LEFT"
                #else:
                    #return "NONE"
                #return command
            
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

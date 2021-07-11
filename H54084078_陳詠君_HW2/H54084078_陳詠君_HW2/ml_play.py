"""
The template of the script for the machine learning process in game pingpong
"""
import random
import os.path
import pickle
class MLPlay:
    import random
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        filename = 'my_model1.pickle' #  mine_model_random1
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model1p = pickle.load(open(filepath, 'rb'))
        
        filename = 'my_model2.pickle' # mine_model_random2
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model2p = pickle.load(open(filepath, 'rb'))
        self.ball_served = False    
        self.side = side
        self.ball_x = 0
        self.last_ball_x = 0
        self.ball_y = 0
        self.last_ball_y = 0
        self.des_x = 80  

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        #if game pass pr game over -> reset
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
            self.des_x=80


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
                while self.des_x>200 or self.des_x < 0:
                    if self.des_x>200:
                        self.des_x=(200-(self.des_x-200))
                    else:
                        self.des_x = -self.des_x



               
                nx = scene_info["ball"][0]
                ny = scene_info["ball"][1]
                vx = scene_info["ball_speed"][0]
                vy = scene_info["ball_speed"][1]
                p1x = scene_info["platform_1P"][0]+15
                        #b = scene_info["blocker"][0]
                command = self.model1p.predict([[nx, ny, self.ball_x-self.last_ball_x,self.ball_y-self.last_ball_y,p1x,self.des_x]])

                if command == 0: return "NONE"
                elif command == 1: return "MOVE_LEFT"
                else: return "MOVE_RIGHT"

            else: 
                                                                  #2P
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
                while self.des_x>200 or self.des_x < 0:
                    if self.des_x>200:
                        self.des_x=(200-(self.des_x-200))
                    else:
                        self.des_x = -self.des_x

             
                nx = scene_info["ball"][0]
                ny = scene_info["ball"][1]
                vx = scene_info["ball_speed"][0]
                vy = scene_info["ball_speed"][1]
                p2x = scene_info["platform_2P"][0]+15
                        #b = scene_info["blocker"][0]
                command = self.model2p.predict([[nx, ny, self.ball_x-self.last_ball_x,self.ball_y-self.last_ball_y,p2x,self.des_x]])

                if command == 0: return "NONE"
                elif command == 1: return "MOVE_LEFT"
                else: return "MOVE_RIGHT"
   
            
                                                                         #if self.side == 2P

                

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

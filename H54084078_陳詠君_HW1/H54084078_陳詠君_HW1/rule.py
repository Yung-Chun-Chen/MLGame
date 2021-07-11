"""
The template of the main script of the machine learning process
"""
from random import seed,randint
import math
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False

    def update(self, scene_info):

        """
        Generate the command according to the received `scene_info`.
        """
        global current_ball_x,current_ball_y,des_x,last_ball_x,last_ball_y
        # Make the caller to invoke reset() for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"
        
        if not self.ball_served:
            self.ball_served = True
            seed()
            rand_val=randint(0,1)
            if rand_val==1:
                command="SERVE_TO_RIGHT"
            else:
                command = "SERVE_TO_LEFT"
        else:
            global current_ball_x
            global current_ball_y
            global des_x
            global last_ball_x
            global last_ball_y 
            #command = "MOVE_LEFT"   原始的程式碼
            
            print(scene_info)
            if scene_info["frame"]==0 or scene_info["frame"]==1:
                current_ball_x=scene_info["ball"][0]
                current_ball_y=scene_info["ball"][1]
                des_x = 100
            else:
                
                last_ball_x = current_ball_x
                last_ball_y = current_ball_y
                current_ball_x=scene_info["ball"][0]
                current_ball_y=scene_info["ball"][1]
                if current_ball_y>last_ball_y:
                    if current_ball_x>last_ball_x:
                        des_x=(400-current_ball_y)+current_ball_x	
                    else:
                        des_x=current_ball_x-(400-current_ball_y)
                if current_ball_y<last_ball_y:
                    des_x=100
                last_ball_x = scene_info["ball"][0]
                last_ball_y = scene_info["ball"][1]
                
            while des_x>200 or des_x<0:
                if des_x>200:
                    des_x=(200-(des_x-200))
                else:
                    des_x=-des_x
            a=randint(-15,15)
            des_x=des_x+a
            if des_x<scene_info["platform"][0]+25:
                command = "MOVE_LEFT"
            elif des_x>scene_info["platform"][0]+25:
                command = "MOVE_RIGHT"
            else:
                command = "NONE"   
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False



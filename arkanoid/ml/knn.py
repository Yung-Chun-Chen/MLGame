"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        filename = 'arkanoid_n3_20210309_knn_model.pickle'#arkanoid_n3_20210309_knn_
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ball_served = False
        self.current_ball_x = 0
        self.current_ball_y = 0
        self.last_ball_x = 0
        self.last_ball_y = 0
        self.des_x = 0
        self.des_vx = 0
        self.des_vy = 0

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"
        else:
            if scene_info["frame"]==0 or scene_info["frame"]==1:
                self.current_ball_x=scene_info["ball"][0]
                self.current_ball_y=scene_info["ball"][1]
                self.des_x = 100
            else:
                self.last_ball_x = self.current_ball_x
                self.last_ball_y = self.current_ball_y
                self.current_ball_x=scene_info["ball"][0]
                self.current_ball_y=scene_info["ball"][1]

                if self.current_ball_y>self.last_ball_y:
                    if self.current_ball_x>self.last_ball_x:
                        self.des_x=(400-self.current_ball_y)+self.current_ball_x	
                    else:
                        self.des_x=self.current_ball_x-(400-self.current_ball_y)
                if self.current_ball_y<self.last_ball_y:
                    self.des_x=80
                self.last_ball_x = scene_info["ball"][0]
                self.last_ball_y = scene_info["ball"][1]

            while self.des_x>200 or self.des_x < 0:
                if self.des_x>200:
                    self.des_x=(200-(self.des_x-200))
                else:
                    self.des_x = -self.des_x

            self.des_vx = self.current_ball_x - self.last_ball_x
            self.des_vy = self.current_ball_y - self.last_ball_y

            nx = scene_info["ball"][0]
            ny = scene_info["ball"][1]
            px = scene_info["platform"][0] + 20
            command = self.model.predict([[nx, ny, px,self.des_vx,self.des_vy,self.des_x]])

        if command == 0: return "NONE"
        elif command == 1: return "MOVE_LEFT"
        else: return "MOVE_RIGHT"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

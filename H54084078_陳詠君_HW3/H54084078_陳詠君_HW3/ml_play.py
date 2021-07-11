"""
The template of the script for playing the game in the ml mode
"""
import random
import os.path
import pickle
from random import seed,randint,random
import math
import numpy as np

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        filename = 'model.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))

        self.headx = 0
        self.heady = 0
        self.x_dir = 0
        self.y_dir = 0
        self.foodx = 0
        self.foody = 0
        self.current_x = 0
        self.current_y = 0
        self.last_x = 0
        self.last_y = 0
        
        self.wall_disx = 0
        self.wall_disy = 0

        self.direction = 0#上下左右 :1,2,3,4 
        self.wall = 0
        self.body = 0

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        snake_head = scene_info["snake_head"]
        food = scene_info["food"]

        if scene_info["frame"] == 0:
            
            self.current_x = snake_head[0]
            self.current_y = snake_head[1]
            self.last_x = snake_head[0]
            self.last_y = snake_head[1]
            self.x_dir = 0
            self.y_dir = 0

            self.wall_disx = 30
            self.wall_disx = 270
            self.body = 0
            self.wall = 0

            self.direction = 0 #上下左右 :1,2,3,4 

        else:
            snake_body = scene_info["snake_body"]
            snake_head = scene_info["snake_head"]
            food = scene_info["food"]
            self.body = 0
            self.wall = 0
            self.current_x = snake_head[0]
            self.current_y = snake_head[1]
            self.x_dir = self.current_x - self.last_x
            self.y_dir = self.current_y - self.last_y

            if self.x_dir > 0 and self.y_dir == 0:#right
                self.direction = 4
            if self.x_dir < 0 and self.y_dir == 0:#left
                self.direction = 3
            if self.x_dir == 0 and self.y_dir > 0:#down
                self.direction = 2
            if self.x_dir == 0 and self.y_dir < 0:#up
                self.direction = 1

            self.last_x = snake_head[0]
            self.last_y = snake_head[1]

            self.headx = snake_head[0]
            self.heady = snake_head[1]
            self.foodx = food[0]
            self.foody = food[1]

            if self.x_dir >0 and self.y_dir == 0:
                self.wall_disx = 300 - self.current_x
            elif self.x_dir<0 and self.y_dir == 0:
                self.wall_disx = self.current_x
            elif self.y_dir>0 and self.x_dir == 0:
                self.wall_disy = 300 - self.current_y
            elif self.y_dir<0 and self.x_dir == 0:
                self.wall_disy = self.current_y

            if self.y_dir == 0:
                self.wall_disy = max(300 - self.current_y,self.current_y)
            elif self.x_dir == 0:
                self.wall_disx = max(300 - self.current_x,self.current_x)

            if ((snake_head[0] > 285 and snake_head[1] > 285)or(snake_head[0] > 285 and snake_head[1] < 5) or (snake_head[0] < 5 and snake_head[1] > 285)or(snake_head[0] < 5 and snake_head[1] > 285)):
                #x方向移動
                if self.direction >= 3:
                    if snake_head[0] > 285:
                        if snake_head[1] > 285: #右下
                            self.wall = 1
                        if snake_head[1] < 5:#右上
                            self.wall = 2
                    if snake_head[0] < 5:
                        if snake_head[1] > 285:#左下
                            self.wall = 1
                        if snake_head[1] < 5:#左上
                            self.wall = 2
                #y方向移動
                if self.direction <= 2:
                    if snake_head[1] > 285:
                        if snake_head[0] > 285: #右下
                            self.wall = 3
                        if snake_head[0] < 5:#左下
                            self.wall = 4
                    if snake_head[1] < 5:
                        if snake_head[0] > 285:#右上
                            self.wall = 3
                        if snake_head[0] < 5:#左下
                            self.wall = 4          
            else:
                #x方向移動
                if self.direction >= 3:
                    if snake_head[0] >= 285:
                        if snake_head[1] > 145: #右下
                            self.wall = 1
                        else:#右上
                            self.wall = 2
                    if snake_head[0] < 5:
                        if snake_head[1] > 145:#左下
                            self.wall = 1
                        else:#左上
                            self.wall = 2
                #y方向移動
                if self.direction <= 2:
                    if snake_head[1] >= 285:
                        if snake_head[0] > 145: #右下
                            self.wall = 3
                        else:#左下
                            self.wall = 4
                    if snake_head[1] < 5:
                        if snake_head[0] > 145:#右上
                            self.wall = 3
                        else:#左上
                            self.wall = 4
       

            for i in range(0,len(snake_body)):
                if self.direction==3:#left
                    if(snake_head[0]==snake_body[i][0]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[1]==snake_body[i][1]+10):
                                self.body = 2
                            elif(snake_head[1]==snake_body[i][1]-10):
                                self.body = 1
                    if (snake_head[0]==snake_body[i][0]+10 and snake_head[1]==snake_body[i][1]): 
                        if(i!=len(snake_body)-1):
                            if(snake_head[1]+10==snake_body[i+1][1]):
                                self.body = 2
                            elif(snake_head[1]-10==snake_body[i+1][1]):
                                self.body = 1
                        
                    
                elif self.direction==4:#right 
                    if(snake_head[0]==snake_body[i][0]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[1]==snake_body[i][1]+10):
                                self.body = 2
                            elif(snake_head[1]==snake_body[i][1]-10):
                                self.body = 1
                    if (snake_head[0]==snake_body[i][0]-10 and snake_head[1]==snake_body[i][1]): # 
                       if(i!=len(snake_body)-1):
                            if(snake_head[1]+10==snake_body[i+1][1]):
                                self.body = 2
                            elif(snake_head[1]-10==snake_body[i+1][1]):
                                self.body = 1
                      
                            
                elif self.direction==1:#up
                    if(snake_head[1]==snake_body[i][1]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]==snake_body[i][0]+10):
                                self.body = 4
                            elif(snake_head[0]==snake_body[i][0]-10):
                                self.body = 3
                    if (snake_head[1]==snake_body[i][1]+10 and snake_head[0]==snake_body[i][0]): #
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]+10==snake_body[i+1][0]):
                                self.body = 4
                            elif(snake_head[0]-10==snake_body[i+1][0]):
                                self.body = 3
                        
                elif self.direction==2:#down
                    if(snake_head[1]==snake_body[i][1]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]==snake_body[i][0]+10):
                                self.body = 4
                            elif(snake_head[0]==snake_body[i][0]-10):
                                self.body = 3
                    if (snake_head[1]==snake_body[i][1]-10 and snake_head[0]==snake_body[i][0]): # 
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]+10==snake_body[i+1][0]):
                                self.body = 4
                            elif(snake_head[0]-10==snake_body[i+1][0]):
                                self.body = 3
                        

            command = self.model.predict([[self.headx, self.heady,self.direction,self.wall_disx,self.wall_disy,self.foodx,self.foody,self.body,self.wall]])
            #print(command)
            if command == 0: 
                return "UP"
            elif command == 1: 
                return "DOWN"
            elif command == 2: 
                return "LEFT"
            elif command == 3: 
                return "RIGHT"
            else: 
                return "NONE"


            
        

    def reset(self):
        """
        Reset the status if needed
        """
        pass


"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.direction = 0#上下左右 :1,2,3,4 
        self.current_x = 0
        self.current_y = 0
        self.last_x = 0
        self.last_y = 0
        self.x_dir = 0
        self.y_dir = 0
        #pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            snake_body = scene_info["snake_body"]
            #print(len(snake_body))
            return "RESET"

        snake_head = scene_info["snake_head"]
        food = scene_info["food"]
        snake_body = scene_info["snake_body"]

        if scene_info["frame"] == 0:
            self.direction = 0 #上下左右 :1,2,3,4 
            self.current_x = snake_head[0]
            self.current_y = snake_head[1]
            self.last_x = snake_head[0]
            self.last_y = snake_head[1]
            self.x_dir = 0
            self.y_dir = 0
        
        else:
            
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

            

            #print(self.direction,snake_head[0],snake_head[1])
            #四個角角
            if ((snake_head[0] > 285 and snake_head[1] > 285)or(snake_head[0] > 285 and snake_head[1] < 5) or (snake_head[0] < 5 and snake_head[1] > 285)or(snake_head[0] < 5 and snake_head[1] > 285)):
                #x方向移動
                if self.direction >= 3:
                    if snake_head[0] > 285:
                        if snake_head[1] > 285: #右下
                            return "UP"
                        if snake_head[1] < 5:#右上
                            return "DOWN"
                    if snake_head[0] < 5:
                        if snake_head[1] > 285:#左下
                            return "UP"
                        if snake_head[1] < 5:#左上
                            return "DOWN"
                #y方向移動
                if self.direction <= 2:
                    if snake_head[1] > 285:
                        if snake_head[0] > 285: #右下
                            return "LEFT"
                        if snake_head[0] < 5:#左下
                            return "RIGHT"
                    if snake_head[1] < 5:
                        if snake_head[0] > 285:#右上
                            return "LEFT"
                        if snake_head[0] < 5:#左下
                            return "RIGHT"            
            else:
                #x方向移動
                if self.direction >= 3:
                    if snake_head[0] >= 285:
                        if snake_head[1] > 145: #右下
                            return "UP"
                        else:#右上
                            return "DOWN"
                    if snake_head[0] < 5:
                        if snake_head[1] > 145:#左下
                            return "UP"
                        else:#左上
                            return "DOWN"
                #y方向移動
                if self.direction <= 2:
                    if snake_head[1] >= 285:
                        if snake_head[0] > 145: #右下
                            return "LEFT"
                        else:#左下
                            return "RIGHT"
                    if snake_head[1] < 5:
                        if snake_head[0] > 145:#右上
                            return "LEFT"
                        else:#左上
                            return "RIGHT"
            
            for i in range(0,len(snake_body)):
                if self.direction==3:#left
                    if(snake_head[0]==snake_body[i][0]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[1]==snake_body[i][1]+10):
                                return "DOWN"
                            elif(snake_head[1]==snake_body[i][1]-10):
                                return "UP"
                    if (snake_head[0]==snake_body[i][0]+10 and snake_head[1]==snake_body[i][1]): 
                        if(i!=len(snake_body)-1):
                            if(snake_head[1]+10==snake_body[i+1][1]):
                                return "DOWN"
                            elif(snake_head[1]-10==snake_body[i+1][1]):
                                return "UP"
                        
                    
                elif self.direction==4:#right 
                    if(snake_head[0]==snake_body[i][0]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[1]==snake_body[i][1]+10):
                                return "DOWN"
                            elif(snake_head[1]==snake_body[i][1]-10):
                                return "UP"
                    if (snake_head[0]==snake_body[i][0]-10 and snake_head[1]==snake_body[i][1]): # 
                       if(i!=len(snake_body)-1):
                            if(snake_head[1]+10==snake_body[i+1][1]):
                                return "DOWN"
                            elif(snake_head[1]-10==snake_body[i+1][1]):
                                return "UP"
                      
                            
                elif self.direction==1:#up
                    if(snake_head[1]==snake_body[i][1]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]==snake_body[i][0]+10):
                                return "RIGHT"
                            elif(snake_head[0]==snake_body[i][0]-10):
                                return "LEFT"
                    if (snake_head[1]==snake_body[i][1]+10 and snake_head[0]==snake_body[i][0]): #
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]+10==snake_body[i+1][0]):
                                return "RIGHT"
                            elif(snake_head[0]-10==snake_body[i+1][0]):
                                return "LEFT"
                        
                elif self.direction==2:#down
                    if(snake_head[1]==snake_body[i][1]):
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]==snake_body[i][0]+10):
                                return "RIGHT"
                            elif(snake_head[0]==snake_body[i][0]-10):
                                return "LEFT"
                    if (snake_head[1]==snake_body[i][1]-10 and snake_head[0]==snake_body[i][0]): # 
                        if(i!=len(snake_body)-1):
                            if(snake_head[0]+10==snake_body[i+1][0]):
                                return "RIGHT"
                            elif(snake_head[0]-10==snake_body[i+1][0]):
                                return "LEFT"
                        
                            
            
                   

            if snake_head[0] > food[0]:
                return "LEFT"
            elif snake_head[0] < food[0]:
                return "RIGHT"
            elif snake_head[1] > food[1]:
                return "UP"
            elif snake_head[1] < food[1]:
                return "DOWN"

    def reset(self):
        """
        Reset the status if needed
        """
        pass
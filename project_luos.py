from sys import *
from graphics import *
from random import *

#Summary: This program create a random maze using recursion and stack in python and used the Dijkstra’s algorithm to 
#find the shortest path from the starting point to the ending point including the keys along the way. 
#The starting point is red, it can be in any coordinate.
#The ending point is green and is always on the edge.
#The key is yellow
#Inorder to show the pathway clearly, the brown pathway is from the starting point to the key and the black pathway is from the key to the ending point 

class MyStack:
'''Create a class Stack that implements the regular operations of a stack. It is used for both building the maze and exploring
for the shortest path in the maze because both requires recursion to keep track of the cells visited and to back-track to 
previously visited cells when a deadend is reached'''
    def __init__(self):
        #Initiate empty list to store the cells
        pass #no action has to be performed

    def push(self,item,S):
        #Push an item which is the cell to the top of the stack S
        S.append(item)#Adds the cell to the top of the stack

    def isEmpty(self,S):
        #Gives the status or whether there are any cells in the stack S
        return len(S)==0#returns true if there are not cells stored in the stack and false if there are cells stored in the stack

    def pop(self,S):
        #Returns the most current cells stored in stack S and also cover the condition when there are no cells on the stack
        if len(S) == 0:#If there are no cells stored in the stack
            pass#Performs no action
        else:#If there are cells stored in the stack S
            return S.pop()#Returns the most recent cell from the stack and shortens the stack by one cell

    def size(self,S):
        #Gives the number of cells stored in stack S
        return len(S)#returns the number of cells stored in stack S


class Maze:
    '''
    The class Maze generates a maze and build the shortest path in the maze. In the case of building the maze, the cells in
    the maze that originally all have intact walls are pushed onto the stack and a wall between the current cell and a 
    neighbor is randomly taken down to create different paths. If the cell is at the boarder or have no neighbors with intact 
    walls then cells are poped off the stack to back up until another neighbor is available with intact walls. In the case for 
    exploring the shortest path, every cell along the path is kept track of until the path hits a deadend, at that point cells
    are poped off which means the path backs up until there is another path available and the stack also makes sure any visited
    paths will not be visited again. The shortest path will also include a key which must be pickted up to finish the maze.
    The generated maze is a N+2 by N+2 maze so that each side of the maze has an invisible boarder made up by cells to avoid 
    tedious special cases with boarderline cells.
    '''
    def __init__(self,N):
        #N is the dimension of the maze. This method initialize the maze to be a N+2 by N+2 maze where each side has 
        #an invisible boarder to cells to avoid tedious special cases addressing cells on the boarder
        self.N=N#Initiate the dimension of the maze to itself
        self.maze=[[i for i in range(N+2)]for i in range(N+2)]#Initiate the maze to N+2 by N+2 to avoid tedious special cases
        self.stack1=[]#Initiate the stack to store visited cells in the recursion to generate the maze
        self.stack2=[]#Initiate the stack to store visited cells in the recursion in Dijkstra's algorithm to search for the shortest path.
        self.pathToVictory = []#pathToVictory: initiate the list to store the shortest path(consisting of coordinates of cells)
        self.win = GraphWin('Maze', 900, 700)#Defines the size of the window where the maze would be drawn
        self.x1,self.y1=0,0#x1,y1: Initiate the x and y coordinates of the starting point which will be randomly generated
        self.x2,self.y2=0,0#x2,y2: Initiate the x and y coordinates of the ending point which will be randomly generated 
        self.solved = False#Initiate the maze as unsolved. The maze is not solved until a shortest path connects the starting and ending points.
        #Generate the predefined x and y coordinates for the cells in the maze
        for i in range(0,self.N+2):#for i in 1 .. maze size without the boarder
            for j in range(0,self.N+2):#for j in 1 .. maze size without the boarder
                self.maze[i][j]=Cell()#For each cell, initiate class Cell with its x and y coordinates
        #Sets all boarder cells to visited to avoid tedious special cases where a cell is on the boarder
        for i in range(0,self.N+2):#for i in 1 .. maze size without the boarder
            self.maze[0][i].visit()#Set all the West boarder cells to visited
            self.maze[i][0].visit()#Sets all South boarder cells to visited
            self.maze[self.N+1][i].visit()#Sets all East boarder cells to visited
            self.maze[i][self.N+1].visit()#Sets all North boarder cells to visited


    def genMaze(self):
    '''
    This method generate the maze by starting with a N by N grid where each cell has four walls intact. Starting from the lower
    left cell which is the first cell with a coordinate of 1,1 and randomly choosing neighbors cells to recursively knock down 
    the walls in-between the cells until none of the cells have its four walls intact. This is to make sure the maze is generated
    differently every time, every cell is reachable from the starting point and there exist one or more path from the starting to
    the ending point in the maze.
    '''
        self.perfectMaze=MyStack()#Initiate class MyStack to store cells in generating the maze
        totalCells=self.N*self.N#Sets the total number of sells to be NxN
        x,y=1,1 #Sets the initial value of x and y to 1 to identify coordinates for each cell but starting with the first cell on the lower left corner.
        visitedCells=1 #Initiate the number of visited cells to 1 because generating the maze starts in the lower left corner
        currentCell=self.maze[1][1] #Sets current cell to (1,1) to start in the lower left corner of the maze

        #Continuously build the maze by knocking down walls of cells through recursion until every cell in the maze is visited
        while visitedCells<totalCells:#Loops if the number of visited cells are smaller than the number of total cells in the maze
            intact=[]#Initiate the list to keep track of the the number of intact neighbors of each cell
            neighbors=[(x,y+1),(x+1,y),(x,y-1),(x-1,y)]#Four possible neighbors of the cell on the north, east, west and south sides.
            #For each cell, check all its four neibours to see if the neighbors are inside boarder of the maze
            for neighbor in neighbors:#for each of the four neighbors 
                if neighbor[0]>0 and neighbor[1]>0:#Make sure the coordinate of its neighbors are inside the minimum boarders of the maze
                    if neighbor[0]<=self.N and neighbor[1]<=self.N:#Make sure the coordinate of its neighbor is inside the maximum boarder of the maze
                        a,b=neighbor#a,b: the x,y coordinates of the neighbor
                        #If the neighbor has all four walls intact, add the neighbor to the intact list
                        if self.maze[a][b].checkNorth() and self.maze[a][b].checkSouth() and self.maze[a][b].checkWest() and self.maze[a][b].checkEast():#Checks if all walls are intact
                            intact.append(neighbor)#Add the qualified neighbor cells which has all its walls intact to the list
            #As long as there are one or more neighbors of the cell with all its walls intact, the construction of the maze continues which means
            #A random neighbor is choosen and one of its walls will be randomly knocked down.
            if len(intact)>0:#If there are one or more neighbors with all its walls intact
                randomNeighbor=randrange(0,len(intact))#Choose a random neighbor from the intact list
                c,d=intact[randomNeighbor]#c,d: The x and y coordinate of the random neighbor
                newCell=self.maze[c][d]#newCell: The random neighbor becomes the new cell that will be visited to look at its neighbors cell next
                #Knocks down the wall between the current cell and its random neighbor chosen
                if ((intact[randomNeighbor][0]-x)==0) and ((intact[randomNeighbor][1]-y)==1):#If the neighbor is above the current cell
                    currentCell.visitNorth()#Knock down the north wall of the current cell
                    newCell.visitSouth()#Knowck down the south wall of the neighbor cell
                    y+=1#Change the y coordinate so that the x,y coordinates are coordinates of the neighbor
                if ((intact[randomNeighbor][0]-x)==1) and ((intact[randomNeighbor][1]-y)==0):#If the neighbor is on the right of the current cell
                    currentCell.visitEast()#Knock down the east wall of the current cell
                    newCell.visitWest()#Knock down the west wall of the neighbor cell
                    x+=1#Change the x coordinate so that the x,y coordinates are coordinates of the neighbor
                if ((intact[randomNeighbor][0]-x)==0) and ((intact[randomNeighbor][1]-y)==-1):#If the neighbor is on the bottom of the current cell
                    currentCell.visitSouth()#Knock down the south wall of the current cell
                    newCell.visitNorth()#Knowck down the north wall of the neighbor cell
                    y-=1#Change the y coordinate so that the x,y coordinates are coordinates of the neighbor
                if ((intact[randomNeighbor][0]-x)==-1) and ((intact[randomNeighbor][1]-y)==0):#If the neighbor is on the left of the current cell
                    currentCell.visitWest()#Knock down the west wall of the current cell
                    newCell.visitEast()#Knowck down the east wall of the neighbor cell
                    x-=1#Change the x coordinate so that the x,y coordinates are coordinates of the neighbor
                newCell=self.maze[x][y]#newCell: The random neighbor becomes the new cell that will be visited to check its neighbors for intact walls
                self.perfectMaze.push((x,y),self.stack1)#Push the coordinate of the current cell into the stack in case a deadend is
                #reached where none of the neighbors of the cell has all its four walls intact. The stack will help the path 
                #back track until a cell is found to have one or more neighbor which have all its walls intact through recursion.
                currentCell=newCell#Sets current cell to new cell to visit the new cell
                visitedCells+=1#Increase the number of visited cell by 1
            #If the current cell do not have any neighbors with all its four walls intact, revisit the previous cell to check its
            #neighbors for intact wall and do so until a neighbor is found with all its walls intact
            else:
                newCell = self.stack1[0]#Set the new cell to the coordinate of the previous cell visited
                self.stack1 = self.stack1[1:len(self.stack1)]#Shorten the stack by one cell because of the backup
                x=newCell[0]#Get the x coordinate of the previous cell
                y=newCell[1]#Get the y coordinate of the previous cell
                newCell=self.maze[x][y]#Set the coordinate of the new cell to the previously visited cell
                currentCell=newCell#Set the previously visited cell as the current cell to backup
                
    def isSolved(self,x,y, endX, endY):
    '''Check to see if the current position equals to the end position to see if the maze is solved, this is when a path starting
    from the start point has reached the position of the end point.
    x and y and the coordinates of the last cell on the path and endX and endY are the coordinates of the ending point.
    '''
        if x==endX and y==endY:#If the coordinate of the current cell on the path is equal to the coordinate of the end point
            return True#maze is solved and the shortest path is found from the starting point to the ending point

    def ExploreHelper(self, x, y, endX, endY):
        '''
        This method implements Dijistra's algorithm to generate the shortest path between two points efficiently and fast
        without using up too much memory
        x,y: are the coordinate of the starting point
        endX, endU: are the coordinates of the ending point
        '''
        currentCell=self.maze[x][y]#Set current cell as the coordinate of the starting point
        self.path=MyStack()#Initiate stack class to store the path 
        currentCell.visit()#Set current cell as visited
        self.path.push((x,y),self.stack2)#Add the coordinate of the current cell onto the stack as the first point int he path

        #Check to see if the starting and ending point do not overlap
        if self.isSolved(x,y, endX, endY):#Check if current position is equal to the end position to see if the shortest path has already been found
            return #performs no action and returns control to the Explore method, this means the shortest path is found
        #Visit the north neighbor of the current cell if possible
        if not currentCell.checkNorth() and not self.maze[x][y+1].isVisited():#if the north has no wall, and is not visited
            self.ExploreHelper(x,y+1, endX, endY)#visit the north neighbor
        #If the north neighbor cannot be visited, try visiting the east neighbor of the current cell   
        elif not currentCell.checkEast() and not self.maze[x+1][y].isVisited():#if the east has no wall, and is not visited
            self.ExploreHelper(x+1,y, endX, endY)#visit the east neighbor
        #If the north and east neighbors cannot be visited, try visiting the south neighbor of the current cell   
        elif not currentCell.checkSouth() and not self.maze[x][y-1].isVisited():#if the south has no wall, and is not visited
            self.ExploreHelper(x,y-1, endX, endY)#visit the south neighbor
        #If the north, east and south neighbors cannot be visited, try visiting the west neighbor of the current cell   
        elif not currentCell.checkWest() and not self.maze[x-1][y].isVisited():#if the west has no wall, and is not visited
            self.ExploreHelper(x-1,y, endX, endY)#Visit the west neighbor
        #If none of the neighbors can be visited or dead end, return to the previous cell
        else:
            old = self.path.pop(self.stack2)#Return current coordinate
            old = self.path.pop(self.stack2)#Return the coordinate of the previous cell
            #If at the end of the maze and the ending point is also at the end, calling ExploreHelper will result in the maze been solved
            if old!=None:
                self.ExploreHelper(old[0],old[1], endX, endY)#Call the ExploreHelper again with the same two coordinates


    def Explore(self, x, y):
        '''
        This method uses Dijkstra’s algorithm in ExploreHelper to generate the shortest path from the starting point to the key 
        then finally to the ending point through the randomly generated maze to make sure the path is generated efficiently
        and quickly without using up too much memory
        x and y are the coordinates of the starting point
        '''
        #Generate the shortest path and draw the path to the key from the starting point
        endX = self.x3;#endX: the x coordinate of the key that is randomly generated, x3: the x coordinate of the key
        endY = self.y3;#endY: the y coordinate of the key that is randomly generated, y3: the y coordinate of the key
        self.ExploreHelper(x, y, endX, endY)#use ExploreHelper to generate path to the key from the starting point
        # draw the path from starting point to key
        for i in range(len(self.stack2)):#for i from 0 to the length of the path to the key
            dot=self.stack2[i]#get the x and y coordinte of the cell in the path
            self.drawDot(dot[0],dot[1],5,"brown")#draw a dot to indicate the coordinate along with a radius of 5 and in brown color
        
        #Generate the shortest path and draw the path from the key to the ending point
        endX = self.x2#endX: the x coordinate of the ending point that is randomly generated
        endY = self.y2#endY: the y coordinate of the ending that is randomly generated
        self.pathToVictory = self.stack2#Add the path from the starting point to the key as first part of the shortest path through the maze
        self.stack2=[]#reinitialize stack 2 to store the second part of the shortest path from the key to the ending point
        #Set all the cells in the maze as unvisited
        for i in range(1,self.N+1):#for i in 1 .. maze size with boarder
            for j in range(1,self.N+1):#for j in 1 .. maze size with boarder
                self.maze[i][j].unVisit()#Set cell to unvisited
        self.ExploreHelper(self.x3,self.y3,endX,endY)#use ExploreHelper to generate path from the key to the ending point
        self.stack2=self.stack2[1:len(self.stack2)]#To avoid repeating the starting point of key delete the first cell from the path
        # draw the path from key to ending point
        for i in range(len(self.stack2)):#for i from 0 to the length of the path to from the key to the ending point
            dot=self.stack2[i]#get the x and y coordiante of the cell in the path
            self.drawDot(dot[0],dot[1],3,"black")#draw a dot to indicate the coordinate along with a radius of 3 and in black color
            self.pathToVictory.append(dot)#add the coordinate of the cell to the shortest path 
        print(self.pathToVictory)#print the exit path from the starting point to the key and finally to the ending point



    def Draw(self):
        '''This method draws original generated random maze with all the boarder and all the cells in the maze showing
        which of the walls are intact. A red dot indicates the starting point, a yellow dot indicates the key and a
        green dot indicates the ending point.
        '''
        self.win.setBackground("white")#Set background to white
        self.x1,self.y1=randint(1,self.N),randint(1,self.N)#Generate random coordinates for the starting point
        self.x2,self.y2=randint(1,self.N),randint(1,self.N)#Generate random coordinates for the ending point
        self.x3,self.y3=randint(1,self.N),randint(1,self.N)#Generate random coordinates for the key

        #Makes sure the ending point is always on the edge of the maze to make the maze completable, otherwise generate another ending point
        while (self.x2!=1 and self.x2!=self.N) and (self.y2!=1 and self.y2!=self.N):#Check to see if the ending point in not on the edge of the maze
            self.x2,self.y2=randint(1,self.N),randint(1,self.N)#Generate another coordinate for the ending point until the ending point is on the edge
        #Makes sure the starting and ending points have different coordinates
        while (self.x1==self.x2 and self.y1==self.y2) :#Check to see that the coordinate of the starting point is equal to the coordinate of the ending point
            self.x1,self.y1=randint(1,self.N),randint(1,self.N)#Generate another coordinate for the starting point which does not have the same coordinate as the ending point
        #Make sure the key do not have the same coordinates as the starting or ending points
        while (self.x1==self.x3 and self.y1==self.y3) or (self.x2==self.x3 and self.y2==self.y3): #Check to see that key overlaps with starting or ending point
            self.x3,self.y3=randint(1,self.N),randint(1,self.N)#Generate another coodinate for the key which does not overlap with the coordinate of the starting or ending point
        
        #If exit at the ending point is on the top, knock down the north wall and the east or west wall if the exit is on a corner
        if self.y2==self.N:#If the exit is on the top
            if self.x2==self.N:#If the exit is on the top and most right
                self.maze[self.x2][self.y2].visitEast()#only knock down east wall
            elif self.x2==1:#If the exit is on the top and most left
                self.maze[self.x2][self.y2].visitWest()#only knock down west wall
            else:#If the exis is on the top but not on a corner of the maze
                self.maze[self.x2][self.y2].visitNorth()#Only knock down the north wall
        #If exit at the ending point is on the bottom, knock down the south wall and the east or west wall if the exit is on a corner        
        elif self.y2==1:#If the exit is on the bottom
            if self.x2==self.N:#If the exit is on the bottom and most right
                self.maze[self.x2][self.y2].visitEast()#only knock down east wall
            elif self.x2==1:#If the exit is on the bottom and most left
                self.maze[self.x2][self.y2].visitWest()#only knock down west wall
            else:#If exit is on the bottom but is not on any corners
                self.maze[self.x2][self.y2].visitSouth()#knock down the south wall
        #If exit is on the most right, knock down the east wall only because the previous two cases would have checked and knocked down other walls
        elif self.x2==self.N:#If the exit is on the right
            if self.y2==self.N:#If the exit is on the top right
                self.maze[self.x2][self.y2].visitEast()#The east wall is knocked down
            elif self.y2==1:#If the exit is on the bottom right most cell
                self.maze[self.x2][self.y2].visitEast()#knock down the east wall
            else:#If the exit is on the most right but is not on any corners
                self.maze[self.x2][self.y2].visitEast()##Knock down the east wall
        #If exit is on the most left, knock down the west wall only because the previous two cases would have checked and knocked down other walls
        elif self.x2==1:#If the exit in on the left
            if self.y2==self.N:#If the exit is on the top lefe
                self.maze[self.x2][self.y2].visitWest()#the west wall is knocked down
            elif self.y2==1:#If the exit is on the bottom left most cell
                self.maze[self.x2][self.y2].visitWest()#knock down the west wall
            else:#If the exit in the left but not on any corners
                self.maze[self.x2][self.y2].visitWest()#Knock down the west wall
        self.drawDot(self.x1,self.y1,8,"red")#Draw starting point
        self.drawDot(self.x2,self.y2,8,"green")#Draw ending point
        self.drawDot(self.x3,self.y3,8,"yellow")#Draw key


        #Draws the North walls vertically column by column where each cell has a length of 20
        x,y=10,self.N*20-10 #Sets initial values for x and y for the North walls for the first cell located at the top left corner
        #For each column draw the north wall of the cells if the wall is still intact
        for i in range(1, self.N + 1):#for i in 1 .. maze size with boarder
            for j in range(1, self.N + 1):#for j in 1 .. maze wize with boarder
                #Check if the North wall is intact. If true draw the north wall for the cell.
                if self.maze[i][j].checkNorth():#Check if the north wall is intact
                    wall = (Line(Point(x, y), Point(x + 20, y))).draw(self.win)#Draws the north wall of one cell with a width of 20
                x, y = x, y - 20 #Sets the position of the wall for the next wall in the row
            x, y = x + 20, self.N*20-10 #Sets the position of the wall for the next column

        #Draws the West walls vertically column by column
        x, y = 10, self.N*20+10 #Sets the initial x and y position for the West walls for the first cell located at top left corner
        #For each column draw the west wall of the cells if the wall is still intact        
        for i in range(1, self.N + 1):#for i in 1 .. maze size with boarder
            for j in range(1, self.N + 1):#for j in 1 .. maze size with boarder
                #Check if the West wall is standing. If true draw the north wall for the cell.
                if self.maze[i][j].checkWest():#Check if the north wall is intact
                    wall = (Line(Point(x, y), Point(x, y - 20))).draw(self.win)#Draws the West wall of one cell with a height of 20
                x, y = x, y-20  #Sets the position of the wall in the next column
            x, y = x+20, self.N*20+10 #Sets the position of the wall for the next row

        #Draws one wall at the bottom of the maze to be the the South wall of the last row of cells
        x, y = 10, self.N*20+10 #Sets the initial x and y position for the South walls to start from bottom
        #Draw the wall at the south boarder
        for i in range(1, self.N + 1): #for i in 1 .. maze size with boarder
            if self.maze[i][1].checkSouth():#Check if the South wall is standing. If true draw the South wall for the last row
                wall = (Line(Point(x, y), Point(x + 20, y))).draw(self.win)#Draws the South wall of one cell with the width of 20
            x, y = x + 20, y #Sets the position for the South wall of the next cell

        #Draws one wall at the right of the maze to the the East wall of the last column of cells
        x, y = self.N * 20 + 10, self.N*20+10 #Sets the initial x and y position for the East wall to start from the right
        #Draws the wall for the east boarder
        for i in range(1, self.N + 1):#for i in 1 .. maze size with boarder
            if self.maze[self.N][i].checkEast():#Check if the East wall is standing. If true draw the East wall for the right most column
                wall = (Line(Point(x, y), Point(x, y - 20))).draw(self.win)#Draws the East wall of one cell with the height of 20
            x, y = x, y - 20 #Sets the position for the East wall of the next cell

        return self.x1,self.y1 #Return the coordinate of the starting point for the Explore(self, x,y) method to use when finding the shortest path

    def drawDot(self,x,y,r,c):
        '''
        This method draws a dot with a radius and color that used to represent the starting point, the key, the ending point
        and the path which starts from the starting point crossing the key and ending in the ending point
        x and y is the coordiante of the dot to be drawn in the maze
        r is the radius of the dot
        c is the color of the dot
        '''
        #Draw a point given coordinate on grid and radius and color
        coord=Point(20*x,20*(self.N+1)-20*y)#Sets the position of the point to be in the middle of the cell
        circle = (Circle(coord,r))#draws the circle to represent the dot
        circle.setOutline(c)#Set color for the outline of the dot
        circle.setFill(c)#Set color to fill the dot
        circle.draw(self.win)#Draw the point on the window with the maze


class Cell:
    '''
    This class initiate the cells within the maze with its walls and status of the walls to indicate if the walls are still
    intact. It also has methods to set the cell to visited or unvisited and  gives the status of the cell to indicate if 
    the cell has been visited 
    '''
    
    #Initiate the four walls to be intact and the cell to be not visited
    def __init__(self):
        self.north=True#Set the north wall to intact
        self.south=True#Set the south wall to intact
        self.east=True#Set the east wall to intact
        self.west=True#Set the west wall to intact
        self.visited=False#Set the cell to not visited
    
    #Change the cell to visited
    def visit(self):
        self.visited=True #Set visited to True
        
    #Knock down the north wall     
    def visitNorth(self):
        self.north=False #Set status of the north wall to False (not intact)
    #Knock down the east wall    
    def visitEast(self):
        self.east=False#Set status of the east wall to False (not intact)
        
    #Knock down the west wall    
    def visitWest(self):
        self.west=False#Set status of the west wall to False (not intact)
    
    #Knock down the south wall
    def visitSouth(self):
        self.south=False#Set status of the south wall to False (not intact)
    
    #Check to see if the north wall is still intact
    def checkNorth(self):
        return self.north#Return the status of the north wall
    
    #Check to see if the south wall is still intact
    def checkSouth(self):
        return self.south#Return the status of the south wall
    
    #Check to see if the east wall is still intact
    def checkEast(self):
        return self.east#Return the status of the east wall
    
    #Check to see if the west wall is still intact
    def checkWest(self):
        return self.west#Return the status of the west wall
    
    #Check to see if the cell has been visited
    def isVisited(self):
        return self.visited#Return the status of whether the cell is visited
    
    #Set the cell to unvisited
    def unVisit(self):
        self.visited=False#Changed the visited status of the cell to False

def getInput():
    '''Get user input for dimensions of the maze which will be N by N. The user gets to decide the size of the maze. 
    However, because the program is written in recursion it is generally very slow to generate maze over the size 
    of 20 by 20. The maze will also be generated with an actual size of N+2 by N+2 to have an invisible boarder
    in order to simplify the calculation for the neighbors and the shortest path in the maze'''
    if len(argv)>1 and isinstance(eval(argv[1]),int):
    #Only if the user enters the appropriate dimension (maze is greaters than 1 by 1) and the user input is an integer, the
    #dimension N will be saved and returned in the function
        N=eval(argv[1])#Stores the N dimension of the maze inside N
    else:
    #If user input is incorrect or is being asked for the first time, repeated ask for user input for a dimension N
    #until user input is correct.
        N=eval(input("Please enter the dimension 'N' for the NxN maze:"))#Asks for user input for a dimension N
    return N #Returns the dimension of the maze

def main():
    """This program create a random maze using recursion and stack in python and used the Dijkstra’s algorithm to quickly 
    find the shortest path from the starting point to the ending point including the keys along the way. The program
    first receives an input from the user for the dimension, then initializes and generate a N by N maze, draws out
    the maze with a starting point, then discovers and marks the shortest path through the maze."""
    N=getInput()#Get user input for dimension of N by N maze, the maze will be a square matrix with side length of N
    output=Maze(N)#Initialize the maze with user specified dimensions of N by N
    output.genMaze()#Generate maze with user specified dimensions
    x=output.Draw()#Draw maze and return x which is the coordinates of the starting point
    a=x[0]#a is the x coordinate of the starting point x
    b=x[1]#a is the y coordinate of the starting point x
    output.Explore(a,b)#Expolore the shortest path in the maze from the starting to the finishing point
    output.win.getMouse()#Wait for user mouse input to draw the shortest path
    output.win.close()#Close window after the enitre shortest path is displayed on screen

main()

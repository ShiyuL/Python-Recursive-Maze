from sys import *
from graphics import *
from random import *

#Summary: This file create a random maze using recursion and stack in python and used the Dijkstra’s algorithm to 
#find the shortest path from the starting point to the ending point including the keys along the way. 
#The starting point is red, it can be in any coordinate.
#The ending point is green and is always on the edge.
#The key is yellow
#Inorder to show the pathway clearly, the brown pathway is from the starting point to the key and the black pathway is from the key to the ending point 

class MyStack:
#A stack that implements the push and pop operations
    def __init__(self):#Initiate empty list
        pass

    def push(self,item,S):#Push an item to the top of the stack
        S.append(item)

    def isEmpty(self,S):#returns True if there are no elements in S, otherwise return False
        return len(S)==0

    def pop(self,S):#Pop the top item
        if len(S) == 0:
            pass
        else:
            return S.pop()

    def size(self,S):#returns the number of elements in S
        return len(S)


class Maze:
    def __init__(self,N):#Initialize the maze to be a N+2 by N+2 maze to avoid tedious special cases
        self.N=N#Initiate the dimension of the maze to itself
        self.maze=[[i for i in range(N+2)]for i in range(N+2)]#Initiate the maze to N+2 by N+2 to avoid tedious special cases
        self.stack1=[]
        self.stack2=[]
        self.pathToVictory = []
        self.win = GraphWin('Maze', 900, 700)#Defines the size of the window
        self.x1,self.y1=0,0
        self.x2,self.y2=0,0
        self.solved = False
        self.trace = []
        for i in range(0,self.N+2):#Generate the x coordinates of the cells
            for j in range(0,self.N+2):#Generate the y coordinates of the cells
                self.maze[i][j]=Cell()#For each cell, initiate class Cell
        for i in range(0,self.N+2):#Sets all border cells to visited
            self.maze[0][i].visit()
            self.maze[i][0].visit()
            self.maze[self.N+1][i].visit()
            self.maze[i][self.N+1].visit()


    def genMaze(self):#Generates the perfect maze
        self.perfectMaze=MyStack()#Initiate class MyStack
#        stack=self.perfectMaze.push(self.maze[1][1],self.perfectMaze)
        totalCells=self.N*self.N#Sets the total number of sells to be NxN
        x,y=1,1 #Sets the initial value of x and y to 1
        #self.maze[1][1].checkVisit()#Change cell (1,1) to visited
        visitedCells=1 #Initiate the number of visited cells to 1
        currentCell=self.maze[1][1] #Sets current cell to (1,1)

        while visitedCells<totalCells:#Loops if the number of visited cells are smaller than the number of total cells
            #print("old",x,y)
            intact=[]#Initiate the list for the number of intact neighbors
            neighbors=[(x,y+1),(x+1,y),(x,y-1),(x-1,y)]#Four possible neighbors of the cell
            for neighbor in neighbors:#Checks each neighbor to see if they satisfy conditions
                if neighbor[0]>0 and neighbor[1]>0:#Make sure the coordinate of the neighbor is inside the maze
#                    print(neighbor[0],neighbor[1])
                    if neighbor[0]<=self.N and neighbor[1]<=self.N:#Make sure the coordinate of the neighbor is inside the maze
                        a,b=neighbor#Gets the x,y coordinates of the neighbor
                        if self.maze[a][b].checkNorth() and self.maze[a][b].checkSouth() and self.maze[a][b].checkWest() and self.maze[a][b].checkEast():#Checks if all walls are intact
                            intact.append(neighbor)#Add the qualified neighbor cells which has all its walls intact to the list
            #print(intact)
            if len(intact)>0:#If there are one or more neighbors with all its walls intact
                randomNeighbor=randrange(0,len(intact))#Choose a random neighbor
                c,d=intact[randomNeighbor]#Get the x and y coordinate of the random neighbor
                newCell=self.maze[c][d]#Sets the random neighbor to the cell that will be explored
                if ((intact[randomNeighbor][0]-x)==0) and ((intact[randomNeighbor][1]-y)==1):#If the neighbor is above the current cell
                    currentCell.visitNorth()#Knock down the north wall of the current cell
                    newCell.visitSouth()#Knowck down the south wall of the neighbor cell
                    y+=1#Change the y coordinate so that the x,y coordinates are coordinates of the neighbor
                if ((intact[randomNeighbor][0]-x)==1) and ((intact[randomNeighbor][1]-y)==0):#If the neighbor is on the right of the current cell
                    currentCell.visitEast()#Knock down the east wall of the current cell
                    newCell.visitWest()#Knowck down the west wall of the neighbor cell
                    x+=1#Change the x coordinate so that the x,y coordinates are coordinates of the neighbor
                if ((intact[randomNeighbor][0]-x)==0) and ((intact[randomNeighbor][1]-y)==-1):#If the neighbor is on the bottom of the current cell
                    currentCell.visitSouth()#Knock down the south wall of the current cell
                    newCell.visitNorth()#Knowck down the north wall of the neighbor cell
                    y-=1#Change the y coordinate so that the x,y coordinates are coordinates of the neighbor
                if ((intact[randomNeighbor][0]-x)==-1) and ((intact[randomNeighbor][1]-y)==0):#If the neighbor is on the left of the current cell
                    currentCell.visitWest()#Knock down the west wall of the current cell
                    newCell.visitEast()#Knowck down the east wall of the neighbor cell
                    x-=1#Change the x coordinate so that the x,y coordinates are coordinates of the neighbor
                #print("new",x,y)
                newCell=self.maze[x][y]#Sets new cell
                #self.maze[x][y].checkVisit()
                self.perfectMaze.push((x,y),self.stack1)#Push the coordinate of the current cell into the stack
                #print("size of stack",perfectMaze.size([]))
                #print(currentCell.checkNorth(),currentCell.checkWest(),currentCell.checkEast(),currentCell.checkSouth())
                #print(newCell.checkNorth(),newCell.checkWest(),newCell.checkEast(),newCell.checkSouth())
                currentCell=newCell#Sets current cell to new cell
                visitedCells+=1#Increase the number of visited cell by 1
            else:
                #print("check if stack is empty",perfectMaze.isEmpty([]))#Check if stack is empty
                newCell = self.stack1[0]#Pop out the previous coordinates from the stack as a tuple
                self.stack1 = self.stack1[1:len(self.stack1)]
                x=newCell[0]#Get the x coordinate of the previous cell
                y=newCell[1]#Get the y coordinate of the previous cell
                newCell=self.maze[x][y]#the old cell becomes the new cell
                currentCell=newCell#the new cell becomes the current cell
    def isSolved(self,x,y, endX, endY):#Check to see if the current position equals to the end position
        if x==endX and y==endY:
            return True

    def ExploreHelper(self, x, y, endX, endY):
        currentCell=self.maze[x][y]#Set current cell
        self.path=MyStack()#Initiate stack
        currentCell.visit()#Set current cell as visited
        self.path.push((x,y),self.stack2)#Add the position of the current cell onto the stack

        if self.isSolved(x,y, endX, endY):#Check if current position is equal to the end position
            return
        if not currentCell.checkNorth() and not self.maze[x][y+1].isVisited():#if the north has no wall, and is not visited
            self.ExploreHelper(x,y+1, endX, endY)
        elif not currentCell.checkEast() and not self.maze[x+1][y].isVisited():#if the east has no wall, and is not visited
            self.ExploreHelper(x+1,y, endX, endY)
        elif not currentCell.checkSouth() and not self.maze[x][y-1].isVisited():#if the south has no wall, and is not visited
            self.ExploreHelper(x,y-1, endX, endY)
        elif not currentCell.checkWest() and not self.maze[x-1][y].isVisited():#if the west has no wall, and is not visited
            self.ExploreHelper(x-1,y, endX, endY)
        else:#If dead end, return to the previous cell
            old = self.path.pop(self.stack2)#Return current position
            old = self.path.pop(self.stack2)#Return previous step
            if old!=None:
                self.ExploreHelper(old[0],old[1], endX, endY)#If at the end of the maze and the ending point is also at the end


    def Explore(self, x, y):
        
#use self.explore to go to the key from the starting point
        endX = self.x3;
        endY = self.y3;
        self.ExploreHelper(x, y, endX, endY)
        # draw dots from starting point to key
        for i in range(len(self.stack2)):
            dot=self.stack2[i]
            self.drawDot(dot[0],dot[1],5,"brown")
        #use self.explore to go to the ending point from the key
        endX = self.x2
        endY = self.y2
        self.pathToVictory = self.stack2
        self.stack2=[]#reinitialize stack 2
        for i in range(1,self.N+1):
            for j in range(1,self.N+1):
                self.maze[i][j].unVisit()#Set all cells to unvisited
        self.ExploreHelper(self.x3,self.y3,endX,endY)
        self.stack2=self.stack2[1:len(self.stack2)]#To avoid repeating the starting point of key
        # draw dots from key to ending point
        for i in range(len(self.stack2)):
            dot=self.stack2[i]
            self.drawDot(dot[0],dot[1],3,"black")
            self.pathToVictory.append(dot)
        #print the exit path
        print(self.pathToVictory)



    def Draw(self):
        #This method draws the maze
        self.win.setBackground("white")#Set background to white
        self.x1,self.y1=randint(1,self.N),randint(1,self.N)#Generate random coordinates for the starting point
        self.x2,self.y2=randint(1,self.N),randint(1,self.N)#Generate random coordinates for the ending point
        self.x3,self.y3=randint(1,self.N),randint(1,self.N)#Generate random coordinates for the key

        # ending point is always on the edge of the maze
        while (self.x2!=1 and self.x2!=self.N) and (self.y2!=1 and self.y2!=self.N):#Check to see if the ending point in on the edge of the maze, if not then reshuffle
            self.x2,self.y2=randint(1,self.N),randint(1,self.N)

        while (self.x1==self.x2 and self.y1==self.y2) :#Check to seee that the coordinate of the starting point does not equal to the coordinate of the ending point
            self.x1,self.y1=randint(1,self.N),randint(1,self.N)

        while (self.x1==self.x3 and self.y1==self.y3) or (self.x2==self.x3 and self.y2==self.y3): #Check to see that key does not overlap with starting or ending point
            self.x3,self.y3=randint(1,self.N),randint(1,self.N)

        if self.y2==self.N:#If exit is on the top, knock down the northwall
            if self.x2==self.N:#If the exit is on the top and most right, only knock down east wall
                self.maze[self.x2][self.y2].visitEast()
            elif self.x2==1:#If the exit is on the top and most left, only knock down west wall
                self.maze[self.x2][self.y2].visitWest()
            else:
                self.maze[self.x2][self.y2].visitNorth()#If exit is on the top, knock down the north wall
        elif self.y2==1:#If exit is on the bottom, knowck down the southwall
            if self.x2==self.N:#If the exit is on the bottom and most right, only knock down east wall
                self.maze[self.x2][self.y2].visitEast()
            elif self.x2==1:#If the exit is on the bottom and most left, only knock down west wall
                self.maze[self.x2][self.y2].visitWest()
            else:#If exit is on the bottom, knock down the south wall
                self.maze[self.x2][self.y2].visitSouth()
        elif self.x2==self.N:#If exit is on the most right, knock down the east wall
            if self.y2==self.N:#If the exit is on the top right, only the east wall is knocked down
                self.maze[self.x2][self.y2].visitEast()
            elif self.y2==1:#If the exit is on the bottom right most cell, knock down the east wall
                self.maze[self.x2][self.y2].visitEast()
            else:#Knock down the west wall
                self.maze[self.x2][self.y2].visitEast()
        elif self.x2==1:#If exit is on the most left, knock down the west wall
            if self.y2==self.N:#If the exit is on the top left, only the west wall is knocked down
                self.maze[self.x2][self.y2].visitWest()
            elif self.y2==1:#If the exit is on the bottom left most cell, knock down the west wall
                self.maze[self.x2][self.y2].visitWest()
            else:#Knock down the west wall
                self.maze[self.x2][self.y2].visitWest()
        self.drawDot(self.x1,self.y1,8,"red")#Draw starting point
        self.drawDot(self.x2,self.y2,8,"green")#Draw ending point
        self.drawDot(self.x3,self.y3,8,"yellow")#Draw key


        #Draws the North walls vertically column by column
        x,y=10,self.N*20-10 #Sets initial values for x and y for the North walls
        for i in range(1, self.N + 1):#Sets the number of columns
            for j in range(1, self.N + 1):#Sets number of walls in each column
                #print(i,j)
                if self.maze[i][j].checkNorth():#Check if the North wall is standing. If true draw the north wall for the cell.
                    wall = (Line(Point(x, y), Point(x + 20, y))).draw(self.win)#Draws the north wall of one cell with a width of 20
                x, y = x, y - 20 #Sets the position for the next wall in the row
            x, y = x + 20, self.N*20-10 #Sets the position for the next column

        #Draws the West walls vertically column by column
        x, y = 10, self.N*20+10 #Sets the initial x and y position for the West walls

        for i in range(1, self.N + 1):#Sets the number of columns
            for j in range(1, self.N + 1):#Sets number of walls in each column
                #print(i,j)
                if self.maze[i][j].checkWest():#Check if the West wall is standing. If true draw the north wall for the cell.
                    wall = (Line(Point(x, y), Point(x, y - 20))).draw(self.win)#Draws the West wall of one cell with a height of 20
                x, y = x, y-20  #Sets the position of the wall in the next column
            x, y = x+20, self.N*20+10 #Sets the position for the next row

        #Draws one wall at the bottom of the maze to be the the South wall of the last row of cells
        x, y = 10, self.N*20+10 #Sets the initial x and y position for the South walls to start from bottom
        for i in range(1, self.N + 1): #Sets the number of walls in the bottom row
            if self.maze[i][1].checkSouth():#Check if the South wall is standing. If true draw the South wall for the last row
                wall = (Line(Point(x, y), Point(x + 20, y))).draw(self.win)#Draws the South wall of one cell with the width of 20
            x, y = x + 20, y #Sets the position for the South wall of the next cell

        #Draws one wall at the right of the maze to the the East wall of the last column of cells
        x, y = self.N * 20 + 10, self.N*20+10 #Sets the initial x and y position for the East wall to start from the right
        for i in range(1, self.N + 1):#Sets the number of walls in the right most column
            if self.maze[self.N][i].checkEast():#Check if the East wall is standing. If true draw the East wall for the right most column
                wall = (Line(Point(x, y), Point(x, y - 20))).draw(self.win)#Draws the East wall of one cell with the height of 20
            x, y = x, y - 20 #Sets the position for the East wall of the next cell

        return self.x1,self.y1 #Return the coordinate of the starting point

    def drawDot(self,x,y,r,c):
        #Draw a point given coordinate on grid and radius and color
        coord=Point(20*x,20*(self.N+1)-20*y)#Sets the position of the point
        circle = (Circle(coord,r))
        circle.setOutline(c)#Set color of point
        circle.setFill(c)#Set color of the point
        circle.draw(self.win)#Draw the point


class Cell:
    def __init__(self):#Initiate the boolean value of the walls
        self.north=True
        self.south=True
        self.east=True
        self.west=True
        self.visited=False

    def visit(self):#Change the cell to visited
        self.visited=True
    def visitNorth(self):#Knock down the north wall
        self.north=False
    def visitEast(self):#Knock down the east wall
        self.east=False
    def visitWest(self):#Knock down the west wall
        self.west=False
    def visitSouth(self):#Knock down the south wall
        self.south=False
    def checkNorth(self):#Check to see if the north wall is still intact
        return self.north
    def checkSouth(self):#Check to see if the south wall is still intact
        return self.south
    def checkEast(self):#Check to see if the east wall is still intact
        return self.east
    def checkWest(self):#Check to see if the west wall is still intact
        return self.west
    def isVisited(self):#Check to see if the cell has been visited
        return self.visited
    def unVisit(self):
        self.visited=False

def getInput():#Get user input for dimensions of the maze
    if len(argv)>1 and isinstance(eval(argv[1]),int):
        N=eval(argv[1])
    else:
        N=eval(input("Please enter the dimension 'N' for the NxN maze:"))
    return N

def main():#Initialize maze
    N=getInput()#Get user input for dimension
    output=Maze(N)#Initialize maze
    output.genMaze()#Generate maze
    x=output.Draw()#Draw maze and return coordinate of the starting point
    a=x[0]#The x coordinate of the starting point
    b=x[1]#The y coordinate of the starting point
    output.Explore(a,b)#Initialize explore
    output.win.getMouse()#Wait for user mouse input
    output.win.close()#Close window

main()

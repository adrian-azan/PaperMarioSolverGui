class Tile:

    def __init__(self):
        self.foward = None
        self.cw = None
        self.full = False
        self.id = None
    

    

class Arena:
    
    def __init__(self):
        self.rings = list()
        count = 1
        
        #Creates 4 circular linked lists
        for ring in range(0,4):
            self.rings.append(Tile())
            currentTile = self.rings[ring]

            for tile in range(0,11):
                currentTile.cw = Tile()
                currentTile.id = count
                count += 1
                currentTile = currentTile.cw

            currentTile.id = count
            count+=1
            currentTile.cw = self.rings[ring]

        column = list()
        columnAcross = list()

        for i in range(0,4):
            column.append(self.rings[i])
            columnAcross.append(self.rings[i])
            for k in range(0,6):
                columnAcross[i] = columnAcross[i].cw

        """
        Creates outer and inner connection 
	between each tile foward rings
	Allows outer ring to wrap around
	"""
        for col in range(0,6):
            for i in range (3,0,-1):
                column[i].foward = column[i-1]

            column[0].foward = columnAcross[0]

            for i in range(0,3):
                columnAcross[i].foward = columnAcross[i+1]

            columnAcross[3].foward = column[3]

            for i in range(0,4):
                column[i] = column[i].cw
                columnAcross[i] = columnAcross[i].cw


    def solveArena(self):
        if self.solveArenaSlide("", 3) == True:
            return
        self.solveArenaRotate("",3)

    def solveArenaRotate(self,moves, moveCount):

        if (self.isSolved() == True):
            print("SOLUTION: " , moves)
            return True

        if moveCount <= 0:
            return False

        moveSlide = ""
        move = ""

        for ring in range(4):
            for amount in range(1,12):

                if self.isRingEmpty(ring) == False:
                    self.rotate(ring,amount)
                    move = "R"+ str(ring) + ":" + str(amount) + " "
                    moves += move
                    moveCount -=1
                    if self.solveArenaRotate(moves,moveCount):
                        return True

                for column in range(6):
                    for amountCol in range(1,8):
                        if moveCount >= 1 and self.isColEmpty(column) == False:                            
                            self.slide(column, amountCol)
                            moveSlide = "S" + str(column) + ":" + str(amountCol) + " "
                            moves += moveSlide

                            moveCount -= 1
                            if self.solveArenaRotate(moves,moveCount):
                                return True

                            moveCount += 1
                            self.slide(column, 8-amountCol)
                            moves = moves[:len(moves)-len(moveSlide)]

                if self.isRingEmpty(ring) == False:
                    moveCount += 1
                    self.rotate(ring, 12-amount)
                    moves = moves[:len(moves)-len(move)]

        return False

    def solveArenaSlide(self,moves, moveCount):
        if (self.isSolved() == True):
            print("SOLUTION: " , moves)
            return True

        if moveCount <= 0:
            return False

        moveSlide = ""
        move = ""

        for column in range(6):
            for amountCol in range(1,8):
                if self.isColEmpty(column) == False:
                    self.slide(column, amountCol)
                    moveSlide = "S" + str(column) + ":" + str(amountCol) + " "
                    moves += moveSlide

                    moveCount -=1
                    if self.solveArenaSlide(moves,moveCount) == True:
                        return True

                    for ring in range(4):
                        for amount in range(1,12):
                            if moveCount >= 1 and self.isRingEmpty(ring):
                                self.rotate(ring,amount)
                                move = "R"+ str(ring) + ":" + str(amount) + " "
                                moves += move
                                if self.solveArenaSlide(moves,moveCount) == True:
                                    return True

                                self.rotate(ring, 12-amount)
                                moves = moves[:len(moves)-len(move)]

                    moveCount += 1
                    self.slide(column, 8-amountCol)
                    moves = moves[:len(moves)-len(moveSlide)]


        return False            



        

    def isSolved(self):
        squareCheck = [0]*12
        lineCheck = [0]*12

        for i in range(12):
            lineCheck[i] = self.checkLine(i)

        i = 0
        while i < 12:            
            squareCheck[i] = self.checkSquare(i)

            if i != 11 and lineCheck[i] == False and squareCheck[i] == True:
                squareCheck[i+1] = True               
                i = i+1

            if i == 11 and squareCheck[i] == True:
                squareCheck[0] = True               
            i+=1
        
        for i in range(12):
            if squareCheck[i] == False and lineCheck[i] == False:
                return False

        return True

    def checkLine(self,col):
        column = self.rings[3]
        if (col >5):
            column = self.rings[0]

        for i in range(col):
            column = column.cw

        goal = column.full

        for i in range(4):
            if column.full != goal:
                return False
            column = column.foward

        return True

    def checkSquare(self,col):
        column = self.rings[1]
        if (col >5):
            column = self.rings[0]

        for i in range(col):
            column = column.cw

        if col == 5 or col == 11:
            split = column.foward.cw
            if column.full == False or column.foward.full == False\
               or split.full == False or split.foward.full == False:
                return False
            return True

        for i in range(2):
            if column.full == False or column.foward.full == False:
                return False
            column = column.cw
        return True
        

    def isColEmpty(self,col):
        currentTile = self.rings[3]

        for i in range(col):
            currentTile = currentTile.cw

        for i in range(8):
            if currentTile.full == True:
                return False
            currentTile = currentTile.foward

        return True

    def isRingEmpty(self,ring):
        currentTile = self.rings[ring]

        for i in range(12):
            if currentTile.full == True:
                return False
            currentTile = currentTile.cw

        return True
    

    def rotate(self,ring,amount):
        if ring < 0 or ring >= 4 or self.isRingEmpty(ring):
            return

        currentTile = self.rings[ring]
        enemyPos = list()
        enemyNewPos = [0]*12

        for i in range(0,12):
            enemyPos.append(currentTile.full)
            currentTile = currentTile.cw

        for i in range(0,12):
            newSpace = (i+amount)%12
            enemyNewPos[newSpace] = enemyPos[i]

        currentTile = self.rings[ring]
        for i in range(0,12):
            currentTile.full = enemyNewPos[i]
            currentTile = currentTile.cw
            

    def slide(self,col,amount):
        if col < 0 or col >= 6 or self.isColEmpty(col):
            return

        enemies = [0]*8
        enemyNewPos = [0]*8
        newSpace = 0

        currentCol = self.rings[3]
        for i in range(0,col):
            currentCol = currentCol.cw

        temp = currentCol
        for i in range(0,8):
            enemies[i] = temp.id
            temp = temp.foward

        for i in range(0,8):
            newSpace = (i+amount)%8
            enemyNewPos[newSpace] = enemies[i]

        for i in range(0,8):
            currentCol.id = enemyNewPos[i]
            currentCol = currentCol.foward


    def setRing(self, ring,enemies):
        if ring < 0 or ring>= 4:
            return

        tile = self.rings[ring]
        for i in range(12):
            tile.full = enemies[i]
            tile = tile.cw

    def setCol(self,col,enemies):
        if col < 0 or col >= 6:
            return

        tile = self.rings[3]
        for i in range(col):
            tile = tile.cw

        for i in range(8):
            tile.full = enemies[i]
            tile = tile.foward

    def printRings(self):
        for i in range(3,-1,-1):
            currentTile = self.rings[i]
            print(i,": ", end="")

            for col in range(0,12):
                print(currentTile.full," ", end="")
                currentTile = currentTile.cw
            print()

    def printColumns(self):
        currentCol = self.rings[3]
        currentTile = currentCol

        for col in range(0,6):
            for tile in range(0,8):
                print(currentTile.id," ", end="")
                currentTile = currentTile.foward

            print()
            currentCol = currentCol.cw
            currentTile = currentCol
            



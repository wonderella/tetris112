from cmu_graphics import *
import random

# Hi! So um I like...had too much fun with this. Here are some of the
# other things that I did.

# 1. I made it a little prettier... it's now on a black background
# and I changed some fonts and colors 

# 2. There's an animation for game over! It fills the board from bottom 
# to top with white. I felt like that was something I've seen on tetris games

# 3. There are levels! Every 10 lines cleared moves to the next level where 
# the speed increases by half a step per second...one step felt too fast
# but maybe I'm also bad.
# Also it tells you "Level Up!" keeps track of the levels and lines cleared 
# on the side

# 4. When you hover over the restart game button it highlights...very small
# but I thought it was cool

# 5. There's an icon to show the next tetris block that's coming up on the side.

# 6. When researching point structures I found out it's called "Tetris!" when you
# clear four lines at once. So when you get a "Tetris" it tells you

# 7. When you get points, the score is highlighted for a couple seconds

# 8. There's a small highscore board on the game over screen that keeps track
# of the last top 5 scores

def onAppStart(app):
    app.highScores = []
    resetApp(app)
    
def resetApp(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 0
    app.boardTop = 0
    app.boardWidth = 280
    app.boardHeight = 400
    app.cellBorderWidth = 0.5   
    app.isPaused = False
    app.background = 'black'
    app.font = 'orbitron'
    
    app.stepsPerSecond = 2
    app.steps = 0
    
    #game over functions
    app.gameOver = False
    app.gameOverSteps = 0
    app.finishScreen = False
    app.isSelected = False
    
    #score functions
    app.points = 0
    app.scoreAdd = False
    app.scoreSteps = 0
    
    app.tetris = False
    app.tetrisSteps = 0
    
    #leveling up functions
    app.clearedLines = 0
    app.level = 1
    app.levelUp = False
    app.levelUpSteps = 0
    

    # Create the board:
    app.board = [([None] * app.cols) for row in range(app.rows)]
    
    
    #piece functions
    loadTetrisPieces(app)
    
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    
    loadNextPiece(app)
    

    
    
def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'lightCoral', 'lemonChiffon', 'lavender', 'pink',
                              'lightSkyBlue', 'mediumAquamarine', 'peachPuff' ]
    
    
    
def loadPiece(app, pieceIndex):
    app.pieceIndex = pieceIndex
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceTopRow = 0
    
    pieceCols = len(app.piece[0])
    
    app.pieceLeftCol = (app.cols - pieceCols)//2
    
    if not pieceIsLegal(app):
        app.gameOver = True
        app.highScores.append(app.points)
        app.highScores.sort(reverse=True)

def loadNextPiece(app):
    pieceIndex = app.nextPieceIndex
    nextPiece = random.randrange(len(app.tetrisPieces))
    app.nextPieceIndex = nextPiece
    loadPiece(app, pieceIndex)

########### 

def redrawAll(app):
    if app.finishScreen:
        drawLabel(f'Final Score: {app.points}', app.width//2, 85, size=16, fill='white', font=app.font)
        drawLabel('Game Over!', app.width//2, app.height//2 - 10, size=50, fill='white', font=app.font)
        
        drawRect(app.width//2 - 110, app.height//2 + 20, 220, 25, fill=None)
        drawLabel('Click Here to Play Again!', app.width//2, app.height//2 + 30, size=16, fill='white', bold=app.isSelected, font=app.font)
        
        drawHighScores(app)
    
    else:
        drawLabel(f'Score: {app.points}', 340, 40, size=16, fill='white', font=app.font, bold=app.scoreAdd)
        drawLabel(f'Level: {app.level}', 340, 80, size=16, fill='white', font=app.font)
        drawLabel(f'Lines: {app.clearedLines}', 340, 380, size=16, fill='white', font=app.font)
    
        drawLabel('Next Piece:', 340, 170, size=16, fill='white', font=app.font)
        drawRect(340, 230, 90, 90, fill=None, border='gray', align='center')
        
        
        drawBoard(app)
        drawBoardBorder(app)
        
        if not app.gameOver:
            drawNextPiece(app)
            drawPiece(app)
        
    if app.tetris:
        drawLabel('Tetris!', 140, 90, size=20, fill='white', font=app.font, bold=True)
        
    if app.levelUp:
        drawLabel('Level Up!', 140, 185, size=20, fill='white', font=app.font, bold=True)

###########

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='gray',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='gray',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    
def drawPiece(app):
    piece = app.piece
    rows, cols = len(piece), len(piece[0])
    for row in range(rows):
        for col in range(cols):
            if app.piece[row][col] == True:
                color = app.tetrisPieceColors[app.pieceIndex]
                drawCell(app, app.pieceTopRow + row, app.pieceLeftCol + col, color)
                
def drawNextPiece(app):
    piece = app.tetrisPieces[app.nextPieceIndex]
    color = app.tetrisPieceColors[app.nextPieceIndex]
    rows, cols = len(piece), len(piece[0])
    
    boxSize = 20
    startX = 340 - (cols * boxSize) // 2
    startY = 230 - (rows * boxSize) // 2
    
    for row in range(rows):
        for col in range(cols):
            if piece[row][col]:
                cellX = startX + col * boxSize
                cellY = startY + row * boxSize
                drawRect(cellX, cellY, boxSize, boxSize, fill=color, border='gray', borderWidth=0.5)
                
                
def drawHighScores(app):
    drawLabel('High Scores:', app.width//2, 280, fill='white', size=16, font=app.font)
    for i in range(len(app.highScores)):
        if i >= 5:
            break
        score = app.highScores[i]
        spacing = 20
        x = app.width//2
        y = 300 + spacing * i
        drawLabel(f'{i+1}. {score}', x, y, fill='white', font=app.font)
    
                


##############

def movePiece(app, drow, dcol):
    if app.isPaused:
        return
    
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    
    if not pieceIsLegal(app):
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
    else:
        return True
        
def pieceIsLegal(app):
    piece = app.piece
    rows, cols = len(piece), len(piece[0])
    for row in range(rows):
        for col in range(cols):
            cell = app.piece[row][col]
            if cell:
                selectedRow = app.pieceTopRow + row
                selectedCol = app.pieceLeftCol + col
                if (selectedRow < 0) or (selectedRow > app.rows-1) or (selectedCol < 0) or (selectedCol > app.cols-1):
                    return False
                if app.board[selectedRow][selectedCol]:
                    return False
                    
    
    return True

def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass

def onKeyPress(app, key):
    # if ('0' <= key <= '6'):
    #     pieceIndex = int(key)
    #     loadPiece(app, pieceIndex)
    if key == 'left':
        movePiece(app, 0, -1)
    elif key == 'right':
        movePiece(app, 0, +1)
    elif key == 'down':
        movePiece(app, +1, 0)
    elif key == 'up':
        rotatePieceClockwise(app)
    
    # elif key == 's':
    #     takeStep(app)
        
    elif key == 'p':
        app.isPaused = not app.isPaused
        
    elif key == 'space': hardDropPiece(app)
    
    # elif key == 'j':
    #     printBoard(app)
    
    # elif key == 'l':
    #     app.clearedLines += 9
    
    
    #elif key in ['a','b','c','d','e','f','g','h']: loadTestBoard(app, key)
    
    
def rotatePieceClockwise(app):
    if app.isPaused:
        return
    
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows = len(app.piece)
    oldCols = len(app.piece[0])
    
    app.piece = rotate2dListClockwise(app.piece)
    newRows = len(app.piece)
    newCols = len(app.piece[0])
    centerRow = oldTopRow + oldRows//2
    centerCol = oldLeftCol + oldCols//2
    app.pieceTopRow = centerRow - newRows//2
    app.pieceLeftCol = centerCol - newCols//2
    
    if not pieceIsLegal(app):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol

# def printBoard(app):
#     for row in range(len(app.board)):
#         print(app.board[row])
#     print()

###########

def onStep(app):
    if not app.isPaused and not app.gameOver:
        takeStep(app)
            
    if app.tetris:
        app.tetrisSteps += 1
        if app.tetrisSteps >= 3:
            app.tetris = False
            app.tetrisSteps = 0
            
    if app.scoreAdd:
        app.scoreSteps += 1
        if app.scoreSteps >= 3:
            app.scoreAdd = False
            app.scoreSteps = 0
    
    if app.levelUp:
        app.levelUpSteps += 1
        if app.levelUpSteps >= 5:
            app.levelUp = False
            app.levelUpSteps = 0
            
    if app.gameOver:
        app.stepsPerSecond = 10
        if not app.finishScreen:
            app.gameOverSteps += 1
        
        newRow = ['white' for col in range(len(app.board[0]))]
        
        if app.gameOverSteps == 16:
            app.finishScreen = True
            app.gameOverSteps = 0
        
        for row in range(app.rows -1, app.rows - app.gameOverSteps -1, -1):
            if row < 16:
                app.board[row] = newRow
            

def takeStep(app):
    if not movePiece(app, +1, 0):
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

def placePieceOnBoard(app):
    piece = app.piece
    rows, cols = len(piece), len(piece[0])
    color = app.tetrisPieceColors[app.pieceIndex]
    
    for row in range(rows):
        for col in range(cols):
            boardRow = app.pieceTopRow + row
            boardCol = app.pieceLeftCol + col
            
            if piece[row][col]:
                app.board[boardRow][boardCol] = color
            

def removeFullRows(app):
    rows, cols = len(app.board), len(app.board[0])
    i = 0
    popped = 0
    while i < rows:
        if None not in app.board[i]:
            app.board.pop(i)
            popped += 1
            newRow = [None for i in range(cols)]
            app.board.insert(0, newRow)
            
        i += 1
        
    #single
    if popped == 1:
        app.points += 100*(app.level)
        app.scoreAdd = True
    #double
    elif popped == 2:
        app.points += 300*(app.level)
        app.scoreAdd = True
    #triple
    elif popped == 3:
        app.points += 500*(app.level)
        app.scoreAdd = True
    #tetris!
    elif popped == 4:
        app.tetris = True
        app.tetrisSteps = 0
        app.points += 800*(app.level)
        app.scoreAdd = True
        
    lastLines = app.clearedLines
    app.clearedLines += popped
    nextLines = app.clearedLines
    
    if (nextLines // 10) > (lastLines // 10):
        checkLevelUp(app)
    
def checkLevelUp(app):
    app.level += 1
    app.levelUp = True
    app.stepsPerSecond += 0.5
    #print(app.stepsPerSecond)

###########

def rotate2dListClockwise(L):
    oldRows, oldCols = len(L), len(L[0])
    newRows, newCols = oldCols, oldRows
    
    M = []
    for newRow in range(newRows):
        rowList = []
        for newCol in range(newCols):
            rowList.append(None)
        M.append(rowList)
        
    #now 2d list M is the correct size
    
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            thisCell = L[oldRow][oldCol]
            nextRow = oldCol
            nextCol = abs((oldRows-1) - oldRow)
            M[nextRow][nextCol] = thisCell
            
    return M
        
        

def onMousePress(app, mouseX, mouseY):
    if app.gameOver:
        left = app.width//2 - 110
        right = app.width//2 + 110
        top = app.height//2 + 20
        bottom = app.height//2 + 55
    
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            resetApp(app)
        
def onMouseMove(app, mouseX, mouseY):
    if not app.gameOver:
        return
    
    left = app.width//2 - 110
    right = app.width//2 + 110
    top = app.height//2 + 20
    bottom = app.height//2 + 55
    
    if (left <= mouseX <= right) and (top <= mouseY <= bottom):
        app.isSelected = True
    else:
        app.isSelected = False

# def loadTestBoard(app, key):
#     # DO NOT EDIT THIS FUNCTION
#     # We are providing you with this function to set up the board
#     # with some test cases for clearing the rows.
#     # To use this: press 'a', 'b', through 'h' to select a test board.
#     # Then press 'space' for a hard drop of the red I,
#     # and then press 's' to step, which in most cases will result
#     # in some full rows being cleared.

#     # 1. Clear the board and load the red I piece 
#     app.board = [([None] * app.cols) for row in range(app.rows)]
#     app.nextPieceIndex = 0
#     loadNextPiece(app)
#     # 2. Move and rotate the I piece so it is vertical, in the
#     #    top-left corner
#     for keyName in ['down', 'down', 'up', 'left', 'left', 'left']:
#         onKeyPress(app, keyName)
#     # 3. Add a column of alternating plum and lavender cells down
#     #    the rightmost column
#     for row in range(app.rows):
#         app.board[row][-1] = 'plum' if (row % 2 == 0) else 'lavender'
#     # 4. Now almost fill some of the bottom rows, leaving just the
#     #    leftmost column empty
#     indexesFromBottom = [ [ ], [0], [0,1], [0,1,2,3], [0,2],
#                           [1,2,3], [1,2,4], [0,2,3,5] ]
#     colors = ['moccasin', 'aqua', 'khaki', 'aquamarine',
#               'darkKhaki', 'peachPuff']
#     for indexFromBottom in indexesFromBottom[ord(key) - ord('a')]:
#         row = app.rows - 1 - indexFromBottom
#         color = colors[indexFromBottom]
#         for col in range(1, app.cols):
#             app.board[row][col] = color

def main():
    runApp()

main()
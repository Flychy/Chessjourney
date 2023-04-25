"""
-Stocare de informatii despre stadiul curent al jocului de sah
-Responsabil pentru determinarea mutarilor valide la momentul respectiv
"""

class GameState():
    def __init__(self):
        """Constructor default
        Tabla e compusa din liste.
        Liste in liste ce reprezinta practic liniile tablei"""
        # Tabla este o lista 8x8 bidimensionala(2D List), fiecare element al listei avand 2 caractere.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        #Dictionar pentru a nu avea 7 elif uri cand generam functiile getPawn,getRook, etc.
        #suntem eleganti
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,
                              'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        #pentru sah(check) tinem cont de pozitia regilor
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = [] #sa ne asiguram ca nu putem muta piesa daca suntem pinuiti
        self.checks = []
        #self.checkMate = False
        #self.staleMate = False

    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)# for fuutre history of the game
        self.whiteToMove = not self.whiteToMove # swap players
        #update king s Location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    """
    Undo the last move
    """

    def undoMove(self):
        if len(self.moveLog) != 0:  # trebuie sa existe cel putin o mutare
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
            #update king s position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    All moves considering checks
    """
    """
    Algoritm pentru getValidMoves()
    1.Determinam toate mutarile posibile
    2.Pentru fiecare mutare posibila, verifica daca e o mutare valida astfel:
        2.1. Fa mutarea
        2.2 Genereaza toate mutarile posibile ale adversarului
        2.3 Verifica daca oricare dintre mutari ataca Regele
        2.4 Daca regele e protejat, e o mutare valida si o adaugam in lista
    3.Returneaza lista mutarilor valide
    """

    """
    Algoritmul neoptimizat
    def getValidMoves(self):
        #1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        #2.) for each move, make the move
        for i in range(len(moves) -1, -1, -1): # when removing from a list go backwards trough the list
            self.makeMove(moves[i])
            #3.) generate all oponent s move
            oppMoves = self.getAllPossibleMoves()
            #4.) for each of opponent s move, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  #5.)if they do attack ur king is not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:#either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves
    
    """

    """
    Algoritm avansat - se concentreaza doar pe rege si nu genereaza toate mutarile
    """
    def getValidMoves(self):
        moves = []
        #Primul lucru facut este ca in loc sa verificam toate mutarile posibile e sa
        #verificam daca exista orice pin sau check
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck: #if the king is in the check
            if len(self.checks) == 1:#just 1 check
                moves = self.getAllPossibleMoves() #generate all the possible moves and lets see what blocks the piece
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]#enemy piece causing the check
                validSquares = []#squares that pieces can move to
                if pieceChecking[1] == 'N':#if a knight must capture it or move king, other pieces can be blocked
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:#once you get to piece and checks
                            break
                #get rid of any moves that dont block check or move king
                for i in range(len(moves) - 1, -1, -1): #go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K': #move doesnt move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #move doesn't block check or capture piece
                            moves.remove(moves[i])
            else:#double check king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #not check so all moves are fine
            moves = self.getAllPossibleMoves()

        return moves



    """
    Determine if the enemy can attack the square r,c     
    """

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opp s turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turn s back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False



    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #nr linii
            for c in range(len(self.board[r])): #nr col
                turn = self.board[r][c][0] # accesez primul caracter al elementului pentru a imi da seama ce culoare are piesa respectiva
                if(turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)#calls the apropriate move function based on piece type
        return moves

    def checkForPinsAndChecks(self):
        pins = []  # squares where all the allied pinned piece is and direction pinned from
        checks = []  # squares where enmy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == ():  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd allied piece, so no pin or check possible in this direction
                            break  # mai exact, daca am 2 piese pe traiectoria celei care ataca, nu sunt in pin, prin urmare pot muta una din ele
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 posibilitati  in aceasta condiitie
                        # (1) - pe directia ortogonala(vertical/orizontal) a Turei.
                        #      de ex: avem un pion ce apara regele de tura, acesta nu poate fi mutat
                        # (2) - pe directia diagonala a nebunului
                        # (3) - regele e in sah de la un pion
                        # (4) - orice directie, iar piesa e o regina
                        # (5) - king vs king
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and (
                                        (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():  # no piece blocking => check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:
                    break  # off board
            # check for knight checks
            knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
            for m in knightMoves:
                endRow = startRow + m[0]
                endCol = startCol + m[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking king
                        inCheck = True
                        checks.append((endRow, endCol, m[0], m[1]))
            return inCheck, pins, checks


    """
    Get all the pawn moves for the pawn located at row col and add those moves into the list
    """
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            print("sloboz")
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                print("sloboz")
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--": #2 patratele mutare
                        moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture- ne asiguramc a exista o piesa de capturat
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c),(r-1, c-1),self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] =='b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else: #black pawn moves
            if self.board[r + 1][c] == "--": #1 square move
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r,c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--": #2 square moves
                        moves.append(Move((r, c), (r + 2, c), self.board))
            #captures
            if c - 1 >= 0: #capture to left
                if self.board[r + 1][c - 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
    """
    Get all the rook moves for the pawn located at row col and add those moves into the list
    """

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': #cant remove queen from pin or rook moves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #spatiu liber
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #piesa oponent
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #propria piesa
                            break
                else: #off board
                    break


    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves: #m stands for move
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #not an ally piece(empty or enemy)
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Indiferent de pozitia sa pe harta/tabla, nebunul poate fi mutat cel mult 7 patratele
    """
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # 4 diaglonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #is still on the board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #make sure the king is landing ont he board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece(empty or enemy piece
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)




class Move():
    #definim sistemul 'metric' al sahului

    rankstToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in rankstToRows.items()} # pt fiecare key face o pereche  lafel
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
       self.startRow = startSq[0]
       self.startCol = startSq[1]
       self.endRow = endSq[0]
       self.endCol = endSq[1]
       self.pieceMoved = board[self.startRow][self.startCol]
       self.pieceCaptured = board[self.endRow][self.endCol]
       self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
      # print(self.moveID)
    """
        Overriding the equals method
    """

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]









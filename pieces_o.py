import pygame
from pygame.locals import *


class Piece():
    def __init__(self, window, board_start, tile_size, value, team, image, origin):
        self.value = value
        self.window = window
        self.board_start = board_start
        self.tile_size = tile_size
        self.team = team
        self.image = image
        self.origin = origin
        self.moves = []
        self.taken = False

    def render(self):
        if not self.taken:
            self.window.blit(self.image, self.pos)

    def send_to_origin(self, board_start, tile_size):
        self.tile = self.origin
        self.pos = [board_start[0] + tile_size * self.tile[0] + self.offset[0],
                    board_start[1] + tile_size * self.tile[1] + self.offset[1]]

    def taken(self):
        pass

    def get_team(self):
        return self.team

    def get_piece(self):
        return self.piece

    def get_tile(self):
        return self.tile

    def get_never_moved(self):
        return self.never_moved

    def set_taken(self, taken):
        self.taken = taken

    def set_tile(self, tile):
        self.tile = tile
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]


#-------------------------------------------------------------------------------------------------------------------
class King(Piece):
    def __init__(self, window, board_start, tile_size, team, scale_factor, ratio, origin):
        image = pygame.image.load("assets\{}{}.png".format(team, "King"))
        image = pygame.transform.scale(image, (int(scale_factor * ratio), int(scale_factor)))
        self.offset = [tile_size * 0.25, tile_size * 0.1]
        self.piece = "King"
        self.never_moved = True
        
        super().__init__(window, board_start, tile_size, 9999, team, image, origin)


    def get_moves(self, board_state):
        self.moves = []
        possibilities = [[1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1], [1,0]]
        for i in range(8):
            tile = [self.tile[0] + possibilities[i][0], self.tile[1] + possibilities[i][1]]
            if tile[0] <= 7 and tile[0] >= 0 and tile[1] <= 7 and tile[1] >= 0:
                if board_state[tile[0]][tile[1]] == 0:
                    self.moves.append(tile)
                elif board_state[tile[0]][tile[1]].get_team() != self.team:
                    self.moves.append(tile)

        #Castling
        if self.never_moved:
            if self.team == "white":
                #King side
                if board_state[7][7] != 0:
                    if (board_state[7][7].get_piece() == "Rook" and board_state[7][7].get_never_moved() and
                        board_state[6][7] == 0 and board_state[5][7] == 0):
                        self.moves.append([7, 7])

                #Queen side
                if board_state[0][7] != 0:
                    if (board_state[0][7].get_piece() == "Rook" and board_state[0][7].get_never_moved() and
                        board_state[1][7] == 0 and board_state[2][7] == 0 and board_state[3][7] == 0):
                        self.moves.append([0, 7])
 
            elif self.team == "black":
                #King side
                if board_state[7][0] != 0:
                    if (board_state[7][0].get_piece() == "Rook" and board_state[7][0].get_never_moved() and
                        board_state[6][0] == 0 and board_state[5][0] == 0):
                        self.moves.append([7, 0])

                #Queen side
                if board_state[0][0] != 0:
                    if (board_state[0][0].get_piece() == "Rook" and board_state[0][0].get_never_moved() and
                        board_state[1][0] == 0 and board_state[2][0] == 0 and board_state[3][0] == 0):
                        self.moves.append([0, 0])

        return self.moves
    

    def move(self, tile, clicked_state, board_state, pieces):

        #Castling
        if clicked_state != 0 and clicked_state.get_piece() == "Rook":
            #King's Side
            if tile[0] == 7:
                clicked_state.move([tile[0] - 2, tile[1]], clicked_state, board_state, pieces)
                self.tile = [tile[0] - 1, tile[1]]

            #Queen's Side
            elif tile[0] == 0:
                clicked_state.move([tile[0] + 3, tile[1]], clicked_state, board_state, pieces)
                self.tile = [tile[0] + 2, tile[1]]
                
        else:
            board_state[tile[0]][tile[1]] = self
            board_state[self.tile[0]][self.tile[1]] = 0

            #Taking an enemy piece
            if clicked_state != 0 and clicked_state.get_team() != self.team:
                clicked_state.set_taken(True)

            self.tile = tile

        self.never_moved = False
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]

        return board_state, pieces

    def get_never_moved(self):
        return self.never_moved


#-------------------------------------------------------------------------------------------------------------------
class Queen(Piece):
    def __init__(self, window, board_start, tile_size, team, scale_factor, ratio, origin):
        image = pygame.image.load("assets\{}{}.png".format(team, "Queen"))
        image = pygame.transform.scale(image, (int(scale_factor * ratio), int(scale_factor)))
        self.offset = [tile_size * 0.25, tile_size * 0.1]
        self.piece = "Queen"
        
        super().__init__(window, board_start, tile_size, 9, team, image, origin)


    def get_moves(self, board_state):
        self.moves = []
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1]]

        for direction in directions:
            tile = [self.tile[0] + direction[0], self.tile[1] + direction[1]]
            broken = False
            while tile[0] <= 7 and tile[0] >= 0 and tile[1] <= 7 and tile[1] >= 0 and not broken:
                if board_state[tile[0]][tile[1]] == 0:
                    self.moves.append(tile)
                elif board_state[tile[0]][tile[1]].get_team() != self.team:
                    self.moves.append(tile)
                    broken = True
                else:
                    broken = True
                tile = [tile[0] + direction[0], tile[1] + direction[1]]

        return self.moves
    

    def move(self, tile, clicked_state, board_state, pieces):
        board_state[tile[0]][tile[1]] = self
        board_state[self.tile[0]][self.tile[1]] = 0

        #Taking an enemy piece
        if clicked_state != 0 and clicked_state.get_team() != self.team:
            clicked_state.set_taken(True)

        self.tile = tile
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]

        return board_state, pieces

#-------------------------------------------------------------------------------------------------------------------
class Bishop(Piece):
    def __init__(self, window, board_start, tile_size, team, scale_factor, ratio, origin):
        image = pygame.image.load("assets\{}{}.png".format(team, "Bishop"))
        image = pygame.transform.scale(image, (int(scale_factor * ratio * 0.9), int(scale_factor * 0.9)))
        self.offset = [tile_size * 0.275, tile_size * 0.15]
        self.piece = "Bishop"
        
        super().__init__(window, board_start, tile_size, 3, team, image, origin)


    def get_moves(self, board_state):
        self.moves = []
        directions = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

        for direction in directions:
            tile = [self.tile[0] + direction[0], self.tile[1] + direction[1]]
            broken = False
            while tile[0] <= 7 and tile[0] >= 0 and tile[1] <= 7 and tile[1] >= 0 and not broken:
                if board_state[tile[0]][tile[1]] == 0:
                    self.moves.append(tile)
                elif board_state[tile[0]][tile[1]].get_team() != self.team:
                    self.moves.append(tile)
                    broken = True
                else:
                    broken = True
                tile = [tile[0] + direction[0], tile[1] + direction[1]]

        return self.moves
    

    def move(self, tile, clicked_state, board_state, pieces):
        board_state[tile[0]][tile[1]] = self
        board_state[self.tile[0]][self.tile[1]] = 0

        #Taking an enemy piece
        if clicked_state != 0 and clicked_state.get_team() != self.team:
            clicked_state.set_taken(True)

        self.tile = tile
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]

        return board_state, pieces


#-------------------------------------------------------------------------------------------------------------------
class Knight(Piece):
    def __init__(self, window, board_start, tile_size, team, scale_factor, ratio, origin):
        image = pygame.image.load("assets\{}{}.png".format(team, "Knight"))
        image = pygame.transform.scale(image, (int(scale_factor * ratio * 0.9), int(scale_factor * 0.9)))
        self.offset = [tile_size * 0.275, tile_size * 0.15]
        self.piece = "Knight"
        
        super().__init__(window, board_start, tile_size, 3, team, image, origin)

    def get_moves(self, board_state):
        self.moves = []
        directions = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]

        for direction in directions:
            tile = [self.tile[0] + direction[0], self.tile[1] + direction[1]]
            if tile[0] <= 7 and tile[0] >= 0 and tile[1] <= 7 and tile[1] >= 0:
                if board_state[tile[0]][tile[1]] == 0:
                    self.moves.append(tile)
                elif board_state[tile[0]][tile[1]].get_team() != self.team:
                    self.moves.append(tile)

        return self.moves
    

    def move(self, tile, clicked_state, board_state, pieces):
        board_state[tile[0]][tile[1]] = self
        board_state[self.tile[0]][self.tile[1]] = 0

        #Taking an enemy piece
        if clicked_state != 0 and clicked_state.get_team() != self.team:
            clicked_state.set_taken(True)

        self.tile = tile
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]

        return board_state, pieces


#-------------------------------------------------------------------------------------------------------------------
class Rook(Piece):
    def __init__(self, window, board_start, tile_size, team, scale_factor, ratio, origin):
        image = pygame.image.load("assets\{}{}.png".format(team, "Rook"))
        image = pygame.transform.scale(image, (int(scale_factor * ratio * 0.9), int(scale_factor * 0.9)))
        self.offset = [tile_size * 0.275, tile_size * 0.15]
        self.piece = "Rook"
        self.never_moved = True
        
        super().__init__(window, board_start, tile_size, 5, team, image, origin)

    def get_moves(self, board_state):
        self.moves = []
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        for direction in directions:
            tile = [self.tile[0] + direction[0], self.tile[1] + direction[1]]
            broken = False
            while tile[0] <= 7 and tile[0] >= 0 and tile[1] <= 7 and tile[1] >= 0 and not broken:
                if board_state[tile[0]][tile[1]] == 0:
                    self.moves.append(tile)
                elif board_state[tile[0]][tile[1]].get_team() != self.team:
                    self.moves.append(tile)
                    broken = True
                else:
                    broken = True
                tile = [tile[0] + direction[0], tile[1] + direction[1]]

        return self.moves
    

    def move(self, tile, clicked_state, board_state, pieces):
        board_state[tile[0]][tile[1]] = self
        board_state[self.tile[0]][self.tile[1]] = 0

        #Taking an enemy piece
        if clicked_state != 0 and clicked_state.get_team() != self.team:
            clicked_state.set_taken(True)

        self.never_moved = False
        self.tile = tile
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]

        return board_state, pieces

    def get_never_moved(self):
        return self.never_moved


#-------------------------------------------------------------------------------------------------------------------
class Pawn(Piece):
    def __init__(self, window, board_start, tile_size, team, scale_factor, ratio, origin):
        image = pygame.image.load("assets\{}{}.png".format(team, "Pawn"))
        image = pygame.transform.scale(image, (int(scale_factor * ratio * 0.8), int(scale_factor * 0.8)))

        self.offset = [tile_size * 0.3, tile_size * 0.2]
        self.piece = "Pawn"
        self.en_passant = False
        self.never_moved = True

        super().__init__(window, board_start, tile_size, 1, team, image, origin)

        if self.team == "white":
            self.direction = -1
        else:
            self.direction = 1
        

    def get_moves(self, board_state):
        self.moves = []

        #Moving forward
        if board_state[self.tile[0]][self.tile[1] + 1 * self.direction] == 0:
            self.moves.append([self.tile[0], self.tile[1] + 1 * self.direction])
            #Double Move
            if self.never_moved:
                if board_state[self.tile[0]][self.tile[1] + 2 * self.direction] == 0:
                    self.moves.append([self.tile[0], self.tile[1] + 2 * self.direction])

        #Diagonal take
        if self.tile[0] != 7:
            if board_state[self.tile[0] + 1][self.tile[1] + 1 * self.direction] != 0:
                if board_state[self.tile[0] + 1][self.tile[1] + 1 * self.direction].get_team() != self.team:
                    self.moves.append([self.tile[0] + 1, self.tile[1] + 1 * self.direction])

            #En-Passant
            if (board_state[self.tile[0] + 1][self.tile[1]] != 0 and board_state[self.tile[0] + 1][self.tile[1]].get_piece() == "Pawn" and
                board_state[self.tile[0] + 1][self.tile[1]].get_en_passant() and
                board_state[self.tile[0] + 1][self.tile[1]].get_team() != self.team):
                self.moves.append([self.tile[0] + 1, self.tile[1] + 1 * self.direction])

        if self.tile[0] != 0:
            if board_state[self.tile[0] - 1][self.tile[1] + 1 * self.direction] != 0:
                if board_state[self.tile[0] - 1][self.tile[1] + 1 * self.direction].get_team() != self.team:
                    self.moves.append([self.tile[0] - 1, self.tile[1] + 1 * self.direction])

            #En-Passant
            if (board_state[self.tile[0] - 1][self.tile[1]] != 0 and board_state[self.tile[0] - 1][self.tile[1]].get_piece() == "Pawn" and
                board_state[self.tile[0] - 1][self.tile[1]].get_en_passant() and
                board_state[self.tile[0] - 1][self.tile[1]].get_team() != self.team):
                self.moves.append([self.tile[0] - 1, self.tile[1] + 1 * self.direction])

        return self.moves


    def move(self, tile, clicked_state, board_state, pieces):
        board_state[tile[0]][tile[1]] = self
        board_state[self.tile[0]][self.tile[1]] = 0

        #Taking an enemy piece
        if clicked_state != 0 and clicked_state.get_team() != self.team:
            clicked_state.set_taken(True)

        #Queening
        if (self.team == "white" and tile[1] == 0) or (self.team == "black" and tile[1] == 7):
            scale_factor = self.tile_size * 0.8
            ratio = self.window.get_height()/self.window.get_width()
            
            queen = Queen(self.window, self.board_start, self.tile_size, self.team, scale_factor, ratio, tile)
            queen.set_tile(tile)
            board_state[tile[0]][tile[1]] = queen

            pieces.append(queen)
            pieces.pop(pieces.index(self))

        self.tile = tile

        #En-Passant
        if (board_state[self.tile[0]][self.tile[1] - 1 * self.direction] != 0 and
            board_state[self.tile[0]][self.tile[1] - 1 * self.direction].get_piece() == "Pawn" and
            board_state[self.tile[0]][self.tile[1] - 1 * self.direction].get_en_passant()):
            board_state[self.tile[0]][self.tile[1] - 1 * self.direction].set_taken(True)
        
        #Check en-passant
        if self.never_moved and ((self.team == "white" and self.tile[1] == 4) or (self.team == "black" and self.tile[1] == 3)):
            self.en_passant = True
        else:
            self.en_passant = False
            

        self.never_moved = False
        self.pos = [self.board_start[0] + self.tile_size * self.tile[0] + self.offset[0],
                    self.board_start[1] + self.tile_size * self.tile[1] + self.offset[1]]

        return board_state, pieces

    def get_never_moved(self):
        return self.never_moved

    def get_en_passant(self):
        return self.en_passant

            


#-------------------------------------------------------------------------------------------------------------------
def main():
    pass

if __name__ == "__main__":
    main()

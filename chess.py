import pieces_o
import pygame
from pygame.locals import *

def draw_text(surf, text, size, x, y, colour, fontName):
    font = pygame.font.Font(pygame.font.match_font(fontName), size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

def draw_ui_box(window, colours, start, height, board_start, text):

    pygame.draw.rect(window, colours["dark_brown"], (start[0] + 25, start[1], board_start[0] - 72 - 50, height))
    pygame.draw.rect(window, colours["dark_brown"], (start[0], start[1] + 25, board_start[0] - 72, height - 50))
    pygame.draw.circle(window, colours["dark_brown"], (int(start[0] + board_start[0] - 72 - 25), int(start[1] + height - 25)), 25)
    pygame.draw.circle(window, colours["dark_brown"], (int(start[0] + 25), int(start[1] - 25 + height)), 25)
    pygame.draw.circle(window, colours["dark_brown"], (int(start[0] + board_start[0] - 72 - 25), int(start[1] + 25)), 25)
    pygame.draw.circle(window, colours["dark_brown"], (int(start[0] + 25), int(start[1] + 25)), 25)

    if height > 80:
        draw_text(window, text, 25, start[0] + (board_start[0] - 72) / 2, start[1] + 24, (255,255,255), 'times new roman')
        pygame.draw.rect(window, colours["light_brown"], (start[0] + 25 + 8, start[1] + 8 + 40, board_start[0] - 72 - 50 - 16, height - 16 - 40))
        pygame.draw.rect(window, colours["light_brown"], (start[0] + 8, start[1] + 25 + 8 + 15, board_start[0] - 72 - 16, height - 50 - 16 - 15))
        pygame.draw.circle(window, colours["light_brown"], (int(start[0] + board_start[0] - 72 - 25 - 8), int(start[1] + height - 25 - 8)), 25)
        pygame.draw.circle(window, colours["light_brown"], (int(start[0] + 25 + 8), int(start[1] - 25 + height - 8)), 25)

def draw_ui(window, colours, board_start, tile_size):

    window_height = window.get_height()

    draw_ui_box(window, colours, [20, 20], window_height / 6.5, board_start, 'WHITE')
    draw_ui_box(window, colours, [20, 40 + window_height / 6.5 + window_height / 3.4],
                window_height / 2, board_start, 'MOVE HISTORY')
    draw_ui_box(window, colours, [20, 40 + window_height / 6.5], window_height / 3.6, board_start, 'PIECES TAKEN')

    draw_ui_box(window, colours, [board_start[0] + 52 + tile_size * 8, 20], window_height / 6.5, board_start, 'BLACK')
    draw_ui_box(window, colours, [board_start[0] + 52 + tile_size * 8, 40 + window_height / 6.5],
                window_height / 3.6, board_start, 'PIECES TAKEN')

def draw_board(window, colours, board_start, tile_size):
    letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    
    for i in range(8):
        draw_text(window, str(i + 1), 35, (board_start[0] - 20),
                 (board_start[1] + tile_size / 2) + (tile_size * 7) - (i * tile_size), colours["dark_brown"], 'ariel bold')
        draw_text(window, str(i + 1), 35, (board_start[0] + (tile_size * 8) + 20),
                 (board_start[1] + tile_size / 2) + (tile_size * 7) - (i * tile_size), colours["dark_brown"], 'ariel bold')
        draw_text(window, letters[i], 35, (board_start[0] + tile_size / 2) + (i * tile_size),
                 (board_start[1] + 20 + tile_size * 8), colours["dark_brown"], 'ariel bold')
        draw_text(window, letters[i], 35, (board_start[0] + tile_size / 2) + (i * tile_size),
                 (board_start[1] - 20), colours["dark_brown"], 'ariel bold')

    pygame.draw.lines(window, colours["dark_brown"], True, ((board_start[0] - 3,board_start[1] - 3), (board_start[0] + (tile_size * 8) + 3,board_start[1] - 3),(board_start[0] + (tile_size * 8) + 3,board_start[1] + (tile_size * 8) + 3), (board_start[0] - 3,board_start[1] + (tile_size * 8) + 3)), 5)
    pygame.draw.lines(window, colours["dark_brown"], True, ((board_start[0] - 32,board_start[1] - 32), (board_start[0] + (tile_size * 8) + 32,board_start[1] - 32),(board_start[0] + (tile_size * 8) + 32,board_start[1] + (tile_size * 8) + 32), (board_start[0] - 32,board_start[1] + (tile_size * 8) + 32)), 5)

    line = 0
    for i in range(1,64):
        if i % 2 == 0 and line % 2 == 0:
            pygame.draw.polygon(window, colours["dark_brown"],
                                ((board_start[0],board_start[1]), (board_start[0] + tile_size,board_start[1]),
                                 (board_start[0] + tile_size,board_start[1] + tile_size), (board_start[0],board_start[1] + tile_size)))
        elif i % 2 != 0 and line % 2 != 0:
            pygame.draw.polygon(window, colours["dark_brown"],
                                ((board_start[0],board_start[1]), (board_start[0] + tile_size,board_start[1]),
                                 (board_start[0] + tile_size,board_start[1] + tile_size), (board_start[0],board_start[1] + tile_size)))
        if i % 8 == 0:
            board_start[1] = board_start[1] + tile_size
            board_start[0] = board_start[0] - tile_size * 8
            line = line + 1
        board_start[0] = board_start[0] + tile_size


def initiate_pieces(window, resolution, board_start, tile_size):
    pieces = []

    scale_factor = tile_size * 0.8
    ratio = resolution[1]/resolution[0]

    pieces.append(pieces_o.King(window, board_start, tile_size, "white", scale_factor, ratio, [4, 7]))
    pieces.append(pieces_o.Queen(window, board_start, tile_size, "white", scale_factor, ratio, [3, 7]))
    pieces.append(pieces_o.King(window, board_start, tile_size, "black", scale_factor, ratio, [4, 0]))
    pieces.append(pieces_o.Queen(window, board_start, tile_size, "black", scale_factor, ratio, [3, 0]))

    for i in range(8):
        pieces.append(pieces_o.Pawn(window, board_start, tile_size, "white", scale_factor, ratio, [i, 6]))
        pieces.append(pieces_o.Pawn(window, board_start, tile_size, "black", scale_factor, ratio, [i, 1]))

    pieces.append(pieces_o.Knight(window, board_start, tile_size, "white", scale_factor, ratio, [1, 7]))
    pieces.append(pieces_o.Knight(window, board_start, tile_size, "white", scale_factor, ratio, [6, 7]))
    pieces.append(pieces_o.Bishop(window, board_start, tile_size, "white", scale_factor, ratio, [2, 7]))
    pieces.append(pieces_o.Bishop(window, board_start, tile_size, "white", scale_factor, ratio, [5, 7]))
    pieces.append(pieces_o.Rook(window, board_start, tile_size, "white", scale_factor, ratio, [0, 7]))
    pieces.append(pieces_o.Rook(window, board_start, tile_size, "white", scale_factor, ratio, [7, 7]))
    
    pieces.append(pieces_o.Knight(window, board_start, tile_size, "black", scale_factor, ratio, [1, 0]))
    pieces.append(pieces_o.Knight(window, board_start, tile_size, "black", scale_factor, ratio, [6, 0]))
    pieces.append(pieces_o.Bishop(window, board_start, tile_size, "black", scale_factor, ratio, [2, 0]))
    pieces.append(pieces_o.Bishop(window, board_start, tile_size, "black", scale_factor, ratio, [5, 0]))
    pieces.append(pieces_o.Rook(window, board_start, tile_size, "black", scale_factor, ratio, [0, 0]))
    pieces.append(pieces_o.Rook(window, board_start, tile_size, "black", scale_factor, ratio, [7, 0]))

    return pieces


def reset_pieces(pieces, board_start, tile_size):
    for piece in pieces:
        piece.send_to_origin(board_start, tile_size)

    board_state = []
    for i in range(8):
        board_state.append([0,0,0,0,0,0,0,0])

    for piece in pieces:
        tile = piece.get_tile()
        board_state[tile[0]][tile[1]] = piece

    return board_state


def draw_box(window, pos, colour, board_start, tile_size):
    tile = [pos[0] * tile_size + board_start[0], pos[1] * tile_size + board_start[1]]
    pygame.draw.lines(window, colour, True, (tile, [tile[0], tile[1] + tile_size],
                                                             [tile[0] + tile_size, tile[1] + tile_size],
                                                             [tile[0] + tile_size, tile[1]]), 3)
        

def play(window, resolution, clock, colours, tile_size, action):
    board_start = [resolution[0] / 4, (resolution[1] / 2) - (tile_size * 4)]

    pieces = initiate_pieces(window, resolution, board_start, tile_size)
    board_state = reset_pieces(pieces, board_start, tile_size)

    black_score = 39
    white_score = 39

    turn = "white"
    state = "selecting"

    #Pre-render
    window.fill(colours["light_brown"])
    board_start = [resolution[0] / 4, (resolution[1] / 2) - (tile_size * 4)]
    draw_board(window, colours, board_start, tile_size)
    board_start = [resolution[0] / 4, (resolution[1] / 2) - (tile_size * 4)]
    draw_ui(window, colours, board_start, tile_size)
    for piece in pieces:
        piece.render()
    pygame.display.update()
    
    while action == "play":
        mouse_tile = None

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

                #Debug
                if event.key == K_x:
                    print(board_state)

        #Inputs
        if not pygame.mouse.get_pressed()[0]:
            mouse_used = False
            
        if pygame.mouse.get_pressed()[0] and not mouse_used:
            #Render Board
            window.fill(colours["light_brown"])
            board_start = [resolution[0] / 4, (resolution[1] / 2) - (tile_size * 4)]
            draw_board(window, colours, board_start, tile_size)
            board_start = [resolution[0] / 4, (resolution[1] / 2) - (tile_size * 4)]

            #Render UI
            draw_ui(window, colours, board_start, tile_size)

            #Mouse Input
            mouse_used = True
            mouse_pos = pygame.mouse.get_pos()
            
            if (mouse_pos[0] <= board_start[0] + tile_size * 8 and mouse_pos[0] >= board_start[0] and
                mouse_pos[1] <= board_start[1] + tile_size * 8 and mouse_pos[1] >= board_start[1]):
                mouse_tile = [int((mouse_pos[0] - board_start[0]) // tile_size), int((mouse_pos[1] - board_start[1]) // tile_size)]
                clicked_state = board_state[mouse_tile[0]][mouse_tile[1]]

            #Finding and Display Moves
            if mouse_tile != None:

                
                if state == "selecting":
                    if clicked_state != 0 and clicked_state.get_team() == turn:
                        selected_tile = mouse_tile
                        selected_state = board_state[selected_tile[0]][selected_tile[1]]
                        moves = clicked_state.get_moves(board_state)
                        for move in moves:
                            draw_box(window, move, colours["white"], board_start, tile_size)
                        draw_box(window, mouse_tile, colours["green"], board_start, tile_size)
                        state = "moving"
                    else:
                        moves = None
                        state = "selecting"


                elif state == "moving":
                    #Is move possible
                    possible_move = False
                    for move in moves:
                        if move == mouse_tile:
                            possible_move = True

                    #Move piece is move is possible
                    if possible_move:
                        board_state, pieces = selected_state.move(mouse_tile, clicked_state, board_state, pieces)
                        
                        #Set to next turn
                        if turn == "white":
                            turn = "black"
                        elif turn == "black":
                            turn = "white"


                    state = "selecting"
                    

            #Rerendering Pieces
            for piece in pieces:
                piece.render()


            pygame.display.update()
        
            

#-------------------------------------------------------------------------------------------------------------------
def main():
    colours = {"white"       : [255,255,255],
               "red"         : [255,0,0],
               "blue"        : [0,0,255],
               "light_blue"  : [0, 255, 255],
               "green"       : [0, 255, 0],
               "yellow"      : [255,255,0],
               "black"       : [0,0,0],
               "grey"        : [70, 70, 70],
               "light_grey"  : [150, 150, 150],
               "pink"        : [255, 0, 255],
               "purple"      : [102, 0, 102],
               "dark_green"  : [0, 102, 0],
               "orange"      : [255,102,0],
               "dark_brown"  : [128, 64, 0],
               "light_brown" : [242, 145, 13]}
    
    clock = pygame.time.Clock()
    resolution = [1920, 1080]
    tile_size = resolution[0] / 16
    pygame.init()
    window = pygame.display.set_mode((resolution[0], resolution[1]))
    pygame.display.set_caption('Chess')

    action = "play"
    while True:
        if action == "play":
            action = play(window, resolution, clock, colours, tile_size, action)

if __name__ == "__main__":
    main()

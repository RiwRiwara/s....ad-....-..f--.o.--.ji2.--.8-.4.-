import random
import time


def algorithm_provider(possible_move, current_board, type_algorithm):
    if type_algorithm == 1:
        return play_random(possible_move)
    else:
        return play_random(possible_move)
    

def play_random(possible_move):
    while True:
        try:
            print("This is possible move: ", possible_move)
            random_piece = random.choice(list(possible_move.keys()))
            random_move = random.choice(possible_move[random_piece])

            return random_piece, random_move
        except:
            pass

        time.sleep(1)

def oneman(possible_move,current_board, oneman = ""):
    man = ""
    isFound = False
    while True:
        try:
            random_piece = random.choice(list(possible_move.keys()))
            random_move = random.choice(possible_move[random_piece])
            for i in current_board:
                if i['Field'] == random_piece:
                    if i['Piece'] == oneman:
                        isFound = True
                    man = i['Piece']
            isFound = False

            if not isFound:
                oneman = man
            
            file_path = 't.txt'
            with open(file_path, 'a') as file:
                file.write("one man : " + str(possible_move) + " | " + str(current_board) + " |\n" + str(oneman) + "\n")

            return random_piece, random_move, oneman
        except:
            pass
        time.sleep(1)

def loser(possible_move,current_board, Trichess):
    tryRound = 0
    maxRound = 10000
    while True:
        try:
            while True:
                random_piece = random.choice(list(possible_move.keys()))
                random_move = random.choice(possible_move[random_piece])
                
                for i in current_board:
                    if i['Field'] == random_piece and i['Owner'] != Trichess.Player:
                        return random_piece, random_move
                    else:
                        tryRound += 1
                        if tryRound > maxRound:
                            play_random(possible_move)
                            break
                tryRound += 1
                if tryRound > maxRound:
                    play_random(possible_move)
                    break

            return random_piece, random_move
        except:
            pass
        time.sleep(1)


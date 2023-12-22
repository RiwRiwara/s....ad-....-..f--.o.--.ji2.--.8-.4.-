import asyncio
import time
import MESSAGE
import Trichess
# import test
import algorithm
import threading


async def wait_connection(trichess):
    while True:
        try:
            game_start = await trichess.receive_response()
            if game_start['Status'] != "Success":
                return
        except:
            pass

        time.sleep(1)

async def wait_my_turn(trichess):
    while True:
        try:
            await trichess.check_turn()
            turn_response = await trichess.receive_response()

            if turn_response['Status'] == "Success":
                if turn_response['YourTurn']:
                    return turn_response
        except:
            pass

        time.sleep(1)

async def get_my_piece(trichess):
    while True:
        await trichess.myPiece()
        my_piece_response = await trichess.receive_response()

        if my_piece_response['Status'] == 'Success':
            if 'Check board for piece' in my_piece_response['Message']:
                trichess.Piece = my_piece_response['Board']
                break
            
        time.sleep(1)

    print(f"This is samle of piece {trichess.Piece[:3]}")
    return None


async def get_all_possible_move(trichess):
    field = {}
    for current_place in trichess.Piece:
        current_place = current_place['Field']
        
        await trichess.move_able(current_place)
        piece_movable = await trichess.receive_response()

        if piece_movable['Status'] == 'Fail' and 'no movable' in piece_movable['Message']:
            continue

        if piece_movable['Status'] == 'Success':
            if 'MovableFields' in piece_movable['Message']:
                for val in piece_movable['MovableFields']:
                    if current_place not in field:
                        field[current_place] = []
                    else:
                        field[current_place].append(val['Field'])
                    
    return field

def check_pass(possible_move):
    return all(len(value) == 0 for value in possible_move.values())


async def main(url, type_algorithm):
    trichess = Trichess.Trichess(url)
    await trichess.connect()

    await wait_connection(trichess)
    
    oneman = "Pawn"
    getBrave = 2
    roundLoser = 0

    while True:
        turn_response = await wait_my_turn(trichess)
        if turn_response:
            print(MESSAGE.MY_TURN)
            trichess.Board = turn_response['Board']

            await get_my_piece(trichess)
            possible_move = await get_all_possible_move(trichess)

            if check_pass(possible_move):
                await trichess.pass_turn()
                pass_response = await trichess.receive_response()
                if pass_response['Status'] == 'Success':
                    print(MESSAGE.PASS)
                continue

            if type_algorithm == 3:
                curr_position, move_to, oneman = algorithm.oneman(possible_move, trichess.Board, oneman)
            elif type_algorithm == 4:
                roundLoser += 1

                if roundLoser == getBrave:
                    curr_position, move_to = algorithm.loser(possible_move, trichess.Board, trichess)
                    roundLoser = 0
                else:
                    await trichess.pass_turn()
                    pass_response = await trichess.receive_response()
                    if pass_response['Status'] == 'Success':
                        print(MESSAGE.PASS)
                    continue

            else:
                curr_position, move_to = algorithm.algorithm_provider(possible_move, trichess.Board, type_algorithm)
            
            
            await trichess.send_move(curr_position, move_to)
            move_response = await trichess.receive_response()
            if move_response['Status'] == 'Success':
                print(MESSAGE.MOVE_SUCCESS)
        
        time.sleep(1)

if __name__ == '__main__':
    URL = 'ws://192.168.1.10:8181/game'
    n_player = int(input("Enter number of player [int]: "))
    for i in range(n_player):
        print(f"Select algorithm for player {i+1}")
        print(MESSAGE.ALGORITHM)
        algo = int(input("Enter algorithm [int]: "))
        
        threading.Thread(target=asyncio.run, args=(main(URL, algo),)).start()
        print("Thread: ", i, " started")

        time.sleep(0.5)
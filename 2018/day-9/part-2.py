from blist import blist


INPUT = '411 players; last marble is worth 7117000 points'

TEST_INPUT_0 = '9 players; last marble is worth 25 points: high score is 32'
TEST_INPUT_1 = '10 players; last marble is worth 1618 points: high score is 8317'
TEST_INPUT_2 = '13 players; last marble is worth 7999 points: high score is 146373'
TEST_INPUT_3 = '17 players; last marble is worth 1104 points: high score is 2764'
TEST_INPUT_4 = '21 players; last marble is worth 6111 points: high score is 54718'
TEST_INPUT_5 = '30 players; last marble is worth 5807 points: high score is 37305'

ALL_TESTS = [TEST_INPUT_0, TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3, TEST_INPUT_4, TEST_INPUT_5]

def parse_input(input_str):
    words = input_str.split()
    num_players = int(words[0])
    num_marbles = int(words[6])
    return num_players, num_marbles

def play_game(num_players, num_marbles):
    scores = {player: 0 for player in range(num_players)}

    current_marble_index = 0
    marble_list = blist([0])
    for marble in range(1, num_marbles + 1):
        if marble % 23 == 0:
            player_number = marble % num_players
            scores[player_number] += marble
            if current_marble_index < 7:
                scores[player_number] += marble_list.pop(current_marble_index - 6)
                current_marble_index -= 6
            else:
                scores[player_number] += marble_list.pop(current_marble_index - 7)
                current_marble_index -= 7
        else:
            new_marble_index = (current_marble_index + 2) % len(marble_list)
            if new_marble_index == 0:
                current_marble_index = len(marble_list)
            else:
                current_marble_index = new_marble_index
            marble_list.insert(current_marble_index, marble)

    return scores

def max_score(scores):
    return max(scores.values())


if __name__ == '__main__':
    num_players, num_marbles = parse_input(INPUT)
    scores = play_game(num_players, num_marbles)
    winning_score = max_score(scores)
    print(winning_score)
    # for test in ALL_TESTS:
    #     expected_score = test.split()[-1]
    #     num_players, num_marbles = parse_input(test)
    #     scores = play_game(num_players, num_marbles)
    #     winning_score = max_score(scores)
    #     print('expected_score: ' + str(expected_score))
    #     print('winning_score: ' + str(winning_score))

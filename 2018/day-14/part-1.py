class Elf(object):
    """docstring for Elf"""
    def __init__(self, current_recipe_index, current_recipe_score):
        super(Elf, self).__init__()
        self.current_recipe_index = current_recipe_index
        self.current_recipe_score = current_recipe_score

    def new_current_recipe(self, scoreboard):
        self.current_recipe_index += (1 + self.current_recipe_score)
        self.current_recipe_index %= len(scoreboard)
        self.current_recipe_score = scoreboard[self.current_recipe_index]

    def __str__(self):
        return 'Index: ' + str(self.current_recipe_index) + ', Score: ' + str(self.current_recipe_score)


def make_recipes(scoreboard, num_recipes_to_go_through):
    elves = [Elf(0, scoreboard[0]), Elf(1, scoreboard[1])]

    ten_recipes = ''
    while len(ten_recipes) < 10:
        new_recipe = sum([elf.current_recipe_score for elf in elves])
        if new_recipe // 10:
            scoreboard.append(1)
            if len(scoreboard) > num_recipes_to_go_through:
                ten_recipes += '1'
        scoreboard.append(new_recipe % 10)
        if len(scoreboard) > num_recipes_to_go_through and len(ten_recipes) < 10:
            ten_recipes += str(new_recipe % 10)
        for elf in elves:
            elf.new_current_recipe(scoreboard)

    return ten_recipes


if __name__ == '__main__':
    initial_scoreboard = [3, 7]
    INPUT = 760221
    ten_recipes = make_recipes(initial_scoreboard, INPUT)
    print(ten_recipes)

    # initial_scoreboard = [3, 7]
    # test_input_1 = 9
    # expected_output_1 = '5158916779'
    # actual_output_1 = make_recipes(initial_scoreboard, test_input_1)
    # print('Test # 1:')
    # print('expected_output:', expected_output_1)
    # print('actual_output:', actual_output_1)

    # initial_scoreboard = [3, 7]
    # test_input_2 = 5
    # expected_output_2 = '0124515891'
    # actual_output_2 = make_recipes(initial_scoreboard, test_input_2)
    # print('Test # 2:')
    # print('expected_output:', expected_output_2)
    # print('actual_output:', actual_output_2)

    # initial_scoreboard = [3, 7]
    # test_input_3 = 18
    # expected_output_3 = '9251071085'
    # actual_output_3 = make_recipes(initial_scoreboard, test_input_3)
    # print('Test # 3:')
    # print('expected_output:', expected_output_3)
    # print('actual_output:', actual_output_3)

    # initial_scoreboard = [3, 7]
    # test_input_4 = 2018
    # expected_output_4 = '5941429882'
    # actual_output_4 = make_recipes(initial_scoreboard, test_input_4)
    # print('Test # 4:')
    # print('expected_output:', expected_output_4)
    # print('actual_output:', actual_output_4)

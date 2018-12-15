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


def make_recipes(scoreboard, sequence_to_find):
    elves = [Elf(0, scoreboard[0]), Elf(1, scoreboard[1])]

    num_recipes = len(scoreboard)
    recipe_string = ''.join([str(recipe) for recipe in scoreboard])
    for i in range(len(sequence_to_find) - len(scoreboard)):
        recipe_string = '.' + recipe_string

    while sequence_to_find != recipe_string:
        new_recipe = sum([elf.current_recipe_score for elf in elves])
        if new_recipe // 10:
            scoreboard.append(1)
            recipe_string = recipe_string[1:] + '1'
            num_recipes += 1
        if sequence_to_find == recipe_string:
            break
        scoreboard.append(new_recipe % 10)
        recipe_string = recipe_string[1:] + str(new_recipe % 10)
        num_recipes += 1
        for elf in elves:
            elf.new_current_recipe(scoreboard)

    return num_recipes - len(sequence_to_find)


if __name__ == '__main__':
    initial_scoreboard = [3, 7]
    INPUT = '760221'
    num_recipes = make_recipes(initial_scoreboard, INPUT)
    print(num_recipes)

    # initial_scoreboard = [3, 7]
    # test_input_1 = '51589'
    # expected_output_1 = 9
    # actual_output_1 = make_recipes(initial_scoreboard, test_input_1)
    # print('Test # 1:')
    # print('expected_output:', expected_output_1)
    # print('actual_output:', actual_output_1)

    # initial_scoreboard = [3, 7]
    # test_input_2 = '01245'
    # expected_output_2 = 5
    # actual_output_2 = make_recipes(initial_scoreboard, test_input_2)
    # print('Test # 2:')
    # print('expected_output:', expected_output_2)
    # print('actual_output:', actual_output_2)

    # initial_scoreboard = [3, 7]
    # test_input_3 = '92510'
    # expected_output_3 = 18
    # actual_output_3 = make_recipes(initial_scoreboard, test_input_3)
    # print('Test # 3:')
    # print('expected_output:', expected_output_3)
    # print('actual_output:', actual_output_3)

    # initial_scoreboard = [3, 7]
    # test_input_4 = '59414'
    # expected_output_4 = 2018
    # actual_output_4 = make_recipes(initial_scoreboard, test_input_4)
    # print('Test # 4:')
    # print('expected_output:', expected_output_4)
    # print('actual_output:', actual_output_4)

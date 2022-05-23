from helpers import grey_to_dec


def all_are_the_same(population):
    item = population[0][0]
    for i in population:
        if i[0] != item:
            return False
    return True


def f_const_successful_condition(population_with_health):
    l = len(population_with_health[0][0])
    return all_are_the_same(population_with_health) and ((population_with_health[0][0] == (l * '0')) or (population_with_health[0][0] == (l * '1')))


def fh_fhd_successful_condition(population_with_health):
    l = len(population_with_health[0][0])
    ideal_seq = l * '0'
    return all_are_the_same(population_with_health) and (population_with_health[0][0] == ideal_seq)


def grey_x_2_successful_condition(population_with_health):
    return grey_successful_condition(population_with_health, 10.23, 10.23 ** 2, 0, 10.23)


def grey_x_successful_condition(population_with_health):
    return grey_successful_condition(population_with_health, 10.23, 10.23, 0, 10.23)


def grey_x_4_successful_condition(population_with_health):
    return grey_successful_condition(population_with_health, 10.23, 10.23 ** 4, 0, 10.23)


def grey_512_x_2_successful_condition(population_with_health):
    return grey_successful_condition(population_with_health, 0, 5.12 ** 2, -5.11, 5.12)


def grey_512_x_4_successful_condition(population_with_health):
    return grey_successful_condition(population_with_health, 0, 5.12 ** 4, -5.11, 5.12)


def grey_successful_condition(population_with_health, optimal_x, optimal_y, a, b):
    q = 0.01
    p = 0.01
    # we don't need to check all items if all of them are the same
    if all_are_the_same(population_with_health):
        x = grey_to_dec(population_with_health[0][0], a, b)
        y = population_with_health[0][1]
        return ((optimal_x - q) <= x <= (optimal_x + q)) and ((optimal_y - p) <= y <= (optimal_y + p))

    for i in population_with_health:
        x = grey_to_dec(i[0], a, b)
        y = i[1]
        if ((optimal_x - q) <= x <= (optimal_x + q)) and ((optimal_y - p) <= y <= (optimal_y + p)):
            return True
    return False

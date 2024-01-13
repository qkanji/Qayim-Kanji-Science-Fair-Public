def mark(actual: str, guess: str):
    if actual == guess:
        return 14 + 3 * len(actual.split(" "))
    actual = actual.split(" ")
    guess_orig = guess
    guess = guess.split(" ")
    points = 0
    points += mark_punc(guess_orig)
    add_points, better_guess = mark_spelling(actual, guess)
    points += add_points
    points += mark_order(actual, better_guess)
    points += mark_extra(actual, guess)
    return points


def mark_punc(guess):
    capital = one_or_two_off(guess, guess.lower())
    if guess == guess.lower():
        capital = False
    period = "." in guess
    # guess = guess.replace(".", "", 1)
    # extra = False
    # for word in guess:
    #     for bad_punc in list(".,/';:[]{}|~-"):
    #         if bad_punc in word:
    #             extra = True
    #             break
    if capital and period:
        # if extra:
        #     return 3
        return 4
    if not(capital or period):
        return 0
    # if extra:
    #     return 1
    return 2


def mark_spelling(actual, guess):
    better_actual = []
    for act_word in actual:
        for bad_punc in list(".,/';:[]{}|~-"):
            act_word = act_word.replace(bad_punc, "")
        act_word = act_word.lower()
        better_actual.append(act_word)
    better_guess = []
    for gue_word in guess:
        for bad_punc in list(".,/';:[]{}|~-"):
            gue_word = gue_word.replace(bad_punc, "")
        gue_word = gue_word.lower()
        better_guess.append(gue_word)
    actual = better_actual.copy()
    guess = better_guess.copy()
    del better_actual
    del better_guess
    orig_actual = actual.copy()
    points = 0
    better_guess = guess.copy()
    questionable_one_or_two_offs = []
    for guess_word in guess:
        if guess_word in actual:
            points += 3
            actual.remove(guess_word)
            continue
        one_or_two_res = False
        for act_word in actual:
            if one_or_two_off(act_word, guess_word):
                one_or_two_res = True
                break
        if one_or_two_res:
            # noinspection PyUnboundLocalVariable
            questionable_one_or_two_offs.append([guess_word, act_word])
            continue
        better_guess.remove(guess_word)
    for questionable_pair in questionable_one_or_two_offs:
        if (questionable_pair[1] in actual) and (questionable_pair[0] in better_guess):
            better_guess[better_guess.index(questionable_pair[0])] = questionable_pair[1]
            points += 2
        else:
            better_guess.remove(questionable_pair[0])
    final_guess = []
    for guess_word in better_guess:
        if guess_word in orig_actual:
            orig_actual.remove(guess_word)
            final_guess.append(guess_word)
    return points, final_guess


def mark_order(actual, better_guess):
    better_actual = []
    for act_word in actual:
        for bad_punc in list(".,/';:[]{}|~-"):
            act_word = act_word.replace(bad_punc, "")
        act_word = act_word.lower()
        better_actual.append(act_word)
    actual = better_actual.copy()
    del better_actual
    if actual == better_guess:
        return 5
    # 1 word is misplaced if you remove 1 word from both of them and the rest of each list are equal
    # same thing for 2 to 3 if you remove 2 to 3
    guess = better_guess.copy()
    for rm_word in guess:
        gue_copy = guess.copy()
        act_copy = actual.copy()
        gue_copy.remove(rm_word)
        act_copy.remove(rm_word)
        if gue_copy == act_copy:
            return 4
    for rm_word_1 in guess:
        gue_copy_1 = guess.copy()
        gue_copy_1.remove(rm_word_1)
        for rm_word_2 in gue_copy_1:
            gue_copy_2 = gue_copy_1.copy()
            gue_copy_2.remove(rm_word_2)
            for rm_word_3 in gue_copy_2:
                gue_copy = gue_copy_2.copy()
                act_copy = actual.copy()
                gue_copy.remove(rm_word_3)
                act_copy.remove(rm_word_1)
                act_copy.remove(rm_word_2)
                act_copy.remove(rm_word_3)
                if gue_copy == act_copy:
                    return 2
    return 0


def mark_extra(actual, guess):
    l_act = len(actual)
    l_gue = len(guess)
    if l_act == l_gue:
        return 5
    if abs(l_act - l_gue) <= 2:
        return 2
    return 0


def one_or_two_off(actual_word, guess_word):
    errors = 0
    actual_word = list(actual_word)
    guess_word = list(guess_word)
    for letter in guess_word:
        if letter in actual_word:
            actual_word.remove(letter)
        else:
            errors += 1
    errors += len(actual_word)
    if errors <= 2:
        return True
    return False

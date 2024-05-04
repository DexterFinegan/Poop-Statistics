sentence = "234 and 235"
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

for index in range(len(sentence)):
    if sentence[index] in numbers:
        if sentence[index - 1] not in numbers or index == 0:
            number = sentence[index]
            j = 1
            valid = True
            while valid:
                if index + j != len(sentence):
                    if sentence[index + j] in numbers:
                        number += sentence[index + j]
                        j += 1
                    else:
                        valid = False
                else:
                    valid = False
            print(number)

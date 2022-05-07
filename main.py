import string
import re

if __name__ == '__main__':
    text = "kdlwjwk,_2"
    correct = re.compile("[a-z0-9_]+")

    if correct.fullmatch(text):
        print('correct')
    else:print('non correct')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

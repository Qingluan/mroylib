import re


def extract(string, spic='()'):
    pre = spic[0]
    back = spic[1]
    l_count = 0
    while string.find(pre) != -1:
        l_count += 1
        s = string.find(pre) + 1
        string = string[s:]

        last_b = string.rfind(back)
        next_s = string.find(pre)
        next_b = string.find(back)
        if next_b < next_s:
            yield string[:next_b]
            string = string[next_b:] 
        else:
            yield string[:last_b]
            string = string[:last_b]

    

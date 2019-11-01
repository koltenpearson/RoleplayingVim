import re
import vim
from random import randint

def print_error():
    print("""
    Something faulty, use proper die format\n
    Some examples:
        1d6
        1d20+1
        3d6-2
    Currently, only one die type is supported
    """)


def roll_dice(roll_data):
    total = 0
    for key in ['add','sub']:
        for i in range (len(roll_data[key])):
            #All the fixed bonuses are placed in 'mod'
            raw = roll_data[key][i].strip()
            if re.match("[0-9]*d[0-9]+",raw) :
                n,d = raw.split('d')
                if n == '':
                    n = 1
                else:
                    n = int(n)
                d = int(d)

                text = []
                if key == 'add' : 
                    text.append(f'+{n if n != 1 else ""}d{d}(')
                    for i in range (n):
                        res = randint(1,d)
                        total += res
                        text.append(str(res))
                        text.append(',')
                    text.pop()
                    text.append(f') = {total}')
                    print(''.join(text))
                elif key == 'sub' :
                    text.append(f'-{n if n != 1 else ""}d{d}(')
                    for i in range (n):
                        res = randint(1,d)
                        total -= res
                        text.append(str(res))
                        text.append(',')
                    text.pop()
                    text.append(f') = {total}')
                    print(''.join(text))

            elif re.match("[0-9]+", raw) :
                if key == 'add' :
                    total += int(raw)
                    print(f'+{raw} = {total}')
                elif key == 'sub' :
                    total -= int(raw)
                    print(f'-{raw} = {total}')




    print('-'*10)
    print(f'result = {total}')
            
    return
    

def get_bonus(die_string):

    """ A function to split a string based on + and - signs
    returns a dict with 'add' and 'sub' keys"""

    out = {'add':[],'sub':[]}
    
    target = 'add'
    while '+' in die_string or '-' in die_string:
        nextp = die_string.find('+')
        nextm = die_string.find('-')

        if nextp < nextm and nextp > 0 or nextm < 0:
            to_put,die_string = die_string.split('+',1)
            out[target].append(to_put)
            target = 'add'

        else:
            to_put,die_string = die_string.split('-',1)
            out[target].append(to_put)
            target = 'sub'

    out[target].append(die_string)        
    return out

def die_from_text(die_text):
    """ A function to check if a certain text is a die, a bonus, or a predefined
    die. If the latter is the case, the function would return the die
    definition"""

    #Checking if this follows a regular die notation or a simple bonus
    if re.match("[0-9]*d[0-9]+",die_text):
        return die_text
    elif re.match("[0-9]+",die_text):
        return die_text
    #Not a die, searching for the die definition
    lnum = 0
    n0 = 0
    pre = ''
    while '.' in die_text:
        first,die_text = die_text.split('.',1)
        n0 += 1
        pre = '*'*n0 
        pattern = '^' + '\*'*n0 + '[^\*]'

        while lnum < len(vim.current.buffer):
            line = vim.current.buffer[lnum]
            if re.match(pattern,line) and first in line:
                lnum += 1
                break 
            lnum += 1

        
    for line in vim.current.buffer[lnum:]:
        if die_text in line and '=' in line:
            die_info=line.split('=')[1]
            #definition found, return it
            return die_info
        if n0>0 and re.match(pattern,line):
            break
    



def die_converter(die):

    #split bonus from main die
    die_parts = get_bonus(die)

    die_results = {'add' : [], 'sub' : []}
    
    #replace predefined dies and bonuses with die notation
    for key in ['add','sub']:
        for i in range (len(die_parts[key])):
            die_data = die_from_text(die_parts[key][i].strip())

            if die_data is None :
                continue

            if '+' in die_data or '-' in die_data :
                sub_die_data = die_converter(die_data)
                die_results['add'].extend(sub_die_data['add'])
                die_results['sub'].extend(sub_die_data['sub'])
            else :
                die_results[key].append(die_data)

    return die_results
        


#Get die data, retrun False if die infor is faulty
die_data = die_converter(vim.current.line.strip())
if not die_data:
    print_error()
else:
    roll_dice(die_data)


#if die_data == False:
#    print_error()
#else:
#    roll_die(die_data)

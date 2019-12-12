import re
import vim
from random import randint


class RollError(Exception) :
    pass


def tokenize(line) :

    offset = 0

    while offset < len(line) :

        m = re.match(r'[0-9]*d[0-9]+', line[offset:])
        if m :
            yield('die', m[0])
            offset += m.end()
            continue

        m = re.match(r'[0-9]+', line[offset:])
        if m :
            yield('digit', m[0])
            offset += m.end()
            continue

        m = re.match(r'\-', line[offset:])
        if m :
            yield('minus', m[0])
            offset += m.end()
            continue

        m = re.match(r'\+', line[offset:])
        if m :
            yield('plus', m[0])
            offset += m.end()
            continue

        m = re.match(r'\\[a-zA-Z_]+', line[offset:])
        if m :
            yield('var', m[0])
            offset += m.end()
            continue 

        m = re.match(r'\%[a-zA-Z_]+', line[offset:])
        if m :
            yield ('mod', m[0])
            offset += m.end()
            continue

        m = re.match(r'\([a-zA-Z_ ]+\)', line[offset:])
        if m :
            yield('label', m[0])
            offset += m.end()
            continue

        offset += 1


def roll(die_string) :
    count, max = die_string.split('d')
    if count == '' :
        count = 1
    else :
        count = int(count)

    max = int(max)

    rolls = []
    for i in range(count) :
        rolls.append(randint(1,max))

    return rolls


def lookup(var_string) :
    var_string = var_string[1:]
    for line in vim.current.buffer :
        if re.match(r'\s*'+var_string+r'\s*=', line) :
            return line

    raise RollError(f'could not find variable {var_string}')


def process(line, echo=False) :

    if echo :
        disp = lambda x : print(f'{x}', end='')
    else :
        disp = lambda x : x

    total = 0
    op = lambda x,y : x + y
    for t,v in tokenize(line) :
        if t == 'die' :
            rolls = roll(v)
            roll_string = ','.join([str(r) for r in rolls])
            disp(f'{v}({roll_string})')
            total = op(total, sum(rolls))
        elif t == 'digit' :
            disp(v)
            total = op(total, int(v))
        elif t == 'label' :
            disp(' '+v)
        elif t == 'var' :
            val = process(lookup(v))
            disp(f'{val} ({v[1:]})')
            total = op(total, process(lookup(v)))
        elif t == 'mod' :
            val = process(lookup(v))
            val = (val-10)//2
            disp(f'{val} ({v})')
            total = op(total, val)
        elif t == 'plus' :
            disp('\n+ ')
            op = lambda x,y : x+y
        elif t == 'minus' :
            disp('\n- ')
            op = lambda x,y : x-y
        else :
            raise RollError(f"unknown token {t} : {v}")


    return total

if rpg_action == 'roll' :
    t = process(vim.current.line, echo=True)
    print('\n----------\n')
    print(f'total : {t}')


if rpg_action == 'lookup' : 
    l,c = vim.current.window.cursor
    l -= 1

    line = vim.current.buffer[l]
    parts = re.split(r'(\s|\+|\-|\(|\))', line)
    current = 0
    for p in parts :
        c -= len(p)
        if c < 0 :
            try :
                line = lookup(p)
                process(line, echo=True)
            except RollError :
                print('no such variable')
            break




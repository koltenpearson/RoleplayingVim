import re
import vim


class SumError(Exception) :
    pass

def tokenize(line) :

    offset = 0

    while offset < len(line) :

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

        m = re.match(r'gp', line[offset:])
        if m :
            yield('gp', m[0])
            offset += m.end()
            continue 

        m = re.match(r'sp', line[offset:])
        if m :
            yield ('sp', m[0])
            offset += m.end()
            continue

        m = re.match(r'cp', line[offset:])
        if m :
            yield ('cp', m[0])
            offset += m.end()
            continue

        m = re.match(r'pp', line[offset:])
        if m :
            yield ('pp', m[0])
            offset += m.end()
            continue


        offset += 1

rate = {
    'pp' : 10 * 10 * 10,
    'gp' : 10 * 10,
    'sp' : 10,
    'cp' : 1
}
def process(text, echo=False) :

    if echo :
        disp = lambda x : print(f'{x}', end='')
    else :
        disp = lambda x : x

    total = 0
    current = 0
    op = lambda x,y : x + y
    for t,v in tokenize(text) :
        if t == 'digit' :
            disp(v)
            current = int(v)
        elif t in rate :
            disp(' '+t)
            value = current * rate[t]
            total = op(total, value)
            current = 0
        elif t == 'plus' :
            disp('\n+ ')
            op = lambda x,y : x+y
        elif t == 'minus' :
            disp('\n- ')
            op = lambda x,y : x-y
        else :
            raise SumError(f"unknown token {t} : {v}")


    return total


def make_change(total) :
    pp = total // rate['pp']
    gp = (total % rate['pp']) // rate['gp']
    sp = (total % rate['pp'] % rate['pp']) // rate['sp']
    cp = (total % rate['pp'] % rate['pp'] % rate['sp']) // rate['cp']

    return (pp, gp, sp, cp)

l,c = vim.current.window.cursor
l -= 1
start_index = l
end_index = l

while True :
    start_index -= 1 
    if start_index < 0 :
        start_index = 0
        break
    if len(vim.current.buffer[start_index].strip()) == 0 :
        start_index += 1
        break

while True :
    end_index += 1 
    if end_index > len(vim.current.buffer)-1 :
        end_index = len(vim.current.buffer)-1
        break

    if len(vim.current.buffer[end_index].strip()) == 0 :
        break

total = process('\n'.join(vim.current.buffer[start_index:end_index]))
pp,gp,sp,cp = make_change(total)
print('total : ', end='')
if pp != 0 :
    print(f'{pp} pp ', end='')
if gp != 0 :
    print(f'{gp} gp ', end='')
if sp != 0 :
    print(f'{sp} sp ', end='')
if cp != 0 :
    print(f'{cp} cp ', end='')

print('')





let s:plugin_path = resolve(expand('<sfile>:p:h'))

function! RPGC#running#roll()

    "Running the python script
    execute ':python3 rpg_action = "roll"'
    execute 'py3file ' . s:plugin_path . '/die_roller.py'

endfunction



function! RPGC#running#lookup()

    "Running the python script
    execute ':python3 rpg_action = "lookup"'
    execute 'py3file ' . s:plugin_path . '/die_roller.py'

endfunction

function! RPGC#running#check()

    "Running the python script
    execute ':python3 rpg_action = "check"'
    execute 'py3file ' . s:plugin_path . '/die_roller.py'

endfunction


function! RPGC#running#colsum()

    "Running the python script
    execute 'py3file ' . s:plugin_path . '/money_sum.py'

endfunction


import PySimpleGUI as sg
import pokepy
pk = pokepy.V2Client()

def calc(move_name_P='', move_name_O='', accuracy_stages_P='0', accuracy_stages_O='0', evasion_stages_P='0', evasion_stages_O='0', para_P=False, para_O=False, flinch_P=False, flinch_O=False, confusion_P=False, confusion_O=False, infatuation_P=False, infatuation_O=False, ability_P='', ability_O='', item_P='', item_O=''):

    result = []

    accuracy_modifiers = {'-6': 0.33, '-5': 0.38, '-4': 0.43, '-3': 0.5, '-2': 0.6, '-1': 0.75, '0': 1, '1': 1.33, '2': 1.67, '3': 2, '4': 2.33, '5': 2.67, '6': 3, '+1': 1.33, '+2': 1.67, '+3': 2, '+4': 2.33, '+5': 2.67, '+6': 3, '': 1}

    if move_name_P != '':
        move_name_P = move_name_P.replace(" ", "-")
        move_P = pk.get_move(move_name_P)
        ab_mod_P = 1
        item_mod_P = 1
        if ability_P == 'hustle':
            ab_mod_P *= 0.8
        elif ability_P == 'snow cloak':
            ab_mod_P = 0.8
        elif ability_P == 'sand veil':
            ab_mod_P = 0.8
        if item_P == 'wide lens':
            item_mod_P *= 1.1
        final_acc_P = move_P.accuracy*accuracy_modifiers[str(accuracy_stages_P)]*accuracy_modifiers[str('-'+evasion_stages_O)]*ab_mod_P*item_mod_P
        if para_P == True:
            final_acc_P *= 0.75
        if flinch_P == True:
            check_flinch = str(move_O.effect_entries).lower().find('flinch')
            if check_flinch > -1:
                if ability_O == 'serene grace':
                    mod = 2
                if item_O == 'kings rock':
                    mod = 2
                else:
                    mod = 1
                    final_acc_P = (1-move_O.accuracy/100*mod*move_O.effect_chance/100)*final_acc_P
            else:
                final_acc_P = final_acc_P
        if confusion_P == True:
            final_acc_P *= 0.5
        if infatuation_P == True:
            final_acc_P *= 0.5
        result.append(final_acc_P)

    if move_name_O != '':
        move_name_O = move_name_O.replace(" ", "-")
        move_O = pk.get_move(move_name_O)
        ab_mod_O = 1
        item_mod_O = 1
        if ability_O == 'hustle':
            ab_mod_O *= 0.8
        elif ability_O == 'snow cloak':
            ab_mod_O = 0.8
        elif ability_O == 'sand veil':
            ab_mod_O = 0.8
        if item_O == 'wide lens':
            item_mod_O *= 1.1
        final_acc_O = move_O.accuracy*accuracy_modifiers[str(accuracy_stages_O)]*accuracy_modifiers['-'+str(accuracy_stages_P)]*ab_mod_O*item_mod_O
        if para_O == True:
            final_acc_O *= 0.75
        if flinch_O == True:
            check_flinch = str(move_P.effect_entries).lower().find('flinch')
            if check_flinch > -1:
                if ability_P == 'serene grace':
                    mod = 2
                if item_P == 'kings rock':
                    mod = 2
                else:
                    mod = 1
                final_acc_o = (1-move_P.accuracy/100*(mod*move_P.effect_chance/100))*final_acc_O
            else:
                final_acc_O = final_acc_O
        if confusion_O == True:
            final_acc_O *= 0.5
        if infatuation_O == True:
            final_acc_O *= 0.5
        result.append(final_acc_O)

    return(result)




sg.theme('DarkAmber')

layout = [ [sg.Text('Player Move'), sg.InputText('', size=(20,1), key='mnP'), sg.Text('Opponent Move'), sg.InputText('', size=(20,1), key='mnO')],
[sg.Text('Player Accuracy Changes'), sg.InputText('', size=(4,1), key='accP'), sg.Text('Opponent Accuracy Changes'), sg.InputText('', size=(4,1), key='accO')],
[sg.Text('Player Evasion Changes'), sg.InputText('', size=(4,1), key='evP'), sg.Text('Opponent Evasion Changes'), sg.InputText('', size=(4,1), key='evO')],
[sg.Text('Player Item'), sg.InputText('', size=(20,1), key='itP'), sg.Text('Opponent Item'), sg.InputText('', size=(20,1), key='itO')],
[sg.Text('Player Ability'), sg.InputText('', size=(20,1), key='abP'), sg.Text('Opponent Ability'), sg.InputText('', size=(20,1), key='abO')],
[sg.Checkbox('Player Paralysis', default=False, key='paraP'), sg.Checkbox('Opponent Paralysis', key='paraO')],
[sg.Checkbox('Player Flinch', key='flP'), sg.Checkbox('Opponent Flinch', key='flO')],
[sg.Checkbox('Player Confuision', key='confP'), sg.Checkbox('Opponent Confusion', key='confO')],
[sg.Checkbox('Player Infatuation', key='infP'), sg.Checkbox('Opponent Infatuation', key='infO')],
[sg.Submit(), sg.Button('Reset'), sg.Quit()]
]

window = sg.Window(title='Pokemon Accuracy/Probability Calculator', layout=layout, margins=(100,100))

while True:
    event, values = window.read()
    if event == 'Submit':
        result = calc(move_name_P=values['mnP'], move_name_O=values['mnO'], accuracy_stages_P=values['accP'], accuracy_stages_O=values['accO'], evasion_stages_P=values['evP'], evasion_stages_O=values['evO'], para_P=values['paraP'], para_O=values['paraO'], flinch_P=values['flP'], flinch_O=values['flO'], confusion_P=values['confP'], confusion_O=values['confO'], infatuation_P=values['infP'], infatuation_O=values['infO'], ability_P=values['abP'], ability_O=values['abO'], item_P=values['itP'], item_O=values['itO'])
        if len(result) == 2:
            sg.Popup('Player probability = ', str(round(result[0],2)) + '% \n Opponent probability = ', str(round(result[1],2)) + '%')
        else:
            sg.Popup('Probability = ', str(round(result[0],2)) + '%')
    if event == 'Reset':
        for key in values:
            window[key]('')
    if event == 'Quit':
        exit()
    if event == sg.WIN_CLOSED:
        break

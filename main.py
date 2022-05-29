# coding: utf-8

# pyinstaller main.py --onefile --name Dairy_task_manager --noconsole --clean


'''
デイリータスク管理and操作ターミナルアプリケーション(完全個人仕様)
・ターミナルを模したUIからタスクの追加、変更、削除をコマンド形式で可能に(最大４つ) ・・・clear
・HELPコマンドの実装 ・・・clear
・ボタンを押下することでボタン色変化の要領でタスク完了を可視化 ・・・clear
・毎日朝6:00にタスク完了状態を更新
・コマンドから更新時間の変更、更新の有無等も変更可能に
・起動時、前回のタスク設定保持（別ファイル管理IO） ・・・clear

'''

import PySimpleGUI as sg

 
#======================== Define functions ==========================

def command(text, window):

    global change_task_flag, change_task_tnum_flag, helps

    print(' COMMAND_INPUTED >>>  ' + text)
    window['input'].update('')

    if text == 'exit':
        window.close()

    elif text == 'change':
        print(''' タスクを変更します
 変更したいタスク番号を入力してください
 >>> ''', end='')
        change_task_flag = True
        change_task_tnum_flag = True
    
    elif text == 'reset':
        for i in range(5):
            num = str(i+1)
            window['task' + num].update(button_color='#0099ff') 
        print(' タスクの進捗をリセットしました\n')

    elif text == 'help':
        print(helps)

    elif text == '':
        pass
    else:
        print(' Invalid Command. /help to check commands.\n')





def change_task(text, window):

    global change_task_flag, change_task_tnum_flag, task_num, task_list_path, task_list

    window['input'].update('')

    if change_task_tnum_flag == True:

        if text == '1' or text == '2' or text == '3' or  text == '4' or text == '5':
            task_num = text
            print('\n 新しいタスクの内容を入力してください\n>>> ',end='')
            change_task_tnum_flag = False
        else:
            print('\n ERROR：1~5の数字を入力してください\n>>> ')

    else:
        task_list[int(task_num)-1] = text
        with open(task_list_path, mode='w', encoding='utf-8') as f:
            f.write('\n'.join(task_list))
        window['task' + task_num].update(text)
        print(' タスクの内容を「' + text + '」に変更しました\n')
        change_task_flag = False





#==================== Define global Variables ======================
change_task_flag = False
change_task_tnum_flag = False
task_num = '1'

task_list_path = 'data/tasks.txt'

with open(task_list_path, encoding='utf-8') as f:
    task_list = [s.strip() for s in f.readlines()]


helps = '''
 ===================================================================
  **** helps for commands ****

   help - check command list and how to

   change - change the task 

   reset - reset task progress

   exit - close this app

 ===================================================================


'''


#======================== Define Lauout =============================
term = [
            [sg.Output(pad=((0,0),(0,0)),
                        text_color='#ffffff',
                        background_color='#2b0020',
                        echo_stdout_stderr=True,
                        font=('Arial',11),
                        key='output')],
            [sg.Text('Input >>> ', font=('Arial',12)),
             sg.Input(key='input',
                        size=(80,None),
                        expand_x=True,
                        pad=((0,5),(0,0)),
                        focus=True)]
       ]


tasks = sg.Frame('',
                    [
                    [sg.Button(task_list[0], 
                                expand_y=True,
                                expand_x=True,
                                key='task1',
                                font=('Arial',18),
                                button_color='#0099ff')],
                    [sg.Button(task_list[1],
                                expand_y=True,
                                expand_x=True,
                                key='task2',
                                font=('Arial',18),
                                button_color='#0099ff')],
                    [sg.Button(task_list[2],
                                expand_y=True,
                                expand_x=True,
                                key='task3',
                                font=('Arial',18),
                                button_color='#0099ff')],
                    [sg.Button(task_list[3],
                                expand_y=True,
                                expand_x=True,
                                key='task4',
                                font=('Arial',18),
                                button_color='#0099ff')],
                    [sg.Button(task_list[4],
                                expand_y=True,
                                expand_x=True,
                                key='task5',
                                font=('Arial',18),
                                button_color='#0099ff')]
                    ],
                    size=(480, 1080), key='tasks', pad=((0,0),(0,0))
                ) 


layout = [
             [sg.Column(term, expand_x=True, expand_y=True),
              tasks]
         ]


#======================= Define Window =============================
sg.theme('DarkBlue')

window = sg.Window('DAIRY TASK MANAGER',
                    layout,
                    no_titlebar=True,
                    location=(0,0),
                    margins=(0,0),
                    resizable=True
                  ).Finalize()
window.maximize()

window['output'].expand(expand_x=True, expand_y=True)
window['input'].bind("<Return>", "_Enter")


print(''' #############################################################

       Dairy Tasks Manager by N4RU53.
       Version 0.0.1 all right reserved.

 #############################################################\n
 Type \'help\' to refer command list.\n\n''')


#======================== Main Loop ============================
while True:
    event, values = window.read(timeout=None)

    if event == sg.WIN_CLOSED:
        break

    elif event == 'input' + '_Enter':
        if change_task_flag == True:
            change_task(values['input'], window)

        else:
            command(values['input'], window)

    elif event == 'task1' or event == 'task2' or event == 'task3' or event == 'task4' or event == 'task5':
        window[event].update(button_color='#808080')
        

window.close()
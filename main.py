# coding: utf-8

'''
デイリータスク管理アプリケーション
・画面に常に表示させておく状態を想定
・ターミナルを模したUIからタスクの追加、変更、削除をコマンド形式で可能に(最大４つ)
・HELPコマンドの実装
・ボタンを押下することでボタン色変化の要領でタスク完了を可視化
・毎日朝6:00にタスク完了状態を更新
・コマンドから更新時間の変更、更新の有無等も変更可能に
・起動時、前回のタスク設定保持（別ファイル管理IO）

'''


from audioop import add
from turtle import window_width
import PySimpleGUI as sg
from sqlalchemy import false

 
#======================== Define functions ==========================

def command(text, window):

    global change_flag
    global change_tnum_flag
    global helps

    print('COMMAND_INPUTED >>>  ' + text)
    window['input'].update('')

    if text == '/exit':
        ans = sg.popup_ok_cancel('アプリを閉じますか？', title = '')
        if ans == 'OK':
            window.close()
        else:
            print('Exit Canceled.')

    elif text == '/change':
        print('''タスクを変更します
変更したいタスク番号を入力してください
>>> ''', end='')
        change_flag = True
        change_tnum_flag = True
    
    elif text == '/reset':
        for i in range(5):
            num = str(i+1)
            window['task' + num].update(button_color='#00bfff') 
        print('タスクの進捗をリセットしました')

    elif text == '/help':
        print(helps)


    else:
        print('Invalid Command. /help to check commands.')





def change_task(text, window):

    global change_flag 
    global change_tnum_flag
    global task_num

    window['input'].update('')

    if change_tnum_flag == True:

        if text == '1' or text == '2' or text == '3' or  text == '4' or text == '5':
            task_num = text
            print('\n新しいタスクの内容を入力してください\n>>> ',end='')
            change_tnum_flag = False
        else:
            print('\nERROR：1~5の数字を入力してください')

    else:
        window['task' + task_num].update(text)
        print('タスクの内容を「' + text + '」に変更しました')
        change_flag = False




#==================== Define global Variables ======================
change_flag = False
change_tnum_flag = False
task_num = '1'




helps = '''
===================================================================
 **** helps for commands ****

   /help - check command list and how to

   /change - change the task 

   /reset - reset task progress

   /exit - close this app

===================================================================
'''


#======================== Define Lauout =============================
term = [
            [sg.Output(pad=((0,0),(0,0)),
                        text_color='white',
                        background_color='black',
                        echo_stdout_stderr=True,
                        key='output')],
            [sg.Text('Input >>> '),
             sg.InputText(key='input',
                        size=(80,None),
                        expand_x=True,
                        pad=((0,0),(0,0)))]
       ]

tasks = sg.Frame('',
                    [
                    [sg.Button('1.設定されていません', 
                                expand_y=True,
                                expand_x=True,
                                key='task1',
                                button_color='#00bfff')],
                    [sg.Button('2.設定されていません',
                                expand_y=True,
                                expand_x=True,
                                key='task2',
                                button_color='#00bfff')],
                    [sg.Button('3.設定されていません',
                                expand_y=True,
                                expand_x=True,
                                key='task3',
                                button_color='#00bfff')],
                    [sg.Button('4.設定されていません',
                                expand_y=True,
                                expand_x=True,
                                key='task4',
                                button_color='#00bfff')],
                    [sg.Button('5.設定されていません',
                                expand_y=True,
                                expand_x=True,
                                key='task5',
                                button_color='#00bfff')]
                    ],
                    size=(480, 1080), key='tasks'
                ) 


layout = [
             [sg.Column(term, expand_x=True, expand_y=True),
              tasks]
         ]


#======================= Define Window =============================
sg.theme('DarkBlue')

window = sg.Window('DAIRY TASK MANAGER',
                    layout,
                    no_titlebar=False,
                    location=(0,0),
                    margins=(0,0),
                    resizable=True
                  ).Finalize()
window.maximize()

window['output'].expand(expand_x=True, expand_y=True)
window['input'].bind("<Return>", "_Enter")


print('''#############################################################

       Dairy Tasks Manager by N4RU53.
       Version 0.0.1 all right reserved.

#############################################################\n''')



#======================== Main Loop ============================
while True:
    event, values = window.read(timeout=None)

    if event == sg.WIN_CLOSED:
        break

    elif event == 'input' + '_Enter':
        if change_flag == True:
            change_task(values['input'], window)

        else:
            command(values['input'], window)

    elif event == 'task1' or event == 'task2' or event == 'task3' or event == 'task4' or event == 'task5':
        window[event].update(button_color='#808080')
        

window.close()
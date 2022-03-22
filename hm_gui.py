#        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#        |           The Hangman             |
#        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|


''' Objective : Create the hangman (word-guess) game program in Python. Use words and
                guesses from a stored file. Use user authentication before starting the
                app. Store name and score of player in a file. Update scores if it is 
                better for the same player.
'''

# imported modules

import json
import os
import random
from tkinter import *
from tkinter import messagebox, ttk
import mail  # User defined module(To initiate sending of mail.)


# Button Tracker i.e for pressed button

btn_tracker_list = [None]


def btn_track(btn_name):
    global btn_tracker_list
    btn_tracker_list.append(btn_name)

# function defined to show the score board


def leaderboard():

    with open('authentication_file.json', encoding="utf8") as f:
        ld = json.load(f)
        f.close()

    root_lb = Tk()
    root_lb.title('~ Leader Board ~')
    logo1 = PhotoImage(file='pic2'+os.sep + 'GAME LOGO.png', master=root_lb)
    root_lb.iconphoto(False, logo1)

    f1 = Frame(root_lb)
    f1.pack()
    sort_orders = sorted(ld.items(), key=lambda x: x[1][0], reverse=True)
    if len(ld) < 15:
        ht = len(ld)+1
    else:
        ht = 16

    t1 = Text(font='consolas 15', bg='ghostwhite',
              master=f1, wrap=NONE, width=64, height=ht)
    t1.pack(fill=BOTH, expand=True)
    t1.insert(INSERT, f"{'Rank':^20}|{'Player Name':^20}|{'Score':^20}|\n")
    t1.tag_add('header', '1.0', '1.64')
    t1.tag_config('header', foreground='#ffffff', background='black')
    for i, j in enumerate(sort_orders):
        t1.insert(INSERT, f"{i+1:^20}|{j[0]:<20}|{j[1][0]:^20}|\n")
    t1.config(state=DISABLED)

    root_lb.mainloop()

# function defined to remove a user account


def del_usr():
    global root
    try:
        if str(r_p_m.state()) == 'normal':
            r_p_m.destroy()
    except Exception:
        pass
    try:
        if str(reset_screen.state()) == 'normal':
            reset_screen.destroy()
    except Exception:
        pass
    try:
        login_screen.withdraw()
    except Exception:
        game_win.withdraw()
    try:
        root = Toplevel(game_win, bg='ghostwhite')
    except Exception:
        root = Toplevel(login_screen, bg='ghostwhite')

    root.title('Remove Player')
    root.geometry('280x100')
    logo1 = PhotoImage(file='pic2'+os.sep + 'GAME LOGO.png',
                       master=root)
    root.iconphoto(False, logo1)
    Label(root, text="Player name:",
          font='Century 15', bg='ghostwhite').grid(row=1, column=0)
    del_name = ttk.Entry(root)
    del_name.grid(row=1, column=1)
    Label(root, text="Password:",
          font='Century 15', bg='ghostwhite').grid(row=2, column=0)
    del_pass = ttk.Entry(root)
    del_pass.grid(row=2, column=1)

    def cancel():
        try:
            game_win.deiconify()
        except Exception:
            login_screen.deiconify()
        root.withdraw()

    def proceed():
        with open('authentication_file.json', encoding="utf8") as f:
            ld = json.load(f)
            f.close()
        try:
            if ld[str(del_name.get())][1] == str(del_pass.get()):

                # print(str(del_pass.get()))
                # print(ld[str(del_name.get())][1])

                ans = messagebox.askokcancel(
                    title='Confirmation', message='Are you sure?')
                if ans:
                    with open('authentication_file.json', 'w', encoding="utf8") as f:
                        temp_mail = ld[str(del_name.get())][2]
                        del ld[str(del_name.get())]
                        json.dump(ld, f, indent=4)
                        f.close()
                    try:

                        # print(temp_mail)
                        mail.del_mail(RECIEVERMAIL=temp_mail,
                                      PLAYERNAME=str(del_name.get()))
                    except Exception:
                        pass

                    ans = messagebox.askokcancel(
                        title='Successfully Deleted.', message='Player removed successfully.\nWhat to play?')

                    if ans:
                        main_screen.deiconify()
                        try:
                            game_win.withdraw()
                        except Exception:
                            pass
                        root.withdraw()
                    else:
                        try:
                            main_screen.destroy()
                            game_win.destroy()

                            exit
                        except Exception:
                            exit

                        exit
                else:
                    cancel()
            else:
                messagebox.showerror(
                    title='Incorrect Details', message='Incorrect Username or Password')
        except Exception:
            messagebox.showerror(title='Incorrect Details',
                                 message='Incorrect Username or Password')

    conform_btn = ttk.Button(root, text='Proceed', command=proceed)
    conform_btn.grid(row=3, column=1)

    cancel_btn = ttk.Button(root, text="Cancel", command=cancel)
    cancel_btn.grid(row=3, column=0)
    root.mainloop()

# Manuals for the game


def how_to_play():

    with open('manual.txt', 'r') as ftobe:
        r = ftobe.readlines()
    qw = ''
    for i in r:
        qw += i
    messagebox.showinfo(title='How to Play', message=qw)

# Credits


def credits():
    messagebox.showinfo(
        title='Credits', message='Game Coded and Developed by :\n>Uchit.N.M\n>')

# Source code popup window


def source_code():

    with open('source_code.txt', 'r') as ftobe:
        r = ftobe.read()

    messagebox.showinfo(title='Source Code | About ', message=r)

# Game Description


def about_code():

    with open('aboutgame.txt', 'r') as ftobe:
        r = ftobe.readlines()
    qw = ''
    for i in r:
        qw += i
    messagebox.showinfo(title='Source Code | About ', message=qw)

# function defined for updation of the score


def score_update(curr):
    with open('authentication_file.json', 'r', encoding="utf8") as f:  # reading the data bases
        data = json.load(f)
        f.close()
    # Updating the user Score & Dumping the contents
    with open('authentication_file.json', 'w', encoding="utf8") as f:
        data[user_name][0] = curr
        json.dump(data, f, indent=4)
        f.close()


# Defalt theme Value
theme_val = 'L'

# Function to Manage 'Remaining chances label'


def remaining_chances(label_temp):
    global game_win
    if theme_val == 'D':
        label_temp.config(text='Remaining chances : '+'0'+str(10 -
                                                              error), font=('Century', 18), bg='#000b18', fg='#e71e65')
    elif theme_val == 'L':
        label_temp.config(text='Remaining chances : '+'0'+str(10 -
                                                              error), font=('Century', 18), bg='#fcf6e2', fg='green')

# Main Game function


def main_game():

    global word_label, game_win, remaining_chances_label, details_label, Frame1

    game_win = Tk()
    game_win.title('| Hangman GUI |  Hello ' + user_name +
                   ' ! | '+(str(type_game.get())))
    game_win.config(bg='#fcf6e2')
    word_label = Label(game_win, text='', font=('Century 24'), bg='#fcf6e2')

    logo = PhotoImage(file='pic2'+os.sep +
                      'GAME LOGO.png', master=game_win)
    Frame1 = Frame(game_win, bg='#fcf6e2')
    Frame1.place(x=10, y=10)
    remaining_chances_label = Label(Frame1, text='Remaining chances : '+str(10),
                                    font=('Century', 18), bg='#fcf6e2', fg='green')
    details_label = Label(Frame1, font=('Century', 18), bg='#fcf6e2', fg='red')

    game_win.iconphoto(False, logo)

    # Getting conformation for closing
    def close_login():
        conform = messagebox.askyesno(
            title='Are you Sure !', message='Want to force quit the Game ?', detail='Your game might Not be saved !')
        if conform:
            exit()

    game_win.protocol('WM_DELETE_WINDOW', close_login)
    # Loading words from Data bases
    with open('Data_file.json', encoding="utf8") as f:
        ldd = json.load(f)

    f.close()

    tg = (str(type_game.get()))
    main_data = (ldd[tg])

    # Light theme Photos
    photos = [
        PhotoImage(file='Pic2'+os.sep+'h1_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h2_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h3_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h4_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h5_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h6_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h7_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h8_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h9_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h10_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h11_light.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'win_light.png', master=game_win)
    ]

    # Dark theme Photos

    Dark_photos = [
        PhotoImage(file='Pic2'+os.sep+'h1_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h2_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h3_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h4_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h5_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h6_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h7_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h8_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h9_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h10_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'h11_dark.png', master=game_win),
        PhotoImage(file='Pic2'+os.sep+'win_dark.png', master=game_win)
    ]

    # Function to recall new game i.e Launch game with fresh word

    def main():
        global value_1, remaining_chances_label, btn_tracker_list

        # Resetting of the tracter list and letter tracker for keyboard inputs
        btn_tracker_list = [None]
        letter_track_list = []
        word_label.grid(row=0, column=3, columnspan=10, padx=10)

        # Menu Bar

        value_1 = IntVar(game_win)

        bar = Menu(game_win, background='blue')
        # option menu
        options_menu = Menu(bar, tearoff=0, activebackground='coral')
        options_menu.add_command(
            label='New Game', command=lambda: main())
        options_menu.add_command(label='Change Player', command=lambda: (
            main_screen.deiconify(), game_win.destroy()))

        options_menu.add_command(
            label='Play With!', command=lambda: (game_win.destroy(), login()))
        options_menu.add_separator()

        theme = Menu(options_menu, tearoff=0)

        # Setting radiobutton value .
        if theme_val == 'D':  # if dark set 2
            value_1.set(2)
        else:  # if light set 1
            value_1.set(1)


        # Feedback Window and Function

        def Feedback_win():

            root_fb = Tk()
            root_fb.title('Feedback')
            name_slot = Entry(master=root_fb)
            name_slot.pack(fill=BOTH,expand=True)
            name_slot.insert(END,'Your Name')
            name_slot.config(state = DISABLED)
            def click(event):
                if name_slot.get()=='Your Name':
                    name_slot.config(state=NORMAL)
                    name_slot.delete(0,END)
                else:
                    name_slot.config(state=NORMAL)
            def unclick(event):
                if name_slot.get() == '':
                    name_slot.delete(0,END)
                    name_slot.insert(0,'Your Name')
                    name_slot.config(state=DISABLED)
                else:
                    name_slot.config(state=DISABLED)
            # def click1(event):
            #     if message_slot.get("1.0","end")=='Feedback Message Here \U0001F979':
            #         message_slot.config(state=NORMAL)
            #         message_slot.delete("1.0","end")
            #     else:
            #         message_slot.config(state=NORMAL)
            # def unclick1(event):
            #     if message_slot.get("1.0","end") == '':
            #         message_slot.delete("1.0","end")
            #         message_slot.insert(INSERT,'Feedback Message Here \U0001F979')
            #         message_slot.config(state=DISABLED)
            #     else:
            #         message_slot.config(state=DISABLED)

            name_slot.bind("<Button-1>",click)
            name_slot.bind('<Leave>',unclick)
            frame_fb = Frame(master=root_fb)
            frame_fb.pack(fill=BOTH,expand=True)
            Label(frame_fb,text ='Feedback Message Here \U0001F979',font='Century 15', bg='ghostwhite').pack(fill=BOTH,expand=True)
            message_slot = Text(master=frame_fb,height= 15,width=15,font='Century 15', bg='ghostwhite')
            message_slot.pack(fill=BOTH,expand=True)
            bb=Button(root_fb,text='Back',font='Century 15', bg='ghostwhite',command= root_fb.destroy)
            bb.pack(anchor=W,side=LEFT,padx=5,pady=5)

            def SEND_FEEDBACK(message,name='None'):
                mail.feedback_mail(MESSAGE=message,PLAYERNAME=name)
                messagebox.showinfo(title='Feedback',message='Feedback sent successfully')
                root_fb.destroy()

            sb=Button(root_fb,text='Send',font='Century 15', bg='ghostwhite',command= lambda:(SEND_FEEDBACK(message=str(message_slot.get(1.0,END)),name=str(name_slot.get()))))
            sb.pack(anchor=E,side=RIGHT,padx=5,pady=5)
            # message_slot.config(state=DISABLED)
            # message_slot.bind("<Button-1>",click1)
            # message_slot.bind('<Leave>',unclick1)
            root_fb.mainloop()

        # Function Light theme

        def light_theme():
            global theme_val, remaining_chances, Frame1
            theme_val = 'L'
            try:
                game_win.config(bg='#fcf6e2')
                Frame1.config(bg='#fcf6e2')
                remaining_chances_label.config(bg='#fcf6e2', fg='green')
                details_label.config(bg='#fcf6e2', fg='red')
                word_label.config(bg='#fcf6e2', fg='black')
                imgLabel.config(
                    image=photos[no_of_Guesses], borderwidth=0, relief='solid')
                for i in range(97, 97+26):
                    if f'btn_{chr(i)}' not in btn_tracker_list:
                        eval(f'btn_{chr(i)}').config(
                            fg="#70330e", bg="#dcd6bf")
                if 'btn_space' not in btn_tracker_list:
                    btn_space.config(fg="#70330e", bg="#dcd6bf")
            except Exception:
                pass

            game_win.update()

        # Function Dark theme

        def dark_theme():
            global theme_val, Frame1
            theme_val = 'D'
            try:
                game_win.config(bg='#000b18')
                Frame1.config(bg='#000b18')
                remaining_chances_label.config(bg='#000b18', fg='#e71e65')
                details_label.config(bg='#000b18', fg='#fdda13')
                word_label.config(bg='#000b18', fg='#13cbff')
                imgLabel.config(
                    image=Dark_photos[no_of_Guesses], borderwidth=0, relief='solid')
                for i in range(97, 97+26):
                    if f'btn_{chr(i)}' not in btn_tracker_list:
                        eval(f'btn_{chr(i)}').config(
                            fg="#feeeb8", bg="#1f173d")
                if 'btn_space' not in btn_tracker_list:
                    btn_space.config(fg="#feeeb8", bg="#1f173d")

            except Exception:

                pass
            game_win.update()

        theme.add_radiobutton(
            label='Light', command=light_theme, variable=value_1, value=1)
        theme.add_radiobutton(
            label='Dark', command=dark_theme, variable=value_1, value=2)

        # Declaration of the Theme menu

        options_menu.add_cascade(label='Themes', menu=theme)
        options_menu.add_separator()
        options_menu.add_command(
            label='Change Password', command=reset_password_manually)
        options_menu.add_separator()

        options_menu.add_command(label='Delete Player', command=del_usr)
        options_menu.add_separator()

        options_menu.add_command(label='Quit', command=exit)
        bar.add_cascade(label='Options', menu=options_menu)

        how_menu = Menu(bar, tearoff=0, activebackground='coral')

        bar.add_cascade(label='How to play ?',
                        menu=how_menu, command=how_to_play)
        how_menu.add_command(label='Learn..', command=how_to_play)

        score_menu = Menu(bar, tearoff=0, activebackground='darkorange')
        bar.add_cascade(label='Score', menu=score_menu)
        score_menu.add_command(label='Leaderboard', command=leaderboard)

        credits_menu = Menu(bar, tearoff=0, activebackground='darkorange')

        bar.add_cascade(label='About', menu=credits_menu)
        credits_menu.add_command(label='Credits', command=credits)
        credits_menu.add_command(label='About Game', command=about_code)
        credits_menu.add_command(label='Source Code', command=source_code)
        credits_menu.add_separator()
        credits_menu.add_command(label='Feedback', command= Feedback_win)

        game_win.config(menu=bar)

        remaining_chances_label.config(text='Remaining chances : '+str(10))
        remaining_chances_label.pack(
            fill='both', expand=True, anchor=W, side=RIGHT, padx=160)

        global the_word_withsapces, repeats, error, repeats
        error = 0  # variable to track the error/left over chances
        the_word_withsapces = ''

        # initiate the game and the game window

        def GAME():

            global the_word, the_word_withsapces, no_of_Guesses, error, details_label, t
            game_win.resizable(0, 0)
            error = 0
            no_of_Guesses = 0

            # Checking Light or Dark theme

            if theme_val == 'L':
                imgLabel.config(image=photos[0])
            else:
                imgLabel.config(image=Dark_photos[0])

            # Checking Words selected.

            if str(type_game.get()) == 'Country Names':

                the_word = random.choice(main_data).upper()
                # print(the_word)
            else:
                the_word = random.choice(main_data).lower()
                # print(the_word)
            details_label.config(text='>Guess the '+(str(type_game.get())[0:(len((str(type_game.get())))-1)]) + ' with '+str(
                len(the_word)) + ' no. of letters.<')
            details_label.pack(fill='both', expand=True,
                               anchor=W, side=RIGHT, padx=20)

            the_word_withsapces = ' '.join(the_word)

            word_label.config(text=' '.join('_'*len(the_word)))

            if theme_val == 'D':
                dark_theme()
            else:
                light_theme()
        # function defined for passing the letter to the game

        def guess(letter):
            global remaining_chances_label, error, the_word_withsapces, no_of_Guesses

            key_winthout_spaces = the_word_withsapces.split(' ')
            key_winthout_spaces_str = ''

            # Configuring Blanks

            for l in key_winthout_spaces:
                key_winthout_spaces_str += l

            if letter in letter_track_list:  # Check for the letter input from keyboard.
                pass

            else:
                # if new letter found append it the respective list.
                letter_track_list.append(letter)

                # Gusses should be less or equal to 10
                # print(letter_track_list)

                if no_of_Guesses < 10:
                    txt = list(the_word_withsapces)
                    guessed = list(word_label['text'])
                    if the_word_withsapces.count(letter) > 0:

                        for c in range(len(txt)):
                            if txt[c] == letter:
                                guessed[c] = letter
                            word_label.config(text=''.join(guessed))
                            if word_label['text'] == the_word_withsapces:
                                if theme_val == 'L':
                                    imgLabel.config(image=photos[11])
                                else:
                                    imgLabel.config(image=Dark_photos[11])

                                # current Score to be updated

                                new_score = (10-error)*10
                                if new_score > old_score:
                                    score_update(new_score)
                                print('\a')
                                win = messagebox.askyesno(title='You Won!',
                                                          message=('\U0001F44F You Won!'+'\nGuessed right..It was '+the_word+'!\nYou\'r Score: '+str(new_score)), detail='Play once more ?')

                                if win:
                                    main()
                                else:
                                    exit()
                    # If Lost
                    else:

                        no_of_Guesses += 1
                        error += 1
                        remaining_chances(remaining_chances_label)
                        if no_of_Guesses in range(0, 10):
                            if theme_val == 'L':
                                imgLabel.config(image=photos[no_of_Guesses])
                            else:
                                imgLabel.config(
                                    image=Dark_photos[no_of_Guesses])
                        elif no_of_Guesses == 10:
                            if theme_val == 'L':
                                imgLabel.config(image=photos[10])
                            else:
                                imgLabel.config(image=Dark_photos[10])

                            lose = messagebox.askyesno(title='You are Hanged !',
                                                       message=(
                                                           '\U0001F974 Opps!! You are Hanged\nIt was '+key_winthout_spaces_str+'!'),
                                                       detail='Play once more ?')

                            if lose:
                                main()
                            else:
                                exit()

                        else:
                            pass

        if theme_val == 'D':
            dark_theme()
            imgLabel = Label(game_win)
            imgLabel.grid(row=0, column=0, columnspan=4, padx=10, pady=50)
            imgLabel.config(
                image=Dark_photos[0], borderwidth=0, relief='solid')
        else:
            light_theme()
            imgLabel = Label(game_win)
            imgLabel.grid(row=0, column=0, columnspan=4, padx=10, pady=50)
            imgLabel.config(image=photos[0], borderwidth=0, relief='solid')

        # Disabling the buttons after clicking

        def dis(bt):
            bt['state'] = 'disabled'
            bt['bg'] = '#093542'
            bt['highlightbackground'] = 'red'
            bt['disabledforeground'] = 'white'

        # Uppercase letters Buttons

        def upper_case():
            global btn_a, btn_b, btn_c, btn_d, btn_e, btn_f, btn_g, btn_h, btn_i, btn_j, btn_k, btn_l, btn_m, btn_n, btn_o, btn_p, btn_q, btn_r, btn_s, btn_t, btn_u, btn_v, btn_w, btn_x, btn_y, btn_z, btn_space

            btn_a = Button(game_win, text='A', command=lambda: (guess('A'), dis(btn_a), btn_track('btn_a')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_a.grid(row=1, column=0)

            btn_b = Button(game_win, text='B', command=lambda: (guess('B'), dis(btn_b), btn_track('btn_b')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_b.grid(row=1, column=1)

            btn_c = Button(game_win, text='C', command=lambda: (guess('C'), dis(btn_c), btn_track('btn_c')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_c.grid(row=1, column=2)

            btn_d = Button(game_win, text='D', command=lambda: (guess('D'), dis(btn_d), btn_track('btn_d')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_d.grid(row=1, column=3)

            btn_e = Button(game_win, text='E', command=lambda: (guess('E'), dis(btn_e), btn_track('btn_e')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_e.grid(row=1, column=4)

            btn_f = Button(game_win, text='F', command=lambda: (guess('F'), dis(btn_f), btn_track('btn_f')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_f.grid(row=1, column=5)

            btn_g = Button(game_win, text='G', command=lambda: (guess('G'), dis(btn_g), btn_track('btn_g')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_g.grid(row=1, column=6)

            btn_h = Button(game_win, text='H', command=lambda: (guess('H'), dis(btn_h), btn_track('btn_h')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_h.grid(row=1, column=7)

            btn_i = Button(game_win, text='I', command=lambda: (guess('I'), dis(btn_i), btn_track('btn_i')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_i.grid(row=1, column=8)

            btn_j = Button(game_win, text='J', command=lambda: (guess('J'), dis(btn_j), btn_track('btn_j')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_j.grid(row=2, column=0)

            btn_k = Button(game_win, text='K', command=lambda: (guess('K'), dis(btn_k), btn_track('btn_k')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_k.grid(row=2, column=1)

            btn_l = Button(game_win, text='L', command=lambda: (guess('L'), dis(btn_l), btn_track('btn_l')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_l.grid(row=2, column=2)

            btn_m = Button(game_win, text='M', command=lambda: (guess('M'), dis(btn_m), btn_track('btn_m')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_m.grid(row=2, column=3)

            btn_n = Button(game_win, text='N', command=lambda: (guess('N'), dis(btn_n), btn_track('btn_n')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_n.grid(row=2, column=4)

            btn_o = Button(game_win, text='O', command=lambda: (guess('O'), dis(btn_o), btn_track('btn_o')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_o.grid(row=2, column=5)

            btn_p = Button(game_win, text='P', command=lambda: (guess('P'), dis(btn_p), btn_track('btn_p')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_p.grid(row=2, column=6)

            btn_q = Button(game_win, text='Q', command=lambda: (guess('Q'), dis(btn_q), btn_track('btn_q')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_q.grid(row=2, column=7)

            btn_r = Button(game_win, text='R', command=lambda: (guess('R'), dis(btn_r), btn_track('btn_r')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_r.grid(row=2, column=8)

            btn_s = Button(game_win, text='S', command=lambda: (guess('S'), dis(btn_s), btn_track('btn_s')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_s.grid(row=3, column=0)

            btn_t = Button(game_win, text='T', command=lambda: (guess('T'), dis(btn_t), btn_track('btn_t')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_t.grid(row=3, column=1)

            btn_u = Button(game_win, text='U', command=lambda: (guess('U'), dis(btn_u), btn_track('btn_u')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_u.grid(row=3, column=2)

            btn_v = Button(game_win, text='V', command=lambda: (guess('V'), dis(btn_v), btn_track('btn_v')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_v.grid(row=3, column=3)

            btn_w = Button(game_win, text='W', command=lambda: (guess('W'), dis(btn_w), btn_track('btn_w')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_w.grid(row=3, column=4)

            btn_x = Button(game_win, text='X', command=lambda: (guess('X'), dis(btn_x), btn_track('btn_x')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_x.grid(row=3, column=5)

            btn_y = Button(game_win, text='Y', command=lambda: (guess('Y'), dis(btn_y), btn_track('btn_y')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_y.grid(row=3, column=6)

            btn_z = Button(game_win, text='Z', command=lambda: (guess('Z'), dis(btn_z), btn_track('btn_z')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_z.grid(row=3, column=7)

            btn_space = Button(game_win, text='Space', command=lambda: (guess(chr(32)), dis(btn_space), btn_track('btn_space')),
                               font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_space.grid(row=3, column=8)

            # Binding Buttons from keys from keyboard
            game_win.bind("<a>", lambda _: (
                guess("A"), dis(btn_a), btn_track('btn_a')))
            game_win.bind("<b>", lambda _: (
                guess("B"), dis(btn_b), btn_track('btn_b')))
            game_win.bind("<c>", lambda _: (
                guess("C"), dis(btn_c), btn_track('btn_c')))
            game_win.bind("<d>", lambda _: (
                guess("D"), dis(btn_d), btn_track('btn_d')))
            game_win.bind("<e>", lambda _: (
                guess("E"), dis(btn_e), btn_track('btn_e')))
            game_win.bind("<f>", lambda _: (
                guess("F"), dis(btn_f), btn_track('btn_f')))
            game_win.bind("<g>", lambda _: (
                guess("G"), dis(btn_g), btn_track('btn_g')))
            game_win.bind("<h>", lambda _: (
                guess("H"), dis(btn_h), btn_track('btn_h')))
            game_win.bind("<i>", lambda _: (
                guess("I"), dis(btn_i), btn_track('btn_i')))
            game_win.bind("<j>", lambda _: (
                guess("J"), dis(btn_j), btn_track('btn_j')))
            game_win.bind("<k>", lambda _: (
                guess("K"), dis(btn_k), btn_track('btn_k')))
            game_win.bind("<l>", lambda _: (
                guess("L"), dis(btn_l), btn_track('btn_l')))
            game_win.bind("<m>", lambda _: (
                guess("M"), dis(btn_m), btn_track('btn_m')))
            game_win.bind("<n>", lambda _: (
                guess("N"), dis(btn_n), btn_track('btn_n')))
            game_win.bind("<o>", lambda _: (
                guess("O"), dis(btn_o), btn_track('btn_o')))
            game_win.bind("<p>", lambda _: (
                guess("P"), dis(btn_p), btn_track('btn_p')))
            game_win.bind("<q>", lambda _: (
                guess("Q"), dis(btn_q), btn_track('btn_q')))
            game_win.bind("<r>", lambda _: (
                guess("R"), dis(btn_r), btn_track('btn_r')))
            game_win.bind("<s>", lambda _: (
                guess("S"), dis(btn_s), btn_track('btn_s')))
            game_win.bind("<t>", lambda _: (
                guess("T"), dis(btn_t), btn_track('btn_t')))
            game_win.bind("<u>", lambda _: (
                guess("U"), dis(btn_u), btn_track('btn_u')))
            game_win.bind("<v>", lambda _: (
                guess("V"), dis(btn_v), btn_track('btn_v')))
            game_win.bind("<w>", lambda _: (
                guess("W"), dis(btn_w), btn_track('btn_w')))
            game_win.bind("<x>", lambda _: (
                guess("X"), dis(btn_x), btn_track('btn_x')))
            game_win.bind("<y>", lambda _: (
                guess("Y"), dis(btn_y), btn_track('btn_y')))
            game_win.bind("<z>", lambda _: (
                guess("Z"), dis(btn_z), btn_track('btn_z')))
            game_win.bind("<space>", lambda _: (guess(chr(32)),
                          dis(btn_space), btn_track('btn_space')))

        # Lowercase Letters Button

        def lower_case():
            global btn_a, btn_b, btn_c, btn_d, btn_e, btn_f, btn_g, btn_h, btn_i, btn_j, btn_k, btn_l, btn_m, btn_n, btn_o, btn_p, btn_q, btn_r, btn_s, btn_t, btn_u, btn_v, btn_w, btn_x, btn_y, btn_z, btn_space

            btn_a = Button(game_win, text='a', command=lambda: (guess('a'), dis(btn_a), btn_track('btn_a')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_a.grid(row=1, column=0)

            btn_b = Button(game_win, text='b', command=lambda: (guess('b'), dis(btn_b), btn_track('btn_b')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_b.grid(row=1, column=1)

            btn_c = Button(game_win, text='c', command=lambda: (guess('c'), dis(btn_c), btn_track('btn_c')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_c.grid(row=1, column=2)

            btn_d = Button(game_win, text='d', command=lambda: (guess('d'), dis(btn_d), btn_track('btn_d')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_d.grid(row=1, column=3)

            btn_e = Button(game_win, text='e', command=lambda: (guess('e'), dis(btn_e), btn_track('btn_e')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_e.grid(row=1, column=4)

            btn_f = Button(game_win, text='f', command=lambda: (guess('f'), dis(btn_f), btn_track('btn_f')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_f.grid(row=1, column=5)

            btn_g = Button(game_win, text='g', command=lambda: (guess('g'), dis(btn_g), btn_track('btn_g')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_g.grid(row=1, column=6)

            btn_h = Button(game_win, text='h', command=lambda: (guess('h'), dis(btn_h), btn_track('btn_h')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_h.grid(row=1, column=7)

            btn_i = Button(game_win, text='i', command=lambda: (guess('i'), dis(btn_i), btn_track('btn_i')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_i.grid(row=1, column=8)

            btn_j = Button(game_win, text='j', command=lambda: (guess('j'), dis(btn_j), btn_track('btn_j')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_j.grid(row=2, column=0)

            btn_k = Button(game_win, text='k', command=lambda: (guess('k'), dis(btn_k), btn_track('btn_k')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_k.grid(row=2, column=1)

            btn_l = Button(game_win, text='l', command=lambda: (guess('l'), dis(btn_l), btn_track('btn_l')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_l.grid(row=2, column=2)

            btn_m = Button(game_win, text='m', command=lambda: (guess('m'), dis(btn_m), btn_track('btn_m')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_m.grid(row=2, column=3)

            btn_n = Button(game_win, text='n', command=lambda: (guess('n'), dis(btn_n), btn_track('btn_n')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_n.grid(row=2, column=4)

            btn_o = Button(game_win, text='o', command=lambda: (guess('o'), dis(btn_o), btn_track('btn_o')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_o.grid(row=2, column=5)

            btn_p = Button(game_win, text='p', command=lambda: (guess('p'), dis(btn_p), btn_track('btn_p')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_p.grid(row=2, column=6)

            btn_q = Button(game_win, text='q', command=lambda: (guess('q'), dis(btn_q), btn_track('btn_q')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_q.grid(row=2, column=7)

            btn_r = Button(game_win, text='r', command=lambda: (guess('r'), dis(btn_r), btn_track('btn_r')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_r.grid(row=2, column=8)

            btn_s = Button(game_win, text='s', command=lambda: (guess('s'), dis(btn_s), btn_track('btn_s')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_s.grid(row=3, column=0)

            btn_t = Button(game_win, text='t', command=lambda: (guess('t'), dis(btn_t), btn_track('btn_t')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_t.grid(row=3, column=1)

            btn_u = Button(game_win, text='u', command=lambda: (guess('u'), dis(btn_u), btn_track('btn_u')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_u.grid(row=3, column=2)

            btn_v = Button(game_win, text='v', command=lambda: (guess('v'), dis(btn_v), btn_track('btn_v')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_v.grid(row=3, column=3)

            btn_w = Button(game_win, text='w', command=lambda: (guess('w'), dis(btn_w), btn_track('btn_w')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_w.grid(row=3, column=4)

            btn_x = Button(game_win, text='x', command=lambda: (guess('x'), dis(btn_x), btn_track('btn_x')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_x.grid(row=3, column=5)

            btn_y = Button(game_win, text='y', command=lambda: (guess('y'), dis(btn_y), btn_track('btn_y')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_y.grid(row=3, column=6)

            btn_z = Button(game_win, text='z', command=lambda: (guess('z'), dis(btn_z), btn_track('btn_z')),
                           font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_z.grid(row=3, column=7)

            btn_space = Button(game_win, text='Space', command=lambda: (guess(chr(32)), dis(btn_space), btn_track('btn_space')),
                               font='Century 20', width=7, bg='#dcd6bf', relief='groove', cursor='hand2', borderwidth=1)
            btn_space.grid(row=3, column=8)

            # Binding Buttons from keyboard
            game_win.bind("<a>", lambda _: (
                guess("a"), dis(btn_a), btn_track('btn_a')))
            game_win.bind("<b>", lambda _: (
                guess("b"), dis(btn_b), btn_track('btn_b')))
            game_win.bind("<c>", lambda _: (
                guess("c"), dis(btn_c), btn_track('btn_c')))
            game_win.bind("<d>", lambda _: (
                guess("d"), dis(btn_d), btn_track('btn_d')))
            game_win.bind("<e>", lambda _: (
                guess("e"), dis(btn_e), btn_track('btn_e')))
            game_win.bind("<f>", lambda _: (
                guess("f"), dis(btn_f), btn_track('btn_f')))
            game_win.bind("<g>", lambda _: (
                guess("g"), dis(btn_g), btn_track('btn_g')))
            game_win.bind("<h>", lambda _: (
                guess("h"), dis(btn_h), btn_track('btn_h')))
            game_win.bind("<i>", lambda _: (
                guess("i"), dis(btn_i), btn_track('btn_i')))
            game_win.bind("<j>", lambda _: (
                guess("j"), dis(btn_j), btn_track('btn_j')))
            game_win.bind("<k>", lambda _: (
                guess("k"), dis(btn_k), btn_track('btn_k')))
            game_win.bind("<l>", lambda _: (
                guess("l"), dis(btn_l), btn_track('btn_l')))
            game_win.bind("<m>", lambda _: (
                guess("m"), dis(btn_m), btn_track('btn_m')))
            game_win.bind("<n>", lambda _: (
                guess("n"), dis(btn_n), btn_track('btn_n')))
            game_win.bind("<o>", lambda _: (
                guess("o"), dis(btn_o), btn_track('btn_o')))
            game_win.bind("<p>", lambda _: (
                guess("p"), dis(btn_p), btn_track('btn_p')))
            game_win.bind("<q>", lambda _: (
                guess("q"), dis(btn_q), btn_track('btn_q')))
            game_win.bind("<r>", lambda _: (
                guess("r"), dis(btn_r), btn_track('btn_r')))
            game_win.bind("<s>", lambda _: (
                guess("s"), dis(btn_s), btn_track('btn_s')))
            game_win.bind("<t>", lambda _: (
                guess("t"), dis(btn_t), btn_track('btn_t')))
            game_win.bind("<u>", lambda _: (
                guess("u"), dis(btn_u), btn_track('btn_u')))
            game_win.bind("<v>", lambda _: (
                guess("v"), dis(btn_v), btn_track('btn_v')))
            game_win.bind("<w>", lambda _: (
                guess("w"), dis(btn_w), btn_track('btn_w')))
            game_win.bind("<x>", lambda _: (
                guess("x"), dis(btn_x), btn_track('btn_x')))
            game_win.bind("<y>", lambda _: (
                guess("y"), dis(btn_y), btn_track('btn_y')))
            game_win.bind("<z>", lambda _: (
                guess("z"), dis(btn_z), btn_track('btn_z')))
            game_win.bind("<space>", lambda _: (guess(chr(32)),
                          dis(btn_space), btn_track('btn_space')))

        if str(type_game.get()) == 'Country Names':
            upper_case()
        else:
            lower_case()

        GAME()

        game_win.mainloop()

    main()


# Function to allow Existing player to enter the game

def old_player_start():
    global name, old_score, user_name, tg
    with open('authentication_file.json', encoding="utf8") as f:
        ld = json.load(f)
    f.close()
    current_all_name = ld.keys()
    user_name = str(name.get())
    tg = str(type_game.get())
    # print(tg)

    if user_name not in current_all_name or pass_word.get() != ld[user_name][1] or pass_word.get() == '':
        messagebox.showerror(title='User Error.',
                             message='Incorrect Username or Password', detail='Try again.')
    elif user_name in current_all_name and pass_word.get() == ld[user_name][1]:
        with open('authentication_file.json', encoding="utf8") as f:
            ld = json.load(f)
        old_score = (ld[user_name][0])

        login_screen.withdraw()
        main_game()

# function defined to reset the password manually


def reset_password_manually():
    global r_p_m
    try:
        if str(reset_screen.state()) == 'normal':
            reset_screen.destroy()
    except Exception:
        pass
    try:
        if str(root.state()) == 'normal':
            root.destroy()
    except:
        pass
    try:
        if str(login_screen.state()) == 'normal':
            login_screen.withdraw()
        if str(game_win.withdraw()) == 'normal':
            game_win.withdraw()

    except Exception:
        pass

    def change(usr_name, current_pass, new_pass):
        with open('authentication_file.json', encoding="utf8") as f:
            ld = json.load(f)
            f.close()
        try:
            if current_pass == ld[usr_name][1]:

                with open('authentication_file.json', 'w', encoding="utf8") as f:
                    ld[usr_name][1] = new_pass
                    json.dump(ld, f, indent=4)
                    f.close()
                mail.success_mail(
                    RECIEVERMAIL=ld[usr_name][2], PLAYERNAME=usr_name)
                ans = messagebox.askokcancel(
                    title='Change password', message='Changed Password successfully.')
                if ans == True:
                    try:
                        # BUG NOT ABLE TO CHANGE THE PASSWORD IF USER IS NEW.
                        login_screen.deiconify()
                        r_p_m.destroy()
                    except Exception:
                        main_screen.deiconify()
                        game_win.withdraw()
                        r_p_m.destroy()
                else:
                    exit()
            else:
                raise KeyError
        except KeyError:
            messagebox.showerror(title='Incorrect Details',
                                 message='Incorrect Username or Password')
    try:
        r_p_m = Toplevel(game_win, bg='ghostwhite')
    except Exception:
        r_p_m = Toplevel(login_screen, bg='ghostwhite')

        login_screen.withdraw()
    r_p_m.title('Change Password')
    r_p_m.geometry('360x120')
    logo1 = PhotoImage(file='pic2'+os.sep + 'GAME LOGO.png',
                       master=r_p_m)
    r_p_m.iconphoto(False, logo1)
    Label(r_p_m, text="Player Name :",
          font='Century 15', bg='ghostwhite').grid(row=1, column=1)
    user_name_local = ttk.Entry(r_p_m)
    user_name_local.grid(row=1, column=2)

    Label(r_p_m, text="Your current password :",
          font='Century 15', bg='ghostwhite').grid(row=2, column=1)
    old_user_pass = ttk.Entry(r_p_m)
    old_user_pass.grid(row=2, column=2)

    Label(r_p_m, text="Choose your Password :",
          font='Century 15', bg='ghostwhite').grid(row=3, column=1)

    new_user_pass = ttk.Entry(r_p_m)
    new_user_pass.grid(row=3, column=2)

    def back():
        try:
            if str(login_screen.state()) == 'withdrawn':
                login_screen.deiconify()
            r_p_m.destroy()
        except Exception:
            if str(game_win.state()) == 'withdrawn':
                game_win.deiconify()
            r_p_m.destroy()

    ttk.Button(r_p_m, text='Change Password', command=lambda: (change(str(user_name_local.get(
    )), str(old_user_pass.get()), str(new_user_pass.get())))).grid(row=4, column=2)
    back_btn = ttk.Button(r_p_m, text="Back", command=back)
    back_btn.grid(row=4, column=1)
    r_p_m.mainloop()

# function defined to reset the forgotten password


def forgot_password():
    global reset_screen

    try:
        if str(r_p_m.state()) == 'normal':
            r_p_m.destroy()

    except Exception:
        pass
    try:
        if str(root.state()) == 'normal':
            root.destroy()
    except:
        pass
    with open('authentication_file.json', encoding="utf8") as f:
        dic = json.load(f)
        f.close()

    def reset(mail_id):
        def change(name_reset, new_pass, usr_mail_id):
            with open('authentication_file.json', encoding="utf8") as f:
                ld = json.load(f)
                f.close()
            with open('authentication_file.json', 'w', encoding="utf8") as f:
                ld[name_reset][1] = new_pass
                json.dump(ld, f, indent=4)
                f.close()
            mail.success_mail(RECIEVERMAIL=usr_mail_id, PLAYERNAME=name_reset)
            ans = messagebox.askokcancel(
                title='OTP Authentication successful', message='Successfully Done')
            if ans == True:
                login_screen.deiconify()
                reset_s.destroy()
            else:
                quit

        if local_otp.get() == mail.otp_temp:
            reset_s = Toplevel(reset_screen)
            reset_s.title('New Password')
            reset_screen.withdraw()
            Label(reset_s, text="Choose your Password.:",
                  font='Century 15', bg='ghostwhite').grid(row=1, column=1)
            new_user_pass = ttk.Entry(reset_s)
            new_user_pass.grid(row=2, column=1)
            ttk.Button(reset_s, text='Change Password', command=lambda: (change(
                name_reset=str(usr_name_to_reset.get()), new_pass=str(new_user_pass.get()), usr_mail_id=mail_id))).grid(row=3, column=1)

            reset_s.mainloop()

        else:
            ans = messagebox.askyesno(
                title='OTP Error', message='Incorrect/Invalid OTP \n click send OTP to Resend OPT.')
            if ans == True:
                mail.send_mail(RECIEVERMAIL=mail_id,
                               PLAYERNAME=str(usr_name_to_reset.get()))
            else:
                quit
    reset_screen = Toplevel(main_screen)
    reset_screen.geometry('300x120')
    login_screen.withdraw()
    reset_screen.title('Reset your Password.')
    logo1 = PhotoImage(file='pic2'+os.sep +
                       'GAME LOGO.png', master=login_screen)
    reset_screen.iconphoto(False, logo1)

    reset_screen.resizable(0, 0)
    reset_screen.config(bg='ghostwhite')

    Label(reset_screen, text="Your Username:",
          font='Century 15', bg='ghostwhite').grid(row=1, column=0, sticky=W)
    usr_name_to_reset = ttk.Entry(reset_screen, background='ghostwhite')
    if str(name.get()) != '':
        usr_name_to_reset.insert(0, str(name.get()))
    usr_name_to_reset.grid(row=1, column=1)
    Label(reset_screen, text="Mail ID:",
          font='Century 15', bg='ghostwhite').grid(row=2, column=0, sticky=W)
    usr_mail_id_to_reset = ttk.Entry(reset_screen, background='ghostwhite')
    usr_mail_id_to_reset.grid(row=2, column=1)

    def click(event):
        if local_otp.get() == '   Your OTP':
            local_otp.config(state=NORMAL)
            local_otp.delete(0, END)
        else:
            local_otp.config(state=NORMAL)

    def unclick(event):
        if local_otp.get() == '':
            local_otp.delete(0, END)
            local_otp.insert(0, '   Your OTP')
            local_otp.config(state=DISABLED)
        else:
            local_otp.config(state=DISABLED)
    local_otp = ttk.Entry(reset_screen, background='ghostwhite')
    local_otp.insert(0, '   Your OTP')
    local_otp.config(state=DISABLED)
    local_otp.bind("<Button-1>", click)
    local_otp.bind('<Leave>', unclick)
    local_otp.grid(row=3, column=0)

    def send_1():
        try:
            if (dic[str(usr_name_to_reset.get())][2]) == str(usr_mail_id_to_reset.get()):
                mail.send_mail(RECIEVERMAIL=str(usr_mail_id_to_reset.get()),
                               PLAYERNAME=str(usr_name_to_reset.get()))
            else:
                messagebox.showerror(title='Incorrect Mail Id',
                                     message='Incorrect mail id\nor\nInvalid mail id')
        except KeyError:
            messagebox.showerror(title='Incorrect Username',
                                 message='Incorrect Username Provided.')

    otp_button = ttk.Button(reset_screen, text='Send OTP', command=send_1)
    otp_button.grid(row=3, column=1)
    back_btn = ttk.Button(reset_screen, text='Back', command=lambda: (
        login_screen.deiconify(), reset_screen.destroy()))
    back_btn.grid(row=4, column=0)

    pass_reset = ttk.Button(reset_screen, text='Reset', command=lambda: (reset(usr_mail_id_to_reset.get())
                                                                         ))
    pass_reset.grid(row=4, column=1)

    reset_screen.mainloop()

# Function to Login to the Game i.e Authentication


def login():
    global name, login_screen, type_game, pass_word
    login_screen = Toplevel(main_screen)
    main_screen.withdraw()
    login_screen.title("Existing Player.")
    menubar = Menu(login_screen)
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Passwords & Accounts', menu=file)
    file.add_command(label='Forgot Password', command=forgot_password)
    file.add_command(label='Change Password', command=reset_password_manually)
    file.add_separator()
    file.add_command(label='Delete Player', command=del_usr)
    file.add_separator()
    file.add_command(label='Exit', command=quit)
    login_screen.config(menu=menubar)
    logo1 = PhotoImage(file='pic2'+os.sep +
                       'GAME LOGO.png', master=login_screen)
    login_screen.iconphoto(False, logo1)
    login_screen.geometry("320x180")
    login_screen.resizable(0, 0)
    login_screen.config(bg='ghostwhite')
    Label(login_screen, bg='ghostwhite', text='').grid(row=0, column=0)
    Label(login_screen, text="Your Username:",
          font='Century 15', bg='ghostwhite').grid(row=1, column=0, sticky=W)
    name = ttk.Entry(login_screen)
    name.grid(row=1, column=1)
    Label(login_screen, text="Enter Password.. ",
          font='Century 15', bg='ghostwhite').grid(row=2, column=0, sticky=W)
    pass_word = ttk.Entry(login_screen)
    pass_word.grid(row=2, column=1)
    Label(login_screen, text="Play with - ",
          font='Century 15', bg='ghostwhite').grid(row=3, column=0, sticky=W)
    options = ['Colors', 'Country Names', 'Python Keywords']
    type_game = StringVar(login_screen)
    type_game.set("Python Keywords")  # default value

    w = ttk.Combobox(login_screen, textvariable=type_game,
                     values=options, width=17)

    w.grid(row=3, column=1)
    Label(login_screen, bg='ghostwhite', text='').grid(row=4, column=0)
    play_btn = ttk.Button(login_screen, text="Let's play !",
                          command=old_player_start)
    play_btn.grid(row=5, column=1)
    login_screen.bind('<Return>', lambda _: old_player_start())
    back_btn = ttk.Button(login_screen, text="Back", command=lambda: (
        main_screen.deiconify(), login_screen.destroy()))
    back_btn.grid(row=5, column=0)
    login_screen.bind('<Escape>', lambda _: (
        main_screen.deiconify(), login_screen.destroy()))
    login_screen.protocol('WM_DELETE_WINDOW', exit)

    login_screen.mainloop()

# function defined to suggest usernames for the common usernames


def suggestions(current_try):
    local_syb = '!@#$%^&*()-+_~?><'
    temp = []
    i = 1
    while i <= 3:
        temp.append(
            current_try+str(local_syb[random.randrange(len(local_syb))])+str(random.randrange(10)))

        i += 1
    return temp


# functio to Add and allowing New user to add his username and Allow him play the game.

def new_player_add():
    global user_name, old_score
    new_user = (str(name.get()))
    if new_user in current_all_name:
        ans = messagebox.askretrycancel(
            title='Error!', message='Username already exist !', detail=f'Retry using different username.\nConsider therse suggestions.\n{suggestions(new_user)}')
        if ans:
            register_screen.destroy()
            register()
        else:
            exit()
    else:
        with open('authentication_file.json', encoding="utf8") as f:
            ld = json.load(f)
        f.close()
        user_name = new_user

        try:
            mail.created_mail(RECIEVERMAIL=str(
                usr_mail_id.get()), PLAYERNAME=user_name)
            with open('authentication_file.json', 'w', encoding="utf8") as f:
                ld[user_name] = [old_score, pass_word_new.get(), usr_mail_id.get()]
                json.dump(ld, f, indent=4)
            f.close()
        except Exception as e:
            if f'The recipient address <{str(usr_mail_id.get())}> is not a valid RFC' in str(e):

                ans = messagebox.askretrycancel(
                    title='Error!', message=f'The recipient mail address "{str(usr_mail_id.get())}" is not a valid mail address.', detail='Please check you email id or its status.')
            else:
                ans = messagebox.askretrycancel(
                    title='Error!', message=e, detail='Please check you email id or its status.')
            if ans:
                register_screen.destroy()
                register()
            else:
                exit()

        register_screen.destroy()
        main_game()

# Function to create a new "New User window"


def register():
    global name, old_score, user_name, current_all_name, register_screen, type_game, pass_word_new, usr_mail_id
    with open('authentication_file.json', encoding="utf8") as f:
        ld = json.load(f)
    f.close()
    current_all_name = ld.keys()

    old_score = 0
    register_screen = Tk()
    main_screen.withdraw()
    logo1 = PhotoImage(file='pic2'+os.sep + 'GAME LOGO.png',
                       master=register_screen)
    register_screen.iconphoto(False, logo1)
    register_screen.config(bg='ghostwhite')
    register_screen.title("New Player.")
    register_screen.geometry("320x200")
    register_screen.resizable(0, 0)
    Label(register_screen, bg='ghostwhite', text='').grid(row=0, column=0)
    Label(register_screen, text="Player Name: ",
          font='Century 15', bg='ghostwhite').grid(row=1, column=0, sticky=W)
    name = ttk.Entry(register_screen)
    name.grid(row=1, column=1)
    Label(register_screen, text="Choose Password..",
          font='Century 15', bg='ghostwhite').grid(row=2, column=0, sticky=W)
    pass_word_new = ttk.Entry(register_screen)
    pass_word_new.grid(row=2, column=1)

    Label(register_screen, text="Your Mail ID  ..",
          font='Century 15', bg='ghostwhite').grid(row=3, column=0, sticky=W)
    usr_mail_id = ttk.Entry(register_screen)
    usr_mail_id.grid(row=3, column=1)

    Label(register_screen, text="Play with - ",
          font='Century 15', bg='ghostwhite').grid(row=4, column=0, sticky=W)

    # List of words that can be assigned to the dashes i.e to the game
    options = ["Python Keywords", "Country Names", "Colors"]
    type_game = StringVar(register_screen)
    type_game.set("Python Keywords")  # default value

    w = ttk.Combobox(register_screen, textvariable=type_game,
                     values=options, width=17)

    w.grid(row=4, column=1)
    Label(register_screen, bg='ghostwhite', text='').grid(row=5, column=0)
    ttk.Button(register_screen, text="Let's Start !",
               command=new_player_add).grid(row=6, column=1)
    ttk.Button(register_screen, text="Back", command=lambda: (
        main_screen.deiconify(), register_screen.destroy())).grid(row=6, column=0)
    register_screen.protocol('WM_DELETE_WINDOW', exit)
    register_screen.bind('<Return>', lambda _: new_player_add())
    register_screen.bind('<Escape>', lambda _: (
        main_screen.deiconify(), register_screen.destroy()))
    register_screen.mainloop()

# Main welcome screen . New user or Existing user


def main_screen_fn():
    global main_screen, value_1
    main_screen = Tk()
    logo1 = PhotoImage(file='pic2'+os.sep + 'GAME LOGO.png', master=main_screen)
    main_screen.iconphoto(False, logo1)
    main_screen.geometry("300x250")
    main_screen.title("Hello Player !")
    main_screen.config(bg='ghostwhite')

    value_1 = IntVar(main_screen)

    Label(text="Let's Play ! ", bg="darkorange", fg='black',
          width="300", height="4", font=("Century 16")).pack()
    Label(text="", bg='black').pack()
    b1 = Button(text="Existing Player.", height="2", width="30", command=login,
                bg='white', relief='groove', cursor='hand2', borderwidth=1, font='Century 10')
    b1.pack()
    b1.bind('<Motion>', lambda _: b1.config(
        bg='yellowgreen', highlightbackground='yellowgreen'))
    b1.bind('<Leave>', lambda _: b1.config(
        bg='white', highlightbackground='white'))
    Label(text="", bg='black').pack()
    b2 = Button(text="New Player.", height="2", width="30", command=register,
                bg='white', relief='groove', cursor='hand2', borderwidth=1, font='Century 10')
    b2.bind('<Motion>', lambda _: b2.config(
        bg='yellowgreen', highlightbackground='yellowgreen'))
    b2.bind('<Leave>', lambda _: b2.config(
        bg='white', highlightbackground='white'))
    b2.pack()

    main_screen.mainloop()


# calling the main_screen function to launche the whole game

main_screen_fn()

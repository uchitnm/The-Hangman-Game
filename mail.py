# imported modules

import smtplib
import os
import random
from datetime import date
import time

username = '<MAIL ID>'
userpassword = '<MAIL ID PASSWORD>'


# Function to inciate mail for Successful creating of account. 

def created_mail(RECIEVERMAIL, SENDERMAIL=username, PLAYERNAME='there'):
    subject = 'Hangman GUI Account Created successfully.'
    body = f'Hi {PLAYERNAME}!\nWelcome to our Game {PLAYERNAME},Your Hangman Account is Created on {date.today().strftime("%d/%m/%Y")} at {time.strftime("%H:%M:%S")} IST.\nWe wish you a Happy Playing Experience.\n\nThank you.\nTeam Hangman GUI.'
    msg = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(username, userpassword)

        smtp.sendmail(SENDERMAIL, RECIEVERMAIL, msg)

# Function to inciate mail for Successful deletion of Accound. 

def del_mail(RECIEVERMAIL, SENDERMAIL=username, PLAYERNAME='there'):
    subject = 'Your Account has been Deleted.'
    body = f'Hi {PLAYERNAME}!\nYour Hangman Account has been Deleted on {date.today().strftime("%d/%m/%Y")} at {time.strftime("%H:%M:%S")} IST.\nSorry to leave you. We wish you join us back.\n\nThank you.\nTeam Hangman GUI.'
    msg = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(username, userpassword)

        smtp.sendmail(SENDERMAIL, RECIEVERMAIL, msg)

# OTP Creater.

def otp():
    opt_to_send = ''
    while len(opt_to_send) < 6:
        opt_to_send += str(random.randint(0, 9))

    return opt_to_send

# Function to inciate mail for Successful changing of password 

def success_mail(RECIEVERMAIL, SENDERMAIL=username, PLAYERNAME='there'):

    subject = 'Passsword Successfully Changed.'
    body = f'Hi {PLAYERNAME}!\nYour password has been Successfully updated on {date.today().strftime("%d/%m/%Y")} at {time.strftime("%H:%M:%S")} IST.\nWe hope you have choosen a Password that is strong and you can rembember it.\n\nThank you.\nTeam Hangman GUI.'
    msg = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(username, userpassword)

        smtp.sendmail(SENDERMAIL, RECIEVERMAIL, msg)

# Function to inciate sending OTP mail  

def send_mail(RECIEVERMAIL, SENDERMAIL=username, PLAYERNAME='there'):
    global otp_temp
    otp_temp = otp()
    subject = 'Passsword reset Request.'
    body = f'Hi {PLAYERNAME}!\nUse the OTP to Reset your Password generated on {date.today().strftime("%d/%m/%Y")} at {time.strftime("%H:%M:%S")} IST.\nOTP : {otp_temp}\nWe suggest to choose a Password that is strong and you can rembember it.\n\nThank you.\nTeam Hangman GUI.'
    msg = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(username, userpassword)

            smtp.sendmail(SENDERMAIL, RECIEVERMAIL, msg)
        except Exception :
            pass


def feedback_mail(MESSAGE = '' ,RECIEVERMAIL=username, SENDERMAIL=username, PLAYERNAME = 'Autonomous' , MAILID = 'None'):
    subject = f'Feedback from {PLAYERNAME}.'
    body = f'This is a feedback from {PLAYERNAME} of Mail ID {MAILID}\n-----\n{MESSAGE}\n-----'
    msg = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(username, userpassword)

        smtp.sendmail(SENDERMAIL, RECIEVERMAIL, msg)


if __name__ == '__main__':
    reciever_mail = input('Enter the mail id to whom we need to send: ')
    send_mail(SENDERMAIL=username, RECIEVERMAIL=reciever_mail)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 3, 2012, 1:32:18 PM

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from smtplib import SMTP, SMTPAuthenticationError, SMTPException,\
                    SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError
from socket import sslerror

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "EmailError", 
    "send_email_base", 
    "send_email"
]

#: -- EmailError ----------------------------------------------------------------

class EmailError(Exception):
    def __init__(self, eid=-1, message=None):
        self.__eid = eid
        self.__message = message
    
    @property
    def eid(self):
        return self.__eid
    
    @property
    def emessage(self):
        return self.__message

#: -- send_mail ----------------------------------------------------------------

def send_email_base(subject, body, attachments=None, email_from=None, 
                    email_to=None, email_cc=None, email_bcc=None,
                    server="localhost", port=25, username="", password="", 
                    use_tls=False):
    
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = email_to
    
    dest_to_addrs = [email_to]
    
    if email_cc:
        message["Cc"] = email_cc
        dest_to_addrs += email_cc
    
    if email_bcc:
        dest_to_addrs += email_bcc
    
    message["Date"] = formatdate(localtime=True)
    message.preamble = "You'll not see this in a MIME-aware mail reader.\n"
    message.attach(MIMEText(body))
    
    socket = SMTP(server, port)
        
    if server != "localhost":
        try:
            if use_tls:
                socket.ehlo()
                socket.starttls()
                socket.ehlo()
            socket.login(username, password)
        except SMTPAuthenticationError:
            raise EmailError(3, "Authentication error.")
        except SMTPException:
            raise EmailError(4, "No suitable authentication method.")
            
    try:
        socket.sendmail(email_from, dest_to_addrs, message.as_string())
    except SMTPRecipientsRefused:
        raise EmailError(5, "All recipients were refused."
                            "Nobody got the mail.")
    except SMTPSenderRefused:
        raise EmailError(6, "The server didn't accept the from_addr.")
    except SMTPDataError:
        raise EmailError(7, "An unexpected error code, Data refused.")
    
    try:
        socket.quit()
    except sslerror:
        socket.close()
    
def send_email(subject, body, attachments=None, 
               email_from=None, email_to=None, email_cc=None, email_bcc=None,
               server="localhost", port=25, username="", password="", 
               use_tls=False):
    try:
        send_email_base(subject, body, attachments, 
                        email_from, email_to, email_cc, email_bcc, 
                        server, port, username, password, use_tls)
        return True
    except EmailError as E:
        print E
        return False

#: -- send_mail ----------------------------------------------------------------

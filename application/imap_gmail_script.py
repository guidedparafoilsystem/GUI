#!/usr/bin/python3
import getpass
import imaplib
import email
import os
from datetime import datetime
import pytz
import socket


def format_time(time):
    if time:
        hours = str((int(time[0:2])-7)%24)
        if len(hours) < 2:
            hours = '0'+hours
        mins = time[2:4]
        if len(mins) < 2:
            hours = '0'+hours
        secs = time[4:6]
        if len(secs) < 2:
            hours = '0'+hours
        time = hours + ':' + mins + ':' + secs
    return time
        
def format_longitude(longitude, card):
    if longitude:
        deg = int(longitude[0:3])
        sec = float(longitude[3:])
        longitude =  deg+sec/60
        if card is 'W':
            longitude = longitude * -1
            return str(longitude)[:10]
        else:
            return str(longitude)[:9]
        

def format_latitude(latitude, card):
    if latitude:
        deg = int(latitude[0:2])
        sec = float(latitude[2:])
        latitude = deg+sec/60
        if card is 'S':
            latitude = latitude*-1
            return str(latitude)[:9]
        else:
            return str(latitude)[:8]
        
    
def attachment_handler(attachment):
    diag_dict = {}
    extra_data = attachment.split('/')
    gps_sentence = extra_data[0].split(',')
    diag_dict['Pressure'] = extra_data[2]
    diag_dict['Temperature'] = extra_data[1]
    if 'not' in extra_data[3]:
        diag_dict["cutdown"] = extra_data[3]
    else:
        diag_dict["cutdown"] = extra_data[3]
    for num, entry in enumerate(gps_sentence):
        if entry != '$GPGGA':# This approach works as long as we use this format
            continue
        else:
            diag_dict['Time'] = format_time(gps_sentence[num+1])
            diag_dict['Latitude'] = format_latitude(gps_sentence[num+2],
                                                    gps_sentence[num+3])
            diag_dict['Longitude'] = format_longitude(gps_sentence[num+4], 
                                                      gps_sentence[num+5])
            diag_dict['Satellites'] = gps_sentence[num+7]
            diag_dict['Altitude'] = gps_sentence[num+9]
            
    return diag_dict

def search_mail(mail_handle):
    ########### Create a query to search for new mail ###########
    form = "%d-%b-%Y"
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(pytz.timezone('US/Pacific'))
    s = date.strftime(form)
    query = "(FROM \"uivast1\" SINCE \"" + s + "\")"
    # print(query)
    typ, data = mail_handle.search(None, query)  
    
    if typ != 'OK':                                 #typ is for error checking
       print("Error searching mail.")               #data is a tuple of msg num
    
    return data

def fetch_mail(mail_handle, msgId):
    typ, messageParts = mail_handle.fetch(msgId, '(RFC822)')
    if typ != 'OK':
        print("Error fetching mail.")
    emailBody = messageParts[0][1]
    mail = email.message_from_bytes(emailBody)
    diagnostics = []
    for part in mail.walk():
        if part.is_multipart():
            continue
        if part.get('Content-Disposition') is None:
            continue
        if part.get('Content-Disposition') == "inline":
            continue
        attachment = part.get_payload(decode=True).decode("utf-8", "ignore")
        diagnostics = attachment_handler(attachment)
    return diagnostics

    
def main():
    ########### Open IMAP connection to Gmail ##############
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login("Guidedparafoilsystem@gmail.com", "SeniorDesign2015") 
    M.select()
    msgID = 0
    data = search_mail(M)
    if not data[0]:
        return {}
    msgID = data[0].split()[-1]
    diag = fetch_mail(M, msgID)
    diag['msg'] = str(int(msgID))
    M.close()
    M.logout()
    return diag
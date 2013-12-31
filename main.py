from sys import exit
from subprocess import call
from os import path, popen, listdir
from getpass import getpass
import xml.etree.ElementTree as ET
from shutil import copy2

cur_path = path.dirname(path.realpath('main.py')) + '/'
# Useful for when directory names have a space in them (gasp)
# This has been tested, but not thoroughly. Directories shouldn't have
# spaces in them.
cur_path_with_slash = '\ '.join(cur_path.split(' '))
with open(cur_path + 'backup_path.txt', 'rU') as file_:
    backupPath = file_.readline().strip()

pphrase = getpass('Enter passphrase, or enter \'o\' or \'s\': ')

action = 'normal'
if pphrase == 'o':
    action = 'o'
    pphrase = getpass('Enter passphrase to access options: ')
elif pphrase == 's':
    action = 's'
    pphrase = getpass('Enter passphrase:')

def get_date_time():
    '''Returns the time-and-date string that you get from entering 'date'
    into the terminal.
    '''
    bash_output = popen('date')
    date_time = bash_output.readline().strip()
    return date_time

def remove_slashes(string):
    '''Removes the 'extra' slashes from a string. For example:
    '/home/Bad\\ Directory/' --> '/home/Bad Directory/'
    '''
    return ''.join(string.split('\\'))

def crack(file_path, file_name, key=pphrase):
    '''Replaces the encrypted file denoted by FILE_NAME with the
    corresponding unencypted file.
    '''
    full_name = file_path + file_name
    full_name_nc = full_name + '.nc'
    decrypt_cmd = 'mcrypt -d -q ' + full_name_nc + ' -k ' + key
    call(decrypt_cmd, shell=True)
    # check to see if decryption was successful
    filelist = listdir(remove_slashes(file_path)+'.')
    decryptSuccess = remove_slashes(file_name) in filelist
    if not decryptSuccess:
        print 'Decryption failed.'
        exit(1) 
    else:    
        rm_old_nc_cmd = 'shred -u ' + full_name_nc   
        call(rm_old_nc_cmd, shell=True)

def open_helper(file_path, file_name, openWith):
    '''Opens the file denoted by FILE_NAME and FILE_PATH using the bash
    command denoted by OPENWITH.
    '''
    open_cmd = openWith + ' ' + file_path + file_name
    call(open_cmd, shell=True)

def seal(file_path, file_name, key=pphrase):
    '''Encrypts the file denoted by FILE_NAME and file_path.'''
    full_name = file_path + file_name
    full_name_nc = full_name + '.nc'
    encrypt_cmd = 'mcrypt -q ' + full_name + ' -k ' + key
    rmOld2_cmd = 'shred -u ' + full_name
    call(encrypt_cmd, shell=True)
    call(rmOld2_cmd, shell=True)

def backup(file_path, file_name):
    '''Sends an encrypted copy of the file denoted by FILE_NAME and 
    FILE_PATH to the backup folder.
    '''
    full_name = file_path + file_name
    full_name_nc = full_name + '.nc'
    backup = backupPath + file_name + '.nc'
    copy2(remove_slashes(full_name_nc), remove_slashes(backup))

def open_(file_path, file_name, openWith, should_backup, key=pphrase):
    '''Decrypts the file denoted by FILE_NAME and FILE_PATH; opens it using
    the bash command OPENWITH; and then re-encrypts and backs up  the file
    when it is closed.
    '''
    full_name = file_path + file_name
    if path.exists(remove_slashes(full_name + '.nc')):
        crack(file_path, file_name, key)
        open_helper(file_path, file_name, openWith)
        seal(file_path, file_name, key)
        if should_backup:
            backup(file_path, file_name)
    elif path.exists(remove_slashes(full_name)):
        print 'Note:', file_name, 'not found encrypted. Using unencrypted.'
        open_helper(file_path, file_name, openWith)
    else:
        print file_name, 'not found.'

def get_from_XML(XML_file):
    '''Returns a two-dimensional list with some information from XML_FILE.
    '''
    tree = ET.parse(cur_path + XML_file)
    root = tree.getroot()
    filelist = []    
    for child in root:
        appendThis = [child.attrib['name'], {}]
        for part in child:
            appendThis[1][part.tag] = part.text
        filelist.append(appendThis)
    return filelist

if path.exists(cur_path + 'info.xml.nc'):
    print 'hi'
    crack(cur_path_with_slash, 'info.xml')
    filelist = get_from_XML('info.xml')
    seal(cur_path_with_slash, 'info.xml')
else:  # assume info.xml is not encrypted
    filelist = get_from_XML('info.xml')

if action == 'normal' or action == 'o':
    if action == 'normal':
        srcDict = filelist[0][1]
    elif action == 'o':
        for i in range(len(filelist)):
            output = str(i) + '     ' + filelist[i][0]
            print output
        num = int(raw_input('Choose a file number: '))
        srcDict = filelist[num][1]
    file_path = srcDict['path']
    file_name = srcDict['name']
    opener = srcDict['openwith']
    should_backup = int(srcDict['backup'])
    open_(file_path, file_name, opener, should_backup)

elif action == 's':
    srcDict = filelist[0][1]
    file_name = srcDict['name']
    file_path = srcDict['path']
    should_backup = int(srcDict['backup'])
    full_name = file_path + file_name
    crack(file_path, file_name)
    thefile = open(full_name, 'a')
    date1 = get_date_time()
    text = getpass('-' * 60 + '\n')
    date2 = get_date_time()
    text = date1 + '\n' + text + '\n' + date2 + '\n\n'
    thefile.write(text)
    thefile.close()
    seal(file_path, file_name)
    if should_backup:
        backup(file_path, file_name)

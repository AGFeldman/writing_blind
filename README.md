The main feature of this script is that it allows you to write personal notes without the writing appearing on-screen. I run this script from a hotkey when I'm at college.

The script also makes sure that the files you use it with are encrypted at all times when you're not editing the files, and it can send a backup of the encrypted file to a different folder when you're done editing.

The script has been tested with Ubuntu 13.10. It will probably work on UNIX. It won't work on Windows.

In order to use this script, you need to have mcrypt installed. You should
 edit the backup_path.txt file to point to the directory where you'd like to send backups of the encrypted files. The directory that you specify should begin and end with a forward slash. (You don't need to use the backup feature. If you don't use it at all, then you don't need to edit the backup_path.txt file.)

Which files should this script open? Specify them in info.xml. The fields are name, openwith, path, and backup. openwith specifies that terminal command that should may be used to open the file. path specifies where to find the file, and it should begin and end with a forward slash. backup indicates whether or not to send an encrypted copy of the file to the backup folder. A 1 indicates that a backup should be sent, and a 0 indicates that it shouldn't.

The first file specified in info.xml is the one that that the main feature works with. It should be encrypted with mcrypt. If you want to use this script with multiple encrypted files, then they should all be encrypted with the same key.

When the script is launched, it says to enter your passphrase, or 'o', or 's'. If you enter your passphrase, then it will decrypt the first file specified in info.xml and open it with the terminal command speicified in info.xml. When you close the file, the script will re-encrypt it and, if specified in info.xml, send a copy of the encrypted file to the backup folder.

If you enter 'o', then the names of all the files discussed in info.xml will be printed to the terminal. The file that you choose will be decrypted, opened, re-encrypted, and possible backed up.

Enter 's' to edit the first file in info.xml without the files contents appearing on screen. After you enter the passphrase, the file will be decrypted. Then, any text that you enter into the terminal will not appear on screen, until you hit enter. Then, this text will be appended to the file, which will then be re-encrypted, and, if specified in info.xml, backed up. 

Entering 's' will also add the time and date of edits to the special file, which is useful for journal entries.

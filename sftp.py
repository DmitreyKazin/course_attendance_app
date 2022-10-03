#!/usr/bin/env python3

"""
This script downloads csv files from a remote machine.
"""

import os
import paramiko
from dotenv import load_dotenv

RMT_PATH = '/var/tmp/csv_files'
LOCAL_PATH = './csv_files'

load_dotenv()

def download_all_csv():
	# creating a directory
	try:
	    os.mkdir('csv_files')
	except:
	    print('ERR - csv_files directory exists')
	# download files
	transport = paramiko.Transport((os.getenv('RMT_HOST'), 22))
	transport.connect(username=os.getenv('RMT_USER'),
			  password=os.getenv('RMT_PASSWD'))
	sftp = paramiko.SFTPClient.from_transport(transport)

	for file in sftp.listdir(path=RMT_PATH):
		sftp.get(os.path.join(RMT_PATH,file),
			 os.path.join(LOCAL_PATH, file))

	sftp.close()
	transport.close()

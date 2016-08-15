# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import json
import datetime
import requests

if __name__ == "__main__":

	argvs = sys.argv  
	argc = len(argvs) 

	if (argc != 4):
	    print('Usage: # python %s filename output_dir token' % argvs[0])
	    print('Example: python slack_file_download.py ./private_channels/op_analytics_squad.json ./attachment-files xxxxxxxxxxxxxx')
	    quit()

	filename = argvs[1]
	output_dir = argvs[2]
	token = argvs[3]

	f = open(filename, 'r')
	jsonData = json.load(f)
	f.close()

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)


	metadata = open('metadata.json', 'r')
	users = json.load(metadata)["users"]
	metadata.close()

	# for msg in jsonData["messages"]:
	# 	print ("%s" % json.dumps(msg, ensure_ascii=False, indent=2))

	for msg in reversed(jsonData["messages"]):
		user = ""
		ts = ""
		if "user" in msg:
			user = users[msg["user"]]
		if "ts" in msg:
			ts = datetime.datetime.fromtimestamp(float(msg["ts"])).strftime( '%Y-%m-%d %H:%M:%S' )

		# if "text" in msg:
		# 	print ('[%s] %s : %s' % (ts, user,msg["text"]))
		# else:
		# 	print ('[%s] %s : %s' % (ts, user, json.dumps(msg, ensure_ascii=False, indent=2)))
		if "file" in msg:
			if not user and msg["subtype"]=="file_comment":
				continue
			file_id = msg["file"]["id"]
			url_private_download = msg["file"]["url_private_download"]
			fn = url_private_download.split('/')[-1]
			fdir = os.path.join(output_dir, user, file_id)
			#os.makedirs(fdir, exist_ok=True)
			if os.path.exists(fdir):
				print ('[%s] %s : file already exists: %s' % (ts, user, fdir))
			else:
				os.makedirs(fdir)
			fpath = os.path.join(fdir, fn)
			if os.path.exists(fpath):
				print ('[%s] %s : file already exists: %s' % (ts, user, fpath))
			else:
				print ('[%s] %s : downloading %s to %s' % (ts, user, url_private_download, fpath))
				res = requests.get(url_private_download, stream=True, headers={'Authorization': 'Bearer %s' % token })
				with open(fpath,"wb") as fp:
					fp.write(res.content)

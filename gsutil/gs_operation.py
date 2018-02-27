import os

def gs_add(filename):
	os.chdir("C:/Users/NXie/PycharmProjects/flask_google_uploads")
	os.system("gsutil cp {} gs://neallab/dtp_upload/".format(filename))

def gs_rm(filename):
	os.system("gsutil rm gs://neallab/dtp_upload/{}".format(filename))
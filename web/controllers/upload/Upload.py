from flask import Blueprint,request,jsonify
from application import  app
from common.libs.UploadService import UploadService

route_upload = Blueprint('upload_page', __name__)
@route_upload.route("/pic",methods = [ "GET","POST" ])
def uploadPic():
	file_target = request.files
	upfile = file_target['pic'] if 'pic' in file_target else None
	callback_target = 'window.parent.upload'
	if upfile is None:
		return "<script type='text/javascript'>{0}.error('{1}')</script>".format( callback_target,"上传失败" )

	ret = UploadService.uploadByFile(upfile)
	if ret['code'] != 200:
		return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target, "上传失败：" + ret['msg'])

	return "<script type='text/javascript'>{0}.success('{1}')</script>".format(callback_target,ret['data']['file_key'] )
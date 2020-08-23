import json

from flask import request

from application import app
from common.libs.Helper import ops_render
from common.libs.LogService import LogService


@app.errorhandler(500)
def error_500(e):
    LogService.addErrorLog(e)
    return ops_render('error/error.html',{'status':500,'msg':'您访问的页面不存在'})

@app.errorhandler(404)
def error_404(e):
    return ops_render('error/error.html',{'status':404,'msg':'您访问的页面不存在'})
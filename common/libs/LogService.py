import json

from flask import request

from application import db
from common.libs.Helper import get_current_time
from common.models.AppErrorLog import AppErrorLog


class LogService():
    @staticmethod
    def addErrorLog(content):
        target = AppErrorLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time =get_current_time()
        db.session.add(target)
        db.session.commit()
        return True
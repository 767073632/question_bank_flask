from application import app, manager
from flask_script import Server


import www
# web server
from common.libs.UrlManager import UrlManager

manager.add_command("runserver",Server(host='0.0.0.0',port=app.config['SERVER_PORT'],use_debugger=True,use_reloader = True))
app.add_template_global(UrlManager.buildUrl,'buildUrl')
app.add_template_global(UrlManager.buildStaticUrl,'buildStaticUrl')
app.add_template_global(UrlManager.buildImageUrl,'buildImageUrl')

def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()

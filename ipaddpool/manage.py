import os
from Proxy.App.createapp import CreateApp
from flask_script import Manager
from Proxy.utils.database import init_db,drop_db
from Proxy.tools.todos import registtodos

app = CreateApp()
manage = Manager(app=app)
manage.add_command('init',init_db)
manage.add_command('drop',drop_db)

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        registtodos()
    manage.run()
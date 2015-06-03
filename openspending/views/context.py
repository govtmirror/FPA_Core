from flask import current_app, request
from flask.ext.login import current_user

from openspending import auth, _version
from openspending.views.home import blueprint as home
from openspending.lib.helpers import static_path
from openspending.lib.helpers import url_for



@home.after_app_request
def after_request(resp):
    resp.headers['Server'] = 'FIND/Beta'
    
    if resp.is_streamed:
        # http://wiki.nginx.org/X-accel#X-Accel-Buffering
        resp.headers['X-Accel-Buffering'] = 'no'
    
    return resp



def get_active_section():
    # TODO: use request.endpoint
    # ["blog", "dataset", "search", "resources", "help", "about"]
    return {'dataset': True}


@home.app_context_processor
def template_context_processor():
    data = {
        'DEBUG': current_app.config.get('DEBUG'),
        'static_path': static_path,
        'url_for': url_for,
        'section_active': get_active_section(),
        'logged_in': auth.account.logged_in(),
        'current_user': current_user
    }
    return data



def api_form_data():
    data = request.get_json(silent=True)
    if data is None:
        data = dict(request.form.items())
    return data

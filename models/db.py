from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
configuration = AppConfig(reload=True)

db = DAL(configuration.get('db.uri'))

auth = Auth(db, host_names=configuration.get('host.names'))
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

db.define_table('notebooks',
    Field('user_id', 'reference auth_user'),
    Field('title'),)

db.define_table('notes', 
    Field('notebook_id', 'reference notebooks'), 
    Field('title'),
    Field('body', 'text'))
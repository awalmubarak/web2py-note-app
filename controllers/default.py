@auth.requires_login()
def addNotebook():
    form = SQLFORM(db.notebooks)
    if form.process(session=None, formname='notebooks').accepted:
        response.flash = 'NoteBook added successfully'
        redirect(URL('showNotebooks'))
    else:           
        response.flash = 'An error occurred'
    return dict()

def showNotebooks():
    notebooks = db().select(db.notebooks.ALL, orderby=~db.notebooks.id)
    return dict(notebooks=notebooks)

def deleteNotebook():
    if db(db.notebooks.id == request.args(0)).delete():
        response.flash = 'Notebook Deleted Successfully'
    else:
        response.flash = 'An Error Occurred while deleting notebook'
    redirect(request.env.http_referer)

def addNote():
    notebookId = request.args(0, cast=int) or redirect(URL())
    form = SQLFORM(db.notes)
    if form.process(session=None, formname='note').accepted:
        response.flash = 'note added successfully'
        redirect(URL('showNotes', args=notebookId))
    else:
        response.flash = 'error occurred while adding note'
    return dict(form=form, notebookId=notebookId)

def showNotes():
    notebookId = request.args(0) or redirect(URL())
    notes = db(db.notes.notebook_id==notebookId).select(orderby=~db.notes.id)
    return dict(notes=notes, notebookId=notebookId)

def deleteNote():
    noteId = request.args(0) or redirect(URL())
    if db(db.notes.id == noteId).delete():
        response.flash = 'Note Deleted Successfully'
    else:
        response.flash = 'An Error Occurred while deleting note'
    redirect(request.env.http_referer)

def showNoteDetails():
    noteId = request.args(0) or redirect(URL())
    note = db.notes(noteId) or redirect(URL())
    return dict(note=note)

def updateNotebook():
    notebookId = request.args(0) or redirect(URL())
    notebook = db.notebooks(notebookId) or redirect(URL())
    form = SQLFORM(db.notebooks, notebookId)
    if form.process(session=None, formname='notebook_update').accepted:
        redirect(URL('showNotebooks'))
    return dict(notebook=notebook)

def updateNote():
    noteId = request.args(1) or redirect(URL())
    notebookId = request.args(0) or redirect(URL())
    note = db.notes(noteId) or redirect(URL())
    form = SQLFORM(db.notes, noteId)
    if form.process(session=None, formname='note').accepted:
        redirect(URL('showNotes', args=notebookId))
    else:
        response.flash = 'Error Occurred'

    return dict(note=note)

def seeUser():
    return dict(user=auth.user)








# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

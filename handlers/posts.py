import flask
from db import posts, users, helpers
import os
blueprint = flask.Blueprint("posts", __name__)
UPLOAD_FOLDER = 'static/uploads'
@blueprint.route('/post', methods=['POST'])
def post():
    db = helpers.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    post = flask.request.form.get("post")
    media = flask.request.files.get("media") 
    media_filename = None
    media_type = None
    print(media)
    print(post)

    if media and allowed_file(media.filename):
        file_extension = media.filename.rsplit('.', 1)[1].lower()
        media_filename = media.filename
        media.save(os.path.join(UPLOAD_FOLDER, media_filename))

        # Determine media type
        if file_extension in {'png', 'jpg', 'jpeg', 'gif'}:
            media_type = 'image'
        elif file_extension in {'mp4', 'mov', 'avi', 'webm'}:
            media_type = 'video'
        elif file_extension in {'mp3','wav','.ogg'}:
            media_type='audio'
    # Store in TinyDB
    media_url= f"/static/uploads/{media_filename}" if media_filename else None
    
    print(media_url)
    print(media_filename)
    print(media_type)
    posts.add_post(db, user, post, media_url ,media_type)
    return flask.redirect(flask.url_for('login.index'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'webm','mp3','wav','.ogg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
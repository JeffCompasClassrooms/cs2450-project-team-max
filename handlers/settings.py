import flask
from db import users, helpers

blueprint = flask.Blueprint("settings", __name__)

@blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    """Handles the settings page for updating user information and changing passwords."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is None or password is None:
        flask.flash('You must be logged in to access settings.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid session. Please log in again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    if flask.request.method == 'POST':
        action_type = flask.request.form.get('type')

        if action_type == 'Update Info':
            new_username = flask.request.form.get('username')
            new_email = flask.request.form.get('email')
            new_phone = flask.request.form.get('phone')

            if not new_username:
                flask.flash('Username is required.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

            if not new_email:
                flask.flash('Email is required.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

            if not new_phone:
                flask.flash('Phone number is required.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

            # Check if the username is changing and if new one is taken
            if new_username != user['username']:
                if users.get_user_by_name(db, new_username):
                    flask.flash('Username is already taken.', 'danger')
                    return flask.redirect(flask.url_for('settings.settings'))
                user['old_username'] = user['username']
                user['username'] = new_username
            else:
                user['old_username'] = user['username']  # fallback for update_user logic

            # Update fields
            user['email'] = new_email
            user['phone'] = new_phone

            users.update_user(db, user)

            response = flask.make_response(flask.redirect(flask.url_for('settings.settings')))
            response.set_cookie('username', user['username'])
            flask.flash('Account information updated successfully.', 'success')
            return response

        elif action_type == 'Change Password':
            current_password = flask.request.form.get('current_password')
            new_password = flask.request.form.get('new_password')
            confirm_password = flask.request.form.get('confirm_password')

            if not current_password or not new_password or not confirm_password:
                flask.flash('All password fields are required.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

            if current_password != user['password']:
                flask.flash('Current password is incorrect.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

            if new_password != confirm_password:
                flask.flash('New passwords do not match.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

            result = users.update_password(db, user['username'], new_password)
            if result:
                flask.flash('Password changed successfully.', 'success')
            else:
                flask.flash('Failed to update the password. Please try again.', 'danger')
            return flask.redirect(flask.url_for('settings.settings'))

        elif action_type == 'Delete Account':
            result = users.delete_user(db, user['username'])
            if result:
                flask.flash('Your account has been deleted.', 'success')
                response = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
                response.delete_cookie('username')
                response.delete_cookie('password')
                return response
            else:
                flask.flash('Failed to delete your account. Please try again.', 'danger')
                return flask.redirect(flask.url_for('settings.settings'))

    return flask.render_template('settings.html', title='Settings', user=user)
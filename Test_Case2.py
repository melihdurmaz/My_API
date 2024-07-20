import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request, session, url_for


SPOTIPY_CLIENT_ID = '****'
SPOTIPY_CLIENT_SECRET = '*****'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'



app = Flask(__name__)
app.secret_key = '171717'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Spotify OAuth Object
sp_oauth = SpotifyOAuth(
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    scope='user-follow-read'
)

# Routes
@app.route('/')
def index():
    if not session.get('token_info'):
        return redirect(url_for('login'))

    token_info = session.get('token_info')
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    session['token_info'] = token_info
    sp = spotipy.Spotify(auth=token_info['access_token'])

    #get mothodu ile kullanıcı id aldım
    users_id = request.args.get('users_id')

    if users_id:
        # Check if the user entered an artist ID
        following = sp.current_user_following_artists([users_id])
        return following

    else:

        return """
        <form action="/">
            <label for="users_id">kullanıcı id giriniz:</label>
            <input type="text" name="users_id" id="users_id" required>
            <input type="submit" value="kontorl et">
        </form>
        """

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)

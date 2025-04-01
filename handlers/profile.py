import Flask
from templates import profile

app = Flask.flask(__name__)

@app.route('/')
def home():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
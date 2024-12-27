from flask import Flask, request, render_template_string, redirect, url_for, session
import mss
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
messages = []

HTML_TEMPLATE = open('html.html').read()

@app.route('/', methods=['GET', 'POST'])
def index():
    screenshot_url = None
    is_done = False
    logged_in = session.get('logged_in', False)

    if request.method == 'POST' and logged_in:
        user_input = request.form['user_input']

        if user_input == "screenshot":
            screenshot_path = 'static/screenshot.png'
            with mss.mss() as sct:
                sct.shot(output=screenshot_path)
            screenshot_url = screenshot_path
            is_done = True

        if is_done:
            messages.insert(0, f"{user_input} - done")
        else:
            messages.insert(0, f"{user_input} - defected")

    return render_template_string(HTML_TEMPLATE, messages=messages, screenshot_url=screenshot_url, logged_in=logged_in)

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    if password == 'caZdut-sazheg-9duxju':
        session['logged_in'] = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')

    app.run(debug=True)


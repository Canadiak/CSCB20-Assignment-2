from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/assignments')
def assignments():
    return render_template('assignments.html')


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/course_team')
def course_team():
    return render_template('course_team.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/labs')
def labs():
    return render_template('labs.html')


@app.route('/lectures')
def lectures():
    return render_template('lectures.html')


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route('/tests')
def tests():
    return render_template('tests.html')


if __name__ == '__main__':
    app.run()

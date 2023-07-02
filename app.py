from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note %r>' % self.id


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
@app.route('/posts')
def posts():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template("posts.html", notes=notes)


@app.route('/posts/<int:id>')
def post_detail(id):
    note = Note.query.get(id)
    return render_template("post_detail.html", note=note)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    note = Note.query.get(id)
    if request.method == "POST":
        note.title = request.form['title']
        note.intro = request.form['intro']
        note.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error when updating"
    else:
        return render_template("post_update.html", note=note)


@app.route('/create-note', methods=['POST', 'GET'])
def create_note():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        note = Note(title=title, intro=intro, text=text)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error when adding"
    else:
        return render_template("create-note.html")


if __name__ == "__main__":
    app.run(debug=True)

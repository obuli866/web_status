from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'projects.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Project(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    developer = db.Column(db.String(100))
    complexity = db.Column(db.String(50))
    estimation = db.Column(db.String(50))
    analysis_progress = db.Column(db.Integer)
    development_progress = db.Column(db.Integer)
    testing_progress = db.Column(db.Integer)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    status = db.Column(db.String(50))

with app.app_context():
    db.create_all()

def parse_progress(value):
    try:
        v = int(value)
        return max(0, min(100, v))
    except ValueError:
        return 0

# Dashboard
@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Add Project
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        new_project = Project(
            id=request.form.get('id', '').strip(),
            name=request.form.get('name', '').strip(),
            developer=request.form.get('developer', '').strip(),
            complexity=request.form.get('complexity', '').strip(),
            estimation=request.form.get('estimation', '').strip(),
            analysis_progress=parse_progress(request.form.get('analysis_progress', 0)),
            development_progress=parse_progress(request.form.get('development_progress', 0)),
            testing_progress=parse_progress(request.form.get('testing_progress', 0)),
            start_date=request.form.get('start_date', '').strip(),
            end_date=request.form.get('end_date', '').strip(),
            status=request.form.get('status', '').strip()
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_project.html')

# Edit Project
@app.route('/edit/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return redirect(url_for('index'))

    if request.method == 'POST':
        project.name = request.form.get('name', '').strip()
        project.developer = request.form.get('developer', '').strip()
        project.complexity = request.form.get('complexity', '').strip()
        project.estimation = request.form.get('estimation', '').strip()
        project.analysis_progress = parse_progress(request.form.get('analysis_progress', 0))
        project.development_progress = parse_progress(request.form.get('development_progress', 0))
        project.testing_progress = parse_progress(request.form.get('testing_progress', 0))
        project.start_date = request.form.get('start_date', '').strip()
        project.end_date = request.form.get('end_date', '').strip()
        project.status = request.form.get('status', '').strip()
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_project.html', project=project)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

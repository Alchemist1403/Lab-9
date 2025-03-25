from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable = False)
    link = db.Column(db.String(400), unique = True, nullable = False)

    def to_dict(self):
        return {"id":self.id, "title":self.title, "link": self.link,}


# Создание базы данных
with app.app_context():
    db.create_all()


# Фронтенд
@app.route('/')
def index():
    return render_template('index.html')


# Список всех проектов
@app.route("/api/portfolio", methods=["GET"])
def get_projects():
    projects = Portfolio.query.all()
    return jsonify([project.to_dict() for project in projects])


# Добавление проекта
@app.route("/api/portfolio", methods=["POST"])
def add_project():
    data = request.get_json()
    new_project = Portfolio(title=data["title"], link=data["link"])
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201


# Удаление проекта
@app.route("/api/portfolio/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Portfolio.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return  jsonify({"message": "Запись о проекте удалена"})


if __name__ == '__main__':
    app.run(debug=True)

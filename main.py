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


# Вариант кода со сложным синтаксисом Java script (на основе материалов лекции)
# Допзадание не реализовано 

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


# Вариант кода с простым синтаксисом Java script (на основе кода в первоначальном main.py)
# Допзадание реализовано 

# Фронтенд + отображение всего списка
# @app.route('/')
# def index():
#     project = Portfolio.query.all()
#     return render_template('index.html', project_list=project)


# # Добавление проекта
# @app.route('/add', methods=['POST'])
# def add_project():
#     data = request.get_json()
#     title = data['title']
#     link = data['link']
#     project = Portfolio(title=title, link=link)
#     db.session.add(project)
#     db.session.commit()


# # Удаление всего списка
# @app.route("/clear", methods=["POST"])
# def clear_all():
#     db.session.query(Portfolio).delete()
#     db.session.commit()


if __name__ == '__main__':
    # Создание базы данных
    with app.app_context():
        db.create_all()
    app.run(debug=True)

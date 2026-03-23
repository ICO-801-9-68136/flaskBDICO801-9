from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from config import DevelopmentConfig
from models import db, Alumnos
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app, db)


@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_alumno = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_alumno, alumno=alumno)


@app.route("/Alumnos", methods=["GET", "POST"])
def alumnos():
    create_form = forms.UserForm(request.form)
    if request.method == "POST":
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            email=create_form.email.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("Alumnos.html", form=create_form)


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)
    id = request.args.get("id")

    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    if not alum1:
        return redirect(url_for("index"))

    if request.method == "GET":
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email

    if request.method == "POST":
        alum1.nombre = create_form.nombre.data
        alum1.apaterno = create_form.apaterno.data
        alum1.email = create_form.email.data
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("modificar.html", form=create_form)


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm(request.form)
    id = request.args.get("id")

    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    if not alum1:
        return redirect(url_for("index"))

    if request.method == "GET":
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email

    if request.method == "POST":
        db.session.delete(alum1)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("eliminar.html", form=create_form)


@app.route("/detalles", methods=["GET"])
def detalles():
    id = request.args.get("id")
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

    if not alum1:
        return redirect(url_for("index"))

    return render_template(
        "detalles.html",
        id=alum1.id,
        nombre=alum1.nombre,
        apaterno=alum1.apaterno,
        email=alum1.email
    )


if __name__ == "__main__":
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
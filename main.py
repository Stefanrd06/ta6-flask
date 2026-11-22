from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


# ---------------- Funciones ----------------

def calcular_promedio(nota1, nota2, nota3):
    return round((nota1 + nota2 + nota3) / 3, 1)


def obtener_estado(promedio, asistencia):
    if promedio >= 40 and asistencia >= 75:
        return "APROBADO"
    return "REPROBADO"


def nombre_mas_largo(nombres):
    mayor = nombres[0]
    for nombre in nombres:
        if len(nombre) > len(mayor):
            mayor = nombre
    return mayor


# ---------------- Rutas ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inicio")
def inicio():
    # Redirección a la página principal
    return redirect(url_for("index"))


@app.route("/ejercicio/<int:numero>")
def ejercicio(numero):
    # Ruta con parámetro por URL
    if numero == 1:
        return redirect(url_for("ejercicio1"))
    elif numero == 2:
        return redirect(url_for("ejercicio2"))
    abort(404)


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    promedio = None
    estado = None
    error = None

    if request.method == "POST":
        try:
            nota1 = float(request.form["nota1"])
            nota2 = float(request.form["nota2"])
            nota3 = float(request.form["nota3"])
            asistencia = float(request.form["asistencia"])
        except ValueError:
            error = "Debes ingresar solo números en todos los campos."
        else:
            notas = [nota1, nota2, nota3]
            if any(n < 10 or n > 70 for n in notas):
                error = "Las notas deben estar entre 10 y 70."
            elif asistencia < 0 or asistencia > 100:
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio = calcular_promedio(nota1, nota2, nota3)
                estado = obtener_estado(promedio, asistencia)

    return render_template("ejercicio1.html", promedio=promedio, estado=estado, error=error)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    nombre = None
    cantidad = None
    error = None

    if request.method == "POST":
        nombres = [
            request.form["nombre1"].strip(),
            request.form["nombre2"].strip(),
            request.form["nombre3"].strip(),
        ]
        if "" in nombres:
            error = "Debes ingresar los 3 nombres."
        else:
            nombre = nombre_mas_largo(nombres)
            cantidad = len(nombre)

    return render_template("ejercicio2.html", nombre=nombre, cantidad=cantidad, error=error)


@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

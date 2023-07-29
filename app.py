from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la conexión a la base de datos PostgreSQL
app.config['PG_HOST'] = 'dpg-cj084ptph6ek4q4ph2u0-a.oregon-postgres.render.com'
app.config['PG_PORT'] = 5432
app.config['PG_USER'] = 'tasklist_5ote_user'
app.config['PG_PASSWORD'] = 'VAAXhrGus7cRPlTO1wACCKPAzAMijTda'
app.config['PG_DATABASE'] = 'tasklist_5ote'

def connect_db():
    conn = psycopg2.connect(
        host=app.config['PG_HOST'],
        port=app.config['PG_PORT'],
        user=app.config['PG_USER'],
        password=app.config['PG_PASSWORD'],
        database=app.config['PG_DATABASE']
    )
    return conn

@app.route("/")
def Index():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY id")
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()

    return render_template("index.html", tasks=data)

@app.route("/add-task", methods=['POST'])
def add_task():
    task = request.form["nuevo_contenido"]
    state = "PENDING"

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task, State) VALUES (%s, %s)", (task, state))
    conn.commit()
    cur.close()
    conn.close()

    if task:
        return jsonify("The task was added successfully")
    else:
        return jsonify("Error 504")

@app.route("/change-state/<id>", methods=["POST"])
def change_state(id):
    if request.method == "POST":
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT State FROM tasks WHERE id = %s", (id,))
        actual_state = cur.fetchone()

        if actual_state is not None:
            actual_state = actual_state[0]

            if actual_state == "PENDING":
                actual_state = "DONE"
            elif actual_state == "DONE":
                actual_state = "PENDING"

            cur.execute("UPDATE tasks SET State = %s WHERE id = %s", (actual_state, id))
            conn.commit()
            cur.close()
            conn.close()

        return redirect(url_for("Index"))

@app.get("/get-content")
def content():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks  ORDER BY id")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=300, host="0.0.0.0")

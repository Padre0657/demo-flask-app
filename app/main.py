from flask import Blueprint, request, render_template_string
import psycopg2
import os

main_bp = Blueprint('main', __name__)

HTML = """
<!doctype html>
<title>Serveur Web Demo</title>
<h1>Recherche de personne</h1>
<form method="get">
  <input name="query" placeholder="Nom, prénom, fonction">
  <input type="submit" value="Rechercher">
</form>
{% if results %}
  <ul>
  {% for row in results %}
    <li>{{ row[1] }} {{ row[2] }} – {{ row[3] }}</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@main_bp.route("/", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    results = []
    if query:
        try:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                database=os.environ.get("DB_NAME", "persons"),
                user=os.environ.get("DB_USER", "user"),
                password=os.environ.get("DB_PASSWORD", "password")
            )
            cur = conn.cursor()
            sql = """
                SELECT * FROM people
                WHERE first_name ILIKE %s OR last_name ILIKE %s OR function ILIKE %s
            """
            q = f"%{query}%"
            cur.execute(sql, (q, q, q))
            results = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            results = [(0, "Erreur", str(e), "")]
    return render_template_string(HTML, results=results)

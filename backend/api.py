from flask import Flask, request, jsonify, g, send_from_directory
import sqlite3
import json
import os
from db import get_db, close_db

app = Flask(__name__, static_folder="frontend_build", static_url_path="")

# --------------------------
# API ROUTES
# --------------------------

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route("/api/cpes", methods=["GET"])
def get_cpes():
    db = get_db()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    total = db.execute("SELECT COUNT(*) FROM cpe").fetchone()[0]
    rows = db.execute("SELECT * FROM cpe ORDER BY id LIMIT ? OFFSET ?", (limit, offset)).fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row["id"],
            "cpe_title": row["cpe_title"],
            "cpe_22_uri": row["cpe_22_uri"],
            "cpe_23_uri": row["cpe_23_uri"],
            "reference_links": json.loads(row["reference_links"]),
            "cpe_22_deprecation_date": row["cpe_22_deprecation_date"],
            "cpe_23_deprecation_date": row["cpe_23_deprecation_date"],
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    })

@app.route("/api/cpes/search", methods=["GET"])
def search_cpes():
    db = get_db()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    query = "SELECT * FROM cpe WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM cpe WHERE 1=1"
    params = []
    count_params = []

    if title := request.args.get("cpe_title"):
        query += " AND LOWER(cpe_title) LIKE LOWER(?)"
        count_query += " AND LOWER(cpe_title) LIKE LOWER(?)"
        params.append(f"%{title}%")
        count_params.append(f"%{title}%")

    if uri22 := request.args.get("cpe_22_uri"):
        query += " AND LOWER(cpe_22_uri) LIKE LOWER(?)"
        count_query += " AND LOWER(cpe_22_uri) LIKE LOWER(?)"
        params.append(f"%{uri22}%")
        count_params.append(f"%{uri22}%")

    if uri23 := request.args.get("cpe_23_uri"):
        query += " AND LOWER(cpe_23_uri) LIKE LOWER(?)"
        count_query += " AND LOWER(cpe_23_uri) LIKE LOWER(?)"
        params.append(f"%{uri23}%")
        count_params.append(f"%{uri23}%")
    
    deprecation_before = request.args.get("deprecation_before")
    deprecation_after = request.args.get("deprecation_after")

    if deprecation_before:
        query += " AND (cpe_22_deprecation_date <= ? OR cpe_23_deprecation_date <= ?)"
        count_query += " AND (cpe_22_deprecation_date <= ? OR cpe_23_deprecation_date <= ?)"
        params.extend([deprecation_before, deprecation_before])
        count_params.extend([deprecation_before, deprecation_before])

    if deprecation_after:
        query += " AND (cpe_22_deprecation_date >= ? OR cpe_23_deprecation_date >= ?)"
        count_query += " AND (cpe_22_deprecation_date >= ? OR cpe_23_deprecation_date >= ?)"
        params.extend([deprecation_after, deprecation_after])
        count_params.extend([deprecation_after, deprecation_after])

    sort_by = request.args.get("sort_by", "id")
    allowed_sort_fields = ["id", "cpe_title", "cpe_22_deprecation_date", "cpe_23_deprecation_date"]
    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    sort_order = request.args.get("sort_order", "asc").lower()
    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    if sort_by in ["cpe_title", "cpe_22_uri", "cpe_23_uri"]:
        query += f" ORDER BY LOWER({sort_by}) {sort_order} LIMIT ? OFFSET ?"
    else:
        query += f" ORDER BY {sort_by} {sort_order} LIMIT ? OFFSET ?"

    # Add LIMIT and OFFSET for pagination
    params.extend([limit, offset])

    rows = db.execute(query, params).fetchall()
    total = db.execute(count_query, count_params).fetchone()[0]

    result = [{
        "id": row["id"],
        "cpe_title": row["cpe_title"],
        "cpe_22_uri": row["cpe_22_uri"],
        "cpe_23_uri": row["cpe_23_uri"],
        "reference_links": json.loads(row["reference_links"]),
        "cpe_22_deprecation_date": row["cpe_22_deprecation_date"],
        "cpe_23_deprecation_date": row["cpe_23_deprecation_date"]
    } for row in rows]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": result
    })


# --------------------------
# REACT UI ROUTING
# --------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# --------------------------
# Start Server
# --------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)

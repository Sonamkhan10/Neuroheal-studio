from flask import Flask, request, jsonify, send_from_directory, render_template_string
import json
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            name TEXT,
            email TEXT UNIQUE,
            organization TEXT,
            message TEXT,
            phone TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# Lead API
@app.route('/api/lead', methods=['POST'])
def lead():
    data = request.json
    email = data.get("email", "").strip().lower()

    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except:
        leads = []

    # Duplicate email check
    for lead in leads:
        if lead.get("email", "").strip().lower() == email:
            return jsonify({
                "ok": False,
                "error": "Email already exists!"
            })
    # Save new lead in JSON
    leads.append(data)

    with open('leads.json', 'w') as f:
        json.dump(leads, f, indent=2)

    # Save new lead in SQLite
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leads (type, name, email, organization, message, phone)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("type"),
        data.get("name"),
        data.get("email"),
        data.get("organization"),
        data.get("message"),
        data.get("phone")
    ))

    conn.commit()
    print("Saved to SQLite:", data.get("email"))
    conn.close()

    return jsonify({
        "ok": True,
        "message": "Successfully submitted!"
    })

# Ideas API
@app.route('/api/ideas', methods=['POST'])
def ideas():
    data = request.json
    product = data.get("product")

    ideas = [
        {"title": "Idea 1", "description": "Test idea"},
        {"title": "Idea 2", "description": "Test idea"},
        {"title": "Idea 3", "description": "Test idea"}
    ]

    return jsonify({"ok": True, "ideas": ideas})


# ADMIN PANEL
# ADMIN PANEL
@app.route('/neuroheal-control-x7k91')
def admin():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, name, email, organization, message, phone
    FROM leads
    """)

    rows = cursor.fetchall()
    conn.close()

    leads = []

    for row in rows:
        leads.append({
            "type": row[0],
            "name": row[1],
            "email": row[2],
            "organization": row[3],
            "message": row[4],
            "phone": row[5]
        })

    return render_template_string("""
    <h2>My Leads</h2>

    <table border="1" cellpadding="10">
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Type</th>
            <th>Organization</th>
            <th>Message</th>
            <th>Action</th>
        </tr>

        {% for l in leads %}
        <tr>
            <td>{{l.name}}</td>
            <td>{{l.email}}</td>
            <td>{{l.phone}}</td>
            <td>{{l.type}}</td>
            <td>{{l.organization}}</td>
            <td>{{l.message}}</td>

            <td>
                <button onclick="deleteLead('{{l.email}}')">Delete</button>
            </td>
        </tr>
        {% endfor %}
    </table>

<script>
function deleteLead(email) {
  fetch('/delete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: email })
  })
  .then(() => {
    alert("Deleted");
    location.reload();
  });
}
</script>

    """, leads=leads)

@app.route('/delete', methods=['POST'])
def delete():
    email = request.json.get("email")

    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM leads WHERE email = ?",
        (email,)
    )

    conn.commit()
    conn.close()

    return jsonify({"ok": True})
if __name__ == "__main__":
    app.run(debug=True)
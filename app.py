from flask import Flask, request, jsonify, send_from_directory, render_template_string
import json

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# Lead API
@app.route('/api/lead', methods=['POST'])
def lead():
    data = request.json

    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except:
        leads = []

    leads.append(data)

    with open('leads.json', 'w') as f:
        json.dump(leads, f, indent=2)

    return jsonify({
        "ok": True,
        "message": "Successfully submitted!"
    })
    # pehle purana data read karo
    try:
        with open('leads.json', 'r') as f:
            for line in f:
                leads.append(json.loads(line))
    except:
        pass

    # check duplicate email
    for l in leads:
        if l.get("email") == new_email:
            return jsonify({
                "ok": False,
                "error": "Email already exists!"
            })

    # agar duplicate nahi hai tab save karo
    with open('leads.json', 'a') as f:
        f.write(json.dumps(data) + "\n")

    return jsonify({
        "ok": True,
        "message": "You're successfully added!"
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
# ADMIN PANEL
@app.route('/neuroheal-control-x7k91')
def admin():
    leads = []

    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except:
        pass

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

    new_data = []

    try:
        with open('leads.json', 'r') as f:
            for line in f:
                item = json.loads(line)
                if item.get("email") != email:
                    new_data.append(item)
    except:
        pass

    with open('leads.json', 'w') as f:
        for item in new_data:
            f.write(json.dumps(item) + "\n")

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)

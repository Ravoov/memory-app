from flask import request, jsonify
from config import app, db
from models import Contact


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])

def create_contact():

    name = request.json.get("name")
    memory_score = request.json.get("memory_score")
    sleep_score = request.json.get("sleep_score")

    # ✅ Use explicit None checks instead of truthiness
    if not name or memory_score is None or sleep_score is None:
        return (
            jsonify({"message": "You must include a name and score"}),
            400,
        )

    new_contact = Contact(name=name, memory_score=memory_score, sleep_score=sleep_score)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    print("BODY:", request.json)
    return jsonify({"message": "User created!"}), 201
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.name = data.get("name", contact.name)
    contact.memory_score = data.get("memory_score", contact.memory_score)
    contact.sleep_score = data.get("sleep_score",contact.sleep_score)
    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
from flask import Blueprint, json, request, jsonify, render_template
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['webhookdata']

webhook_blueprint = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook_blueprint.route('/', methods=['GET'])
def webhook_data():
    # Query MongoDB for the latest webhook data
    latest_webhooks = list(db.webhooks.find().sort('_id', -1).limit(100))  # Limit to last 100 events

    # Pass the webhook data to the HTML template
    return render_template('webhook_data.html', webhooks=latest_webhooks)

@webhook_blueprint.route('/receiver', methods=["POST"])
def receiver():
    payload = request.json
    if 'action' in payload and payload['action'] in ['opened', 'closed']:
        action = payload['action']
        author = payload['sender']['login']
        pull_request = payload['pull_request']
        from_branch = pull_request['head']['ref']
        to_branch = pull_request['base']['ref']
        timestamp = pull_request['created_at']
        # Save the webhook event to MongoDB
        db.webhooks.insert_one({
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        })
    return jsonify({'message': 'Webhook received'}), 200


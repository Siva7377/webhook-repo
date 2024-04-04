from flask import Blueprint, json, request, jsonify, render_template
from pymongo import MongoClient

# Establish MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['my_webhook_data']

# Create a Blueprint for the webhook routes
my_webhook_blueprint = Blueprint('MyWebhook', __name__, url_prefix='/my_webhook')

@my_webhook_blueprint.route('/', methods=['GET'])
def show_webhook_data():
    latest_webhooks = list(mongo_db.webhooks.find().sort('_id', -1))
    return render_template('webhook.html', webhooks=latest_webhooks)


@my_webhook_blueprint.route('/receiver', methods=["POST"])
def receive_webhook():
    payload = request.json
    action = payload['action']
    if 'action' in payload:
        if action in ['opened', 'closed', 'reopened']:
            author = payload['sender']['login']
            pull_request = payload['pull_request']
            from_branch = pull_request['head']['ref']
            to_branch = pull_request['base']['ref']
            timestamp = pull_request['updated_at']

            mongo_db.webhooks.insert_one({
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            })
    return jsonify({'message': 'Webhook received'}), 200

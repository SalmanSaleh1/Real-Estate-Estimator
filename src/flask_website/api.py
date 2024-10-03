from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api', __name__)

# Define an API route that accepts parcel_no and block_no
@api_blueprint.route('/test', methods=['POST'])
def test_api():
    # Get JSON data from the request
    data = request.get_json()

    # Extract parcel_no and block_no from the request
    parcel_no = data.get('parcel_no')
    block_no = data.get('block_no')

    # Check if both parcel_no and block_no are provided
    if parcel_no is None or block_no is None:
        return jsonify({"error": "Both parcel_no and block_no are required!"}), 400

    # Try to add 2 to both values, even if they are not integers
    try:
        # Convert to integers if possible, else use 0 for non-integer inputs
        parcel_no = int(parcel_no) + 2 if parcel_no.isdigit() else "Invalid input"
        block_no = int(block_no) + 2 if block_no.isdigit() else "Invalid input"

        return jsonify({
            "message": "Success",
            "parcel_no": parcel_no,
            "block_no": block_no
        })

    except Exception as e:
        # Catch any unexpected errors and return a generic error
        return jsonify({"error": f"Error processing input: {e}"}), 400

"""Flask application for Greek verb conjugation API."""

from flask import Flask, request, jsonify

from app.chains import process_conjugation


def create_app():
    """Application factory for Flask app."""
    app = Flask(__name__)

    @app.route('/conjugate', methods=['POST'])
    def conjugate():
        """
        Conjugate an English verb to Modern Greek present tense.

        Request JSON:
            {
                "verb": "to write"
            }

        Returns:
            JSON with validated conjugations from judge LLM
        """
        # Validate request JSON
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        if not data or 'verb' not in data:
            return jsonify({"error": "Missing required field: verb"}), 400

        verb = data['verb']

        if not isinstance(verb, str) or not verb.strip():
            return jsonify({"error": "verb must be a non-empty string"}), 400

        # Process through generator and judge chains
        try:
            result = process_conjugation(verb)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

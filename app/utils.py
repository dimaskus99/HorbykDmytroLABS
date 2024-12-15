from flask import jsonify

def handle_error(err, status_code=500):
    response = {
        "error": str(err),
        "status_code": status_code
    }
    return jsonify(response), status_code

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(err):
        return handle_error("Bad request: " + str(err), status_code=400)

    @app.errorhandler(404)
    def not_found_error(err):
        return handle_error("Not found: " + str(err), status_code=404)

    @app.errorhandler(500)
    def internal_server_error(err):
        return handle_error("Internal server error: " + str(err), status_code=500)

    @app.errorhandler(Exception)
    def global_exception_handler(err):
        return handle_error("An unexpected error occurred: " + str(err), status_code=500)
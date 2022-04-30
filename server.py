from flask import redirect
from flask_app import app
from flask_app.controllers import user_controller, routes, event_controller, news_controller
if __name__ == "__main__":
    app.run(debug=True)
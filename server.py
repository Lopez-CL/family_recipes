from flask_app import app
from flask_app.controllers import recipes, users #import all controllers, don't forget!

if __name__== "__main__":
    app.run(debug=True)

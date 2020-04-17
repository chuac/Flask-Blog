from flaskblog import create_app # create_app function from __init__py
from flaskblog.config import Config


app = create_app(Config)

if __name__ == "__main__":
    app.run(debug=True)

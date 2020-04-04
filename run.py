from flaskblog import app # the app variable MUST exist in __init__.py inside flaskblog package

if __name__ == "__main__":
    app.run(debug=True)

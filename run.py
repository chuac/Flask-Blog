from flaskblog import create_app # create_app function from __init__py


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

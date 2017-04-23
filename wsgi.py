from main import app

# Simply import and start the app
# This becomes gunicorn's application entrypoint

if __name__ == "__main__":
    # use the arg [ debug=True ] to run in debug mode
    # NOTE: do NOT use [ debug=True ] in production
    app.run(debug=True)

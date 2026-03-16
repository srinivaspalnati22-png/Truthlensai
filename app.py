from project.backend.app import app

# This allows 'gunicorn app:app' to work from the root directory
if __name__ == "__main__":
    app.run()

from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Ambil nilai FLASK_ENV, default-nya adalah 'development' jika tidak di-set
    flask_env = os.getenv("FLASK_ENV", "development")
    is_debug = flask_env == "development"
    
    app.run(debug=is_debug, host="127.0.0.1", port=int(os.getenv("PORT", 5000)))

import os
from app import create_app,db

app=create_app()

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))  # Use Render's port, fallback to 5000 locally
    app.run(host="0.0.0.0", port=port, debug=True)
import os
from routes import main
from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.register_blueprint(main)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

# 👇 Required fix for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(host='0.0.0.0', port=port)

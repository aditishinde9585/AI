# app.py
from main import app

if __name__ == "__main__":
    app.run(debug=True)

    if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(host='0.0.0.0', port=port)
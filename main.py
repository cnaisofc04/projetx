from app import app

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Application</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }
            h1 { color: #333; }
            .status { 
                background: #e8f5e9; 
                padding: 20px; 
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <h1>🚀 Flask Application Ready</h1>
        <div class="status">
            <p>Your modular, secure infrastructure is being set up.</p>
            <p>All API integrations are ready to be configured.</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

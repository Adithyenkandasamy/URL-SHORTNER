from url_shortener import create_app

app=create_app()

app.run(debug=True,host="0.0.0.0",port=5000)

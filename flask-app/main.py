from website import create_app, db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) #incase we ake any changes in the app, it is edited directly


#run the server if you run this file directly
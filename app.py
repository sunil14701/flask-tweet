# entry point of our application


from website import create_app # when i import the folder name than everything inside __init__.py runs


# running a flask webserver
if __name__ == "__main__":# this means that this file is not imported . it is the first file to be executed
    app = create_app()
    app.run(debug=True,port=5000)# debug=True -> means when ever you change your python code it will automatically   re-run the flask web server


from website import create_app # calling the __init__.py create_app() method 
app=create_app()
if __name__=='__main__': #only if we run this file (main.py) the app will start running
    app.run(debug=True)# starts running an application and starts a web server 

#basically this file is like an entry point for my application




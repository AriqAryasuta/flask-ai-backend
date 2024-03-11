from flask import Flask

def create_app():
    app = Flask(__name__)
    # app.register_blueprint(main_bp)

    # Collection of Blueprint over here
    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    # from app.chat import bp as chat_bp
    

    @app.route('/')
    def testing():
        return 'Hello, Test!'
    
    return app
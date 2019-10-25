from app import app, db
from app.models import User, Post, Game, Decision1, Decision2, Result1

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Game':Game, 'Decision1':Decision1, 'Decision2':Decision2, 'Result1':Result1}
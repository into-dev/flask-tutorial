from flaskr.models import Post, User


def test_init_database_command(runner, monkeypatch):
    class Recorder:
        called = False
    
    def fake_init_database():
        Recorder.called = True
    
    monkeypatch.setattr('flaskr.database.init_database', fake_init_database)
    result = runner.invoke(args=['init-database'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_user(app):
    with app.app_context():
        user = User.query.filter(User.id == 1).first()
        assert repr(user) == "<User test>"


def test_post(app):
    with app.app_context():
        post = Post.query.filter(Post.id == 1).first()
        assert repr(post) == "<Post test title>"

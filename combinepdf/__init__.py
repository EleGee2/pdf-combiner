from flask import Flask
from .views import bp
from .extensions import c


def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_CONFIG={
            'broker_url': 'redis://redis',
            'result_backend': 'redis://redis',
            'task_ignore_result': True,
        }
    )

    c.init_app(app)
    app.register_blueprint(bp)

    return app, c.celery
    # app.config.from_prefixed_env()
    # celery_init_app(app)

    # @app.route('/')
    # def index():
    #     return render_template('home.html')
    #
    # app.register_blueprint(views.bp)
    # return app

# class FlaskTask:
#     def __init__(self, *args, **kwargs):
#         self.app = kwargs.pop('app', None)
#         super().__init__(*args, **kwargs)
#
#     def __call__(self, *args: object, **kwargs: object) -> object:
#         with self.app.app_context():
#             return self.run(*args, **kwargs)
#
#
# def celery_init_app(app: Flask) -> Celery:
#     celery_app = Celery(
#         app.import_name,
#         broker=app.config["CELERY"]["broker_url"],
#         backend=app.config["CELERY"]["result_backend"],
#         task_ignore_result=True,
#     )
#     celery_app.task_cls = FlaskTask
#     celery_app.set_default()
#     app.extensions["celery"] = celery_app
#     return celery_app

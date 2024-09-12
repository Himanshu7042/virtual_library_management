from models import *
from flask_restful import Api
from flask import Flask,jsonify
import os
from flask_cors import CORS
from auth import userLogin, adminLogin, userSignup
from admin import adminSections, adminBook, adminInfo, adminEmail
from user import allBook, userInfo, requestBook, userEmail, canRequest
from search import searchBook 
from user_stat import barData,pieData
from books_issued import issuedBook
from flask_jwt_extended import JWTManager
# from flask_mail import Mail, Message
# from flask_caching import Cache
import redis

from workers import celery_init_app
from celery.schedules import crontab
from tasks import daily_reminder, monthly_report
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)


    return app



app = create_app()
celery_app = celery_init_app(app)
CORS(app)

app.app_context().push()
jwt = JWTManager(app)


api = Api(app)
api.add_resource(adminLogin,'/admin/login')
api.add_resource(userLogin,'/user/login')
api.add_resource(userSignup,'/user/signup')
api.add_resource(adminSections, '/admin/sections','/admin/section/<string:oldname>')
api.add_resource(adminBook, '/admin/book/<string:isbn>','/admin/book')
api.add_resource(adminInfo, '/admin/info')
api.add_resource(userInfo, '/user/info')
api.add_resource(allBook, '/all/book')
api.add_resource(requestBook, '/request/book')
api.add_resource(issuedBook, '/book/issued', '/book/<int:id>/return','/book/<int:id>/delete')
api.add_resource(userEmail, '/user/email')
api.add_resource(adminEmail, '/admin/email')
api.add_resource(searchBook, '/search/book')
api.add_resource(pieData, '/pie')
api.add_resource(barData,'/bar')
api.add_resource(canRequest, '/check')
api.init_app(app)
file_path = os.path.join(os.getcwd(), 'instance', 'database.sqlite3')

if not os.path.exists(file_path):
    with app.app_context():
        db.create_all()
        try:
            admin_user = User(username='Admin', password='1234', admin=True)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user added successfully")
        except Exception as e:
            db.session.rollback()  # Rollback changes if an error occurs
            print(f"Error adding admin user: {str(e)}")
        finally:
            print("print something")


admin = (User.query.filter_by(admin = 1).first()).email

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=51, day_of_month="*"),
        daily_reminder.s(admin, 'Daily Test'),
    )

    sender.add_periodic_task(
        crontab(hour=8, minute=51, day_of_month="17"),
        monthly_report.s(admin, 'Daily Test'),
    )

if __name__ == '__main__':
    app.run(debug=True)
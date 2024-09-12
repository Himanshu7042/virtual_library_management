
from celery import shared_task
# from .models import StudyResource
# import flask_excel as excel
from mail_service import send_message
# from .models import User, Role
from jinja2 import Template
from models import User, Book, Book_issue,db
from sqlalchemy import func


@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.filter_by(admin = 0).all()
    admin = User.query.filter_by(admin = 1).first()

    for user in users:
        with open('daily.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,
                            template.render(username=user.username, adminname=admin.username))
    return "OK"

from models import Book_issue
@shared_task(ignore_result=True)
def monthly_report(to, subject):
    users = User.query.filter_by(admin=0).all()
    
    for user in users:
        section_counts = db.session.query(Book.section, func.count(Book_issue.isbn)).join(Book_issue, Book_issue.isbn == Book.isbn).filter(Book_issue.username == user.username).group_by(Book.section).all()
        isbn_counts = db.session.query(Book.name, func.count(Book_issue.isbn)).join(Book_issue, Book_issue.isbn == Book.isbn).filter(Book_issue.username == user.username).group_by(Book.name).all()
        section_counts_dict = [{'label': section, 'value': count} for section, count in section_counts]
        isbn_counts_dict = [{'label': name, 'value': count} for name, count in isbn_counts]

        report_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Report</title>
                <!-- Include Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
                <div class="section-container">
                    <h1>Monthly Report for {user.username}</h1>
                    <h4>Analyse Your Literary Journey: Discover Your History Through Category of Books</h4>
                    <table class="table table-striped table-bordered">
                        <thead class="thead-dark">
                            <tr>
                                <th>Section Name</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        for section_count in section_counts_dict:
            report_html += f"""
                <tr>
                    <td>{section_count['label']}</td>
                    <td>{section_count['value']}</td>
                </tr>
            """

        report_html += """
                        </tbody>
                    </table>
                </div>
            """

        report_html += """
                <div class="book-container">
                    <h4>Explore Your Literary Journey: Discover Your History Through Books</h4>
                    <table class="table table-striped table-bordered">
                        <thead class="thead-dark">
                            <tr>
                                <th>Book Name</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        for isbn_count in isbn_counts_dict:
            report_html += f"""
                <tr>
                    <td>{isbn_count['label']}</td>
                    <td>{isbn_count['value']}</td>
                </tr>
            """

        report_html += """
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
        """

        send_message(user.email, subject, report_html)





from flask import Flask, render_template, flash, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import re
import os

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'default123')


# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
if not app.config['MAIL_USERNAME']:
    raise ValueError("MAIL_USERNAME environment variable is not set")


app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
if not app.config['MAIL_PASSWORD']:
    raise ValueError("MAIL_PASSWORD environment variable is not set")


# Initializing Flask-Mail
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    errors = []
    message = None

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_content = request.form.get('message')

        if not name or not email or not subject or not message_content:
            errors.append("All fields are requiered. ")

        if name and not re.match(r"^[A-Za-z\s]+$", name):
            errors.append("Name should only contain letters and spaces. ")

        if email and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            errors.append("Please enter a valid email address. ")

        if subject and (len(subject) < 5 or len(subject) > 100):
            errors.append("Subject must be between 5 and 100 characters. ")

        
        if message_content and (len(message_content) < 10 or len(message_content) > 500):
            errors.append("Message must be between 10 and 500 characters. ")

        if errors:
            flash("".join(errors), 'danger')
            return render_template('contact.html', errors=errors)
        
        try:
            msg = Message(
                subject = f"New Contact Form Submission: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients = ['laraibansari1214@gmail.com'],
                body = f"Name: {name}\nEmail: {email}\n\nSubject: {subject}\n\n\nMessage: {message_content}",
                reply_to = email
            )
            mail.send(msg)
            flash("Thank you for your message! I'll get back to you soon.", 'success')
            return render_template('contact.html')
        except Exception as e:
            flash("Oh ohh! Failed to send message. Please try again later.", 'danger')
            print("MAIL ERROR: ", str(e))
            return render_template('contact.html')
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
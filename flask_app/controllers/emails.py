from flask import render_template, request, redirect, url_for
from flask_app.models.email import Email
from flask_app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not Email.validate_email(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # ... do other things
    return redirect(url_for('result', email_id = Email.add(request.form)))

@app.route('/success/<int:email_id>')
def result(email_id):
    # calling the get_one method and supplying it with the id of the email we want to get
    email = Email.show_one(email_id)
    # call the get all classmethod to get all emails
    emails = Email.get_all()
    print(emails)
    # passing one email to our template so we can display them
    return render_template("success.html", one_email = email, all_emails = emails )

# DELETE
@app.route('/success/<int:email_id>/delete')
def delete_email(email_id):
    Email.delete(email_id)
    return redirect(url_for('result', email_id = email_id))
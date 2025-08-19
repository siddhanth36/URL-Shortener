from flask import Flask, render_template, request, redirect, url_for, flash
import database

# Initialize the Flask application and database
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
database.init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with the form to shorten a URL."""
    short_url = None
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_code = request.form['custom_code'].strip() or None

        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url

        try:
            short_code = database.add_url(original_url, custom_code)
            short_url = f"{request.host_url}{short_code}"
        except Exception as e:
            flash("Error creating short URL. The custom code might be taken. Try another one.", 'error')

    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    """Redirects the short code to the original URL."""
    original_url = database.get_original_url(short_code)
    if original_url:
        return redirect(original_url)
    else:
        flash("Short URL not found!", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

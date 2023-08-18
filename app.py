from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'product')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/home')
def home():
    user_agent = request.headers.get('User-Agent')
    # return '<h1 style="color: red">Hello From Flask</h1>'
    product_list = [
        {
            'name': 'COCA COLA',
            'category': 'drink',
            'price': '0.5 $',
            'old_price': '1 $',
            'discount': '25 %',
            'total_sold': '1000',
            'image': 'coca.jpeg',
        },
        {
            'name': 'Sting Red',
            'category': 'drink',
            'old_price': '1 $',
            'price': '0.5 $',
            'discount': '50 %',
            'total_sold': '1000',
            'image': 'sting_red.jpeg',
        },
        {
            'name': 'Sting Yellow',
            'category': 'drink',
            'old_price': '1 $',
            'price': '0.5 $',
            'discount': '2 %',
            'total_sold': '1000',
            'image': 'string_yellow.jpeg',
        }
    ]
    for count in range(50):
        product_list.append(
            {
                'name': 'COCA COLA',
                'category': 'drink',
                'price': '0.5 $',
                'old_price': '1 $',
                'discount': '25 %',
                'total_sold': '1000',
                'image': 'coca.jpeg',
            }
        )
    return render_template('index.html', product_list=product_list)


@app.route('/product_detail')
def product_details():
    return render_template('detail.html')


@app.route('/add_product_index')
def add_product_index():
    return render_template('add_product.html')


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    category = request.form.get('category')
    filename = None
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Process form data and file as needed

    # Process the form data, e.g., save it to a database
    return f"<p>name:{name}</p>" \
           f"<p>price:{price}</p>" \
           f"<p>category:{category}</p>" \
           f"<p>filename:{filename}</p>"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # return render_template('500.html'), 500
    return '500.html', 500


if __name__ == '__main__':
    app.run()

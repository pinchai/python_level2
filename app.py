from flask import Flask, request, render_template, Response, url_for
from werkzeug.utils import secure_filename
import os
import pdfkit
import xlsxwriter
import requests
from datetime import datetime


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'product')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/pdf")
def index_pdf():
    path = os.getcwd() + '/pdf/invoice.pdf'
    if not os.path.exists(path):
        os.makedirs(os.getcwd() + '/pdf')

    data = [
        {'id': 1, 'name': 'កូកាកូឡា', 'qty': 20, 'price': 0.25},
        {'id': 1, 'name': 'sting', 'qty': 10, 'price': 0.25},
        {'id': 1, 'name': 'abc', 'qty': 3, 'price': 25},
    ]
    now = datetime.now()
    created_at = now.strftime("%Y-%m-%d %H:%M")
    server_url = request.url_root
    html = render_template("invoice.html", data=data, now=created_at, server_url=server_url)
    options = {
        # 'page-size': 'a7',
        'page-height': '7in',
        'page-width': '3in',
        'margin-top': '0.1in',
        'margin-right': '0in',
        'margin-bottom': '0.1in',
        'margin-left': '0in',
    }
    pdf = pdfkit.from_string(html, path, options)
    pdf_preview = pdfkit.from_string(html, '', options)

    return Response(pdf_preview, mimetype="application/pdf")


@app.route('/excel')
def excel():
    # Cretae a xlsx file
    xlsxFile = xlsxwriter.Workbook('demo.xlsx')

    # Add new worksheet
    sheetOne = xlsxFile.add_worksheet("SheetOne")

    # Create List for write data into xlsx file
    data = [
        {"ID": 1, "Name": "ពិនឆៃ", "Email": "chai@gmail.com"},
        {"ID": 2, "Name": "ធារ៉ា", "Email": "theara@gmail.com"},
        {"ID": 3, "Name": "ពិសី", "Email": "pisey@gmail.com"}
    ]

    row = 1
    column = 0

    # Set Header for xlsx file(SheetONE)
    sheetOne.write(0, 0, "ល.រ")
    sheetOne.write(0, 1, "ឈ្មោះ")
    sheetOne.write(0, 2, "Email")

    # write into the worksheet
    for item in data:
        # write operation perform(SheetOne)
        sheetOne.write(row, 0, item["ID"])
        sheetOne.write(row, 1, item["Name"])
        sheetOne.write(row, 2, item["Email"])

        # incrementing the value of row by one
        row += 1

    # Close the Excel file
    xlsxFile.close()


@app.route('/')
@app.route('/home')
def home():
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
    for count in range(7):
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


@app.route('/product_detail/<float:price>')
def product_details(price):

    # name = request.args.get("name", default="all", type=str)
    # price = request.args.get("price", default=0, type=float)

    return render_template('detail.html', price=price)


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


@app.route('/template')
def template():
    name = "SS3.4"
    return render_template('jinja.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # t = threading.Thread(target=start_server)
    # t.daemon = True
    # t.start()
    #
    # webview.create_window("mini POS", "http://127.0.0.1:5050/pdf")
    # webview.start()
    # sys.exit()

    app.run()

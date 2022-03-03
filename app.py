import os
from datetime import datetime, timezone
from dateutil import parser

import yaml
from flask import Flask, render_template, request, abort, send_file

from slugify import slugify
from utils.csv_tools import create_or_append
from utils.qr import create_qr
from utils import strike

app = Flask(__name__)



def get_items(items_path='inventory.yaml'):
    """
    Get items from yaml file
    """

    items = []
    if os.path.exists(items_path):
        with open(items_path) as f:
            items = yaml.safe_load(f.read())

    # add item slugs
    for item in items:
        item['slug'] = slugify(item['name'])

    return items


@app.route("/")
def home():
    """
    Render and return templates/home.html
    """

    # Get list of items
    items = get_items()

    return render_template('home.html', items=items)


@app.route("/product/<slug_name>")
def product(slug_name):
    """
    Render and return templates/product.html
    """

    # Get list of items
    items = get_items()

    for item in items:
        if item['slug'] == slug_name:
            return render_template('product.html', item=item)

    return abort(404)


@app.route("/receipt/<invoice_id>")
def receipt(invoice_id):
    """
    Render and return templates/receipt.html only if invoice is paid
    """

    # Get list of items
    # TODO add func
    items = []
    items_path = 'inventory.yaml'
    if os.path.exists(items_path):
        with open(items_path) as f:
            items = yaml.safe_load(f.read())

    invoice = strike.get_invoice(invoice_id)

    if invoice['state'] == 'PAID':

        # only show receipts for 24 hours
        created = parser.parse(invoice['created'])
        delta = datetime.utcnow().replace(tzinfo=timezone.utc) - created

        if delta.days <= 1:

            # get origin item using description...
            # yuck, but no database, so it will do
            for item in items:
                if item['name'] == invoice['description']:

                    return render_template(
                        'receipt.html', invoice_id=invoice_id)

    # return not found
    return abort(404)


@app.route("/download/<invoice_id>")
def download(invoice_id):
    """
    Pass file to user if their invoice is valid
    """

    # Get list of items
    # TODO add func
    items = []
    items_path = 'inventory.yaml'
    if os.path.exists(items_path):
        with open(items_path) as f:
            items = yaml.safe_load(f.read())

    invoice = strike.get_invoice(invoice_id)

    if invoice['state'] == 'PAID':

        # only show receipts for 24 hours
        created = parser.parse(invoice['created'])
        delta = datetime.utcnow().replace(tzinfo=timezone.utc) - created

        if delta.days <= 1:

            # get origin item using description...
            # yuck, but no database, so it will do
            for item in items:
                if item['name'] == invoice['description']:

                    content_path = 'content/%s' % item['content']

                    return send_file(content_path)

    # return not found
    return abort(404)



@app.route("/about")
def about():
    """
    Render and return templates/about.html
    """

    return render_template('about.html')


@app.route("/invoice/", methods=['POST'])
def create_invoice():
    """
    Create strike invoice
    """

    description = request.form['description']
    price = request.form['price']

    invoice = strike.create_invoice(description, price)

    create_or_append(
        invoice['created'], invoice['invoice_id'], invoice['description'],
        invoice['amount'], 'CREATED'
    )

    return invoice


@app.route("/ln_invoice/", methods=['POST'])
def create_ln_invoice():
    """
    Create strike lightning quote
    """

    invoice_id = request.form['invoice_id']

    ln_invoice = strike.create_ln_invoice(invoice_id)

    # encode as qrcode
    ln_invoice['ln_invoice_qr'] = create_qr(ln_invoice['ln_invoice'])

    return ln_invoice


@app.route("/invoice/<invoice_id>")
def get_invoice(invoice_id):
    """
    Get strike invoice
    """

    invoice = strike.get_invoice(invoice_id)

    if invoice['state'] == 'PAID':
        create_or_append(
            invoice['created'], invoice['invoice_id'], invoice['description'],
            invoice['amount'], invoice['state']
        )

    return invoice


app.run(host='0.0.0.0', port='8080', debug=False)

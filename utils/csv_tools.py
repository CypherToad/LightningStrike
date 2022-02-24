import os

import csv


FILENAME = "sales.csv"
FIELDS = ['created', 'invoice_id', 'description', 'price', 'state']


def create():
    """
    Create the sales.csv
    """

    with open(FILENAME, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(FIELDS)


def append(created, invoice_id, description, price, state):
    """
    Append to the the sales.csv
    """

    with open(FILENAME, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([created, invoice_id, description, price, state])


def create_or_append(created, invoice_id, description, price, state):
    """
    Create or append to our sales.csv
    """

    if not os.path.exists('sales.csv'):
        create()

    append(created, invoice_id, description, price, state)

# **LightningStrike ⚡**

The zero config, self-managed, bitcoin lightning marketplace.

Take back ownership of your market!

  * [BTC Lightning payment](https://lightning.network/)
  * [Strike API integration](https://developer.strike.me/en/)
  * [Tor routed .onion hostname](https://www.torproject.org/)

![1_home.png](/screenshoots/1_home.png)

![2_home.png](/screenshoots/2_pay_with_lightning.png)

![3_home.png](/screenshoots/3_wait_for_payment.png)

![4_home.png](/screenshoots/4_thankyou.png)

## Demo

I'll do my best to keep a demo available at: https://bit.ly/3In25QK

## Startup

Requires [Docker](https://www.docker.com/get-started)

```
$ export ENABLE_TOR=true  # optional
$ export TOKEN="YOUR STRIKE API TOKEN"
$ docker-compose up
```

If you don't yet have a strike api token, you can still explore the platform;
merely unset your $TOKEN variable before run:

```
$ unset TOKEN
$ docker-compose up
```

Now, when you press the "pay with lightning" button, we will respond with mock data (id is all 0s).

You should be able to access http://127.0.0.1:8080


## Inventory

The **inventory.yaml** file is the heart of your marketplace.

The structure of this file should be simple enough for any user to manage,
check out [YAML](https://yaml.org/) if you need more detail.

### Images (thumbnails)

Our inventory file contains a **key** called `images` for each product:

*inventory.yaml*
```
- name: Pancakes
  description: More like tasty cakes
  price: 0.05
  image: pancakes.jpeg
  content: pancakes.jpeg
```

These images are hosted within the `static/images/` folder; for example,
**pancakes.jpeg** can be found at `static/images/pancakes.jpeg`


### Content

Our inventory file also has a **key** called `content` for each product,
as expected, these live in `content/` and are only accessible through a valid
receipt page.

A receipt page is only valid when the following are true:

  1. invoice's state is **PAID**
  2. invoice created less than **24 hours** ago.


## Banner

The banner can be changed by replacing `static/images/banner.jpeg` with your own.

## Templates

The look and feel of your application lives within your templates, more
accurately, your `templates/` folder. You have the ability to change any
aspect of your marketplace and the full power of the
[Jinja2](https://jinja2docs.readthedocs.io/en/stable/templates.html) template
renderer.


## Sales

Without adding much complexity, or more compute resources in the form of
database servers, I decided to go with simple comma-separated values file.

As **invoices** are created, and as invoice are **paid** your `sales.csv` will grow.

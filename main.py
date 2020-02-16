""" ustjay-ethay-actsfyig script """

# imports
import os
import requests
from flask import Flask, Response
from bs4 import BeautifulSoup
# ==========================================

APP = Flask(__name__)
# ------------------------------------------

# APP.secret_key = b"\xe0\x95\xf2`W8'X,2\xfc\x88Z\x8c\x97\xad~1\xd8k\xbb\xaf\xd7\xab"
# APP.secret_key = os.environ.get('SECRET_KEY').encode()
# ------------------------------------------

PARSER = "html.parser"

def get_fact():
    """ get unknown facts """
    url = "http://unkno.com"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, PARSER)
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()
# ------------------------------------------

def get_pig(fact):
    """ get pig """
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    payload = {'input_text': fact}
    response = requests.post(url, data=payload)

    soup = BeautifulSoup(response.text, PARSER)
    pig_fact = [line.strip() for line
                in soup.get_text().strip().splitlines()][-1]

    pig_url = response.request.url
    return (pig_url, pig_fact)
# ------------------------------------------

@APP.route('/')
def home():
    """ app """
    fact = get_fact()
    body = get_pig(fact)

    page = """
    <b> {0} </b>
    <hr></hr>
    <ul style="list-style-type:circle;">
        <li>Unknown fact:  <i>{1}</i> </li>
        <li>Pig-Latinized fact:  <i>{2}<i></li>
    </ul>
    <hr></hr>
    """.format(body[0], fact, body[1])

    return Response(response=page, mimetype="text/html")


# ==========================================
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=PORT)
    # APP.run(debug=True)
    
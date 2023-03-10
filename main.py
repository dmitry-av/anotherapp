from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def index():
    url_list = request.args.get("url_list", "")
    if url_list:
        resultlist = []
        if len(url_list.split(",")) > 10:
            resultlist = "Maximum 10 URLS"
        else:
            for url in url_list.split(","):
                resultlist.append(find_price(url))
    else:
        resultlist = ""
    return (
        """<h1>Check prices on Udemy courses</h1>
            <form action="" method="get">
                Type your URLs separated by <b>comma</b>: <input type="text" name="url_list">
                <input type="submit" value="Check for prices">
            </form>"""
        + "Result: "
        + '   '.join(resultlist)
    )


def find_price(url):
    try:
        page = requests.get(url.strip()).content
        soup = BeautifulSoup(page, 'lxml')
        course_id = soup.body.attrs['data-clp-course-id']
        link = f'https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=title,headline'
        res = requests.get(link).json()
        title = res['title']
        link = f'https://www.udemy.com/api-2.0/pricing/?course_ids={course_id}&fields[pricing_result]=price,discount_price,list_price'
        res = requests.get(link).json()
        price = res['courses'][course_id]['price']['price_string']
        return f"<p>{title} course, price - {price}</p>"
    except:
        return "<p>Error. Check if Udemy URL entered correctly</p>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

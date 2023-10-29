import tornado.ioloop
import tornado.web

def get_pricing_suggestion(price_history, competitor_price, max_increase_percent=20):
    avg_price = price_history
    max_price = avg_price * (1 + max_increase_percent / 100)
    if competitor_price < max_price:
        price_difference = avg_price - competitor_price
        pricing_suggestion = min(avg_price + price_difference, max_price)
        return round(pricing_suggestion, 2)
    else:
        return "Competitor price exceeds the maximum price."

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")  # Assuming "index.html" exists in the "templates" directory

class CalculatePriceHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            price_history = float(self.get_argument("price_history"))
            competitor_price = float(self.get_argument("competitor_price"))
            max_increase_percent = float(self.get_argument("max_increase_percent"))

            pricing_suggestion = get_pricing_suggestion(price_history, competitor_price, max_increase_percent)

            self.render("result.html", pricing_suggestion=pricing_suggestion, error=None)
        except Exception as e:
            error_message = f"Error calculating price: {e}"
            self.render("error.html", error=error_message)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/calculate_price", CalculatePriceHandler),
    ], template_path="templates")

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    print("Server running on port 8889")
    tornado.ioloop.IOLoop.current().start()








#Web Server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Init DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                q = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += '<a href = "/restaurants/new">Make a New Restaurant HERE.</a>'
                output += "<br><br>"

                for item in q:
                    output += item.name
                    output += "<br>"
                    output += "<a href = '/restaurants/%s/edit'>Edit</a>" % item.id
                    output += "<br>"
                    output += "<a href = '#'>Delete</a>"
                    output += "<br><br>"
                output += "</html></body>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant_id = self.path.split("/")[-2]
                restaurant_item = session.query(Restaurant).filter(Restaurant.id==restaurant_id)[0]

                output = ""
                output += "<html><body>"
                output += "Rename %s" % restaurant_item.name
                output += "<br>"
                output += "<form method='POST' enctype='multipart/form-data' action ='/restaurants/%s/edit'><h2>What would you like the rename the restaurant?</h2><input name='newRestaurantName' type = 'text' placeholder='Restaurant Name Here'><input type ='submit' value='Submit'></form>" % restaurant_id
                output += "</html></body>"

                self.wfile.write(output)
                print output

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Make a New Restaurant Menu"
                output += "<br>"
                output += "<form method='POST' enctype='multipart/form-data' action ='/restaurants/new'><h2>What is the name of the restaurant?</h2><input name='newRestaurantName' type = 'text' placeholder='Restaurant Name Here'><input type ='submit' value='Submit'></form>"
                output += "</html></body>"

                self.wfile.write(output)
                print output
                
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print fields
                    messagecontent = fields.get('newRestaurantName')
                    
                    restaurant_id = self.path.split("/")[-2]
                    restaurant_item = session.query(Restaurant).filter(Restaurant.id==restaurant_id)[0]

                    restaurant_item.name = messagecontent[0]
                    session.add(restaurant_item)
                    session.commit()
                    print 'added renamed restaurant now named "%s"' % messagecontent[0]

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print fields
                    messagecontent = fields.get('newRestaurantName')
                
                    new_restaurant = Restaurant(name=messagecontent[0])
                    session.add(new_restaurant)
                    session.commit()
                    print 'added new restaurant named "%s" to DB' % messagecontent[0]

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    
                '''
                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += "<form method='POST' enctype='multipart/form-data' action ='/hello'><h2>What would you like me to say?</h2><input name='message' type = 'text'><input type ='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                '''

        except Exception as E:
            #TODO Fix this garbage
            print "erroreERROROROROROROR"
            print E
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()

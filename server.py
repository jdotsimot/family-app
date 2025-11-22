import http.server
import socketserver
import json
import os
import smtplib
from email.mime.text import MIMEText

PORT = 8000
DATA_FILE = "data.json"

def send_email(to_email, subject, body):
    # NOTE: You must enable "App Passwords" in your Google Account settings to use this.
    sender_email = "your_family_app_email@gmail.com"
    sender_password = "your_app_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                # Return empty object or null, frontend handles default
                self.wfile.write(b"null")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/data":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            with open(DATA_FILE, "wb") as f:
                f.write(post_data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/api/notify":
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            success = send_email(
                post_data.get('email'),
                "New Family App Notification",
                post_data.get('message')
            )

            self.send_response(200 if success else 500)
            self.end_headers()
            self.wfile.write(b"Email Sent" if success else b"Failed")
        else:
            self.send_error(404)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

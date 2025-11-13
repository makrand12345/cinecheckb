from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"message": "API is working!"}
        self.wfile.write(json.dumps(response).encode())

# Vercel needs this handler function
def handler(request, context):
    # This is a simplified version for Vercel
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"message": "API is working on Vercel!"})
    }
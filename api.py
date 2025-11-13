import json

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            "message": "CineCheck API is working!",
            "path": event.get('path', '/'),
            "method": event.get('httpMethod', 'GET')
        })
    }
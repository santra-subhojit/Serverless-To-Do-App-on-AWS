import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TodoItems')

def handler(event, context):
    http_method = event.get('httpMethod')
    if http_method == 'GET':
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []))
        }
    elif http_method == 'POST':
        body = json.loads(event.get('body', '{}'))
        todo_id = str(uuid.uuid4())
        item = {'id': todo_id, 'task': body.get('task', '')}
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'body': json.dumps(item)
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unsupported method'})
        }

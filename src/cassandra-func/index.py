import json
import os
import sys
sys.path.insert(0, 'src/vendor')
import boto3
import cql

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Helper function to validate event
def validate_event(event):
    if 'student_id' not in event:
        return 'Error: Missing student_id in event'
    if 'cassandra_host' not in event:
        return 'Error: Missing cassandra_host in event'
    if 'cassandra_port' not in event:
        return 'Error: Missing cassandra_port in event'
    if 'cassandra_keyspace' not in event:
        return 'Error: Missing cassandra_keyspace in event'
    return 'ok'

# Helper function to validate dynamo db item
# if any of the requried field is missing it will throw error
def validate_response(data):
    if 'id' not in data:
        return 'Error: Missing id in dynamo db table'
    if 'name' not in data:
        return 'Error: Missing name in dynamo db table'
    if 'start_date' not in data:
        return 'Error: Missing start_date in dynamo db table'
    if 'end_date' not in data:
        return 'Error: Missing end_date in dynamo db table'
    if 'amount' not in data:
        return 'Error: Missing amount in dynamo db table'
    if 'state' not in data:
        return 'Error: Missing state in dynamo db table'
    return 'ok'

# Entry Method
# Handler method for the lambda function
def handler(event, context):
    result = 'ok'

    # validating event
    validate = validate_event(event)
    if validate != 'ok':
        return validate

    # Getting values from event passed to lambda
    student_id = event['student_id']
    cassandra_host = event['cassandra_host']
    cassandra_port = event['cassandra_port']
    cassandra_keyspace = event['cassandra_keyspace']

    # Initializing dynamodb client
    client = boto3.client('dynamodb')
    
    #Getting table name from environment variable set in serverless yml
    # To update the dynamo db name you can update config.yml file
    table_name = os.environ['DYNAMO_DB_NAME']

    # if dynamo db name is fed to lambda through event, use this name
    if 'dynamo_db_name' in event:
        table_name = event['dynamo_db_name']
    
    try:
        # getting item from dynamo db table
        response = client.get_item(
            TableName=table_name,
            Key={
                'id': {'S': student_id}
            }
        )

        # validating the dynamo db item if requried data is missing
        validate_res = validate_response(response['Item'])
        if validate_item != 'ok':
            return validate

        # Connecting to Cassandra database
        con = cql.connect(cassandra_host, cassandra_port,  cassandra_keyspace, cql_version='3.0.0')
        cursor = con.cursor()

        # Insert to student_transaction_table
        CQLString = "INSERT INTO student_transaction_table (id, name, start_date, end_date, amount, state) VALUES (validate_res['id'], validate_res['name'], validate_res['start_date'], validate_res['end_date'], validate_res['amount'], validate_res['state']);"
        cursor.execute(CQLString)
    except Exception as e:
        print(e)
        result = 'Fail'
    finally:
        cur.close()
        con.close()
    return result;

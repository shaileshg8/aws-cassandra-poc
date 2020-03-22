# aws-cassandra-poc
```
This is a sample project to demonstrate: to read data from dynamo db table and insert the data into cassandra db
This project uses python, boto3, cql
pip install boto3
pip install cql

Before installation please verify your aws credentials
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
```

# Setting up Dynamo Db Table
```
Go to your AWS Management Console in your web browser
Navigate to Dynamo Db service, and create a table.
Update the config.yml, with the name you provided or you can feed the lambda the dynamo db name (eg. event/kafkaTopic.json)
{
    "dynamo_db_name": "aws-cassandra-poc-table",
    "student_id": "44",
    "cassandra_host": "172.24.24.24",
    "cassandra_port": 9160,
    "cassandra_keyspace": "test_keyspace"
}


Manually insert data with Partition Key , 'id'
Example Sample data:
{
  "amount": 1200,
  "end_date": "2020-03-22T04:36:10.418Z",
  "id": "44",
  "name": "test",
  "start_date": "2020-03-22T04:36:10.418Z",
  "state": "monthly"
}

If any of the data is missing in the dynamo db table, lambda will throw error

```

# Apache Cassandra
```
Get the cassandra host name, port and keyspace
and feed these informatin to lambda
eg: event/cassandra.json
Sample:
{
    "dynamo_db_name": "aws-cassandra-poc-table",
    "student_id": "44",
    "cassandra_host": "172.24.24.24",
    "cassandra_port": 9160,
    "cassandra_keyspace": "test_keyspace"
}
```

# Response
```
Lambda will insert into cassandra table: student_transaction_table, update the line 93 with the correct table name
Sample Insert Data:
{
  "amount": 1200,
  "end_date": "2020-03-22T04:36:10.418Z",
  "id": "44",
  "name": "test",
  "start_date": "2020-03-22T04:36:10.418Z",
  "state": "monthly"
}
```

# Installation
```
clone the project, cd to project directory
npm i
```

# Deployment
```
npm run prepare
npm run deploy
```

# Invocation
```
npm run invoke
```

# Remove
```
npm run remove
```

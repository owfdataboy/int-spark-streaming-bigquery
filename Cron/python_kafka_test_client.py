# A very simple Python programme to test connectivity and 
# configuration of Kafka client (this code) and Broker
#
# Pre-reqs:
#  - A Kafka broker
#  - Confluent Kafka Python library
#      pip3 install confluent_kafka
#
# Usage: 
#
#  python python_kafka_test_client.py [bootstrap server]
# 
# Refs: 
#  - https://docs.confluent.io/current/clients/python.html
#  - https://github.com/confluentinc/confluent-kafka-python/tree/master/examples
#  - https://rmoff.net/2018/08/02/kafka-listeners-explained/
#
# @rmoff 27 April 2020
#
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer
from confluent_kafka import Producer
import json


topic='test-topic'
file = './roam_prescription_based_prediction_test.jsonl'
bootstrap_server='34.121.179.78:9092'
print('⚠️  No bootstrap server defined, defaulting to {}\n'.format(bootstrap_server))


def Produce():
    print('\n<Producing>')
    try:   
        print('Initializing producer')
        p = Producer({'bootstrap.servers': bootstrap_server})

        def delivery_report(err, msg):
            """ Called once for each message produced to indicate delivery result.
                Triggered by poll() or flush(). """
            if err is not None:
                print('❌ Message delivery failed: {}'.format(err))
            else:
                print('✅  📬  Message delivered to {} [partition {}]'.format(msg.topic(), msg.partition()))
        
        print('Loading data')

        with open(file, 'r') as json_file:
            json_list = list(json_file)
        data = []
        for json_str in json_list:
            data.append(json.loads(json_str))

        print('Loaded data')

        for msg in data:
            p.produce(topic, str(msg).encode('utf-8'), callback=delivery_report)

        r=p.flush(timeout=5)
        if r>0:
            print('❌ Message delivery failed ({} message(s) still remain, did we timeout sending perhaps?)\n'.format(r))
    except:
        print("❌ (uncaught exception in produce)")

def Consume():
    print('\n<Consuming>')
    c = Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': 'rmoff',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([topic])
    try:
        msgs = c.consume(num_messages=1,timeout=30)

        if len(msgs)==0:
            print("❌ No message(s) consumed (maybe we timed out waiting?)\n")
        else:
            for msg in msgs:
                print('✅  💌  Message received:  "{}" from topic {}\n'.format(msg.value().decode('utf-8'),msg.topic()))
    except Exception as e:
        print("❌ Consumer error: {}\n".format(e))
    c.close()


a = AdminClient({'bootstrap.servers': bootstrap_server})
try:         
    md=a.list_topics(timeout=10)
    print("""
    ✅ Connected to bootstrap server(%s) and it returned metadata for brokers as follows:

    %s
        ---------------------
        ℹ️  This step just confirms that the bootstrap connection was successful. 
        ℹ️  For the consumer to work your client will also need to be able to resolve the broker(s) returned
            in the metadata above.
        ℹ️  If the host(s) shown are not accessible from where your client is running you need to change 
            your advertised.listener configuration on the Kafka broker(s).
    """
    % (bootstrap_server,md.brokers))

    try:
        Produce()
    except:
        print("❌ (uncaught exception in produce/consume)")


except Exception as e:
    print("""
    ❌ Failed to connect to bootstrap server.
    
    👉 %s
    
    ℹ️  Check that Kafka is running, and that the bootstrap server you've provided (%s) is reachable from your client
    """
    % (e,bootstrap_server))

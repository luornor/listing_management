import pika
import json
from shops.models import Listing, Shop
from decouple import config
from urllib.parse import urlparse

def on_message_callback(ch, method, properties, body):
    routing_key = method.routing_key
    print(f'received message with routing key "{routing_key}": "{body}"')
    
    try:
        # Decode the byte string
        body_str = body.decode('utf-8')
        
        # Parse the JSON string
        message = json.loads(body_str)
        
        if routing_key == 'listing.updated':
            handle_listing_updated(message)
        elif routing_key == 'shop.created':
            handle_shop_created(message)
        else:
            print(f'Unhandled routing key: {routing_key}')
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f'Error processing message: {str(e)}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def handle_listing_updated(message):
    try:
        # Extract the relevant data
        order_data = message[0][0]['order_data']
        
        # Update the Listing object
        product_id = order_data['listing_id']
        product = Listing.objects.get(id=product_id)
        product.quantity -= order_data['quantity']
        product.save()
        print(f'Product updated: {product.name} - {product.stock_quantity}')
    except Exception as e:
        print(f'Error Updating Product: {str(e)}')

def handle_shop_created(message):
    try:
        # Extract the relevant data
        user_data = message[0][0]['user_data']
        
        # Create the Shop object
        shop = Shop.objects.create(created_by=user_data['id'], name=f"{user_data['username']}'s shop")
        print(f'Shop created: {shop.name} - {shop.created_by}')
    except Exception as e:
        print(f'Error creating Shop: {str(e)}')

BROKER_URL = config('CLOUDAMQP_URL')
parsed_url = urlparse(BROKER_URL)

connection_parameters = pika.ConnectionParameters(
    host=parsed_url.hostname,
    port=parsed_url.port or 5672,
    virtual_host=parsed_url.path[1:] or '/',
    credentials=pika.PlainCredentials(parsed_url.username, parsed_url.password)
)

try:
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # Bind the queue to the exchange with different routing keys
    routing_keys = ['listing.updated', 'shop.created']
    for routing_key in routing_keys:
        channel.queue_bind(exchange='listing_exchange', queue='listing_queue', routing_key=routing_key)

    # Set up consumer with a single callback
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='listing_queue', on_message_callback=on_message_callback)

    print('Starting Consuming')
    channel.start_consuming()
except pika.exceptions.AMQPConnectionError as e:
    print(f'Error connecting to RabbitMQ: {str(e)}')
except Exception as e:
    print(f'An error occurred: {str(e)}')

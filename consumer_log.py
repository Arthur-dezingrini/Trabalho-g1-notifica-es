import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"[LOG] {message['user']} executou o evento: {message['event']}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='log_queue')

channel.basic_consume(queue='log_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(" [*] Aguardando todos os eventos. CTRL+C para sair")
channel.start_consuming()

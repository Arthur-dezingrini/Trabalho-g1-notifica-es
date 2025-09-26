import pika
import json
from datetime import datetime

# Conexão com RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criar exchange
channel.exchange_declare(exchange='user_events', exchange_type='direct')

# Criar filas
channel.queue_declare(queue='login_queue')
channel.queue_declare(queue='log_queue')

# Bindings (liga fila -> exchange + routing key)
channel.queue_bind(exchange='user_events', queue='login_queue', routing_key='user.login')
channel.queue_bind(exchange='user_events', queue='log_queue', routing_key='user.login')
channel.queue_bind(exchange='user_events', queue='log_queue', routing_key='user.upload')
channel.queue_bind(exchange='user_events', queue='log_queue', routing_key='user.logout')

# Função para enviar mensagem
def send_event(user, event):
    message = {
        "user": user,
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    channel.basic_publish(
        exchange='user_events',
        routing_key=event,
        body=json.dumps(message)
    )
    print(f" [x] Sent {message}")

# Teste: envia 3 eventos
send_event("João", "user.login")
send_event("João", "user.upload")
send_event("João", "user.logout")

connection.close()

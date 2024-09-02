from kafka import KafkaConsumer
import json
import asyncio
import websockets

kafka_consumer = KafkaConsumer(
    'realtime_numbers',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

async def handler(websocket, path):
    for message in kafka_consumer:
        number = message.value['number']
        await websocket.send(str(number))

async def main():
    async with websockets.serve(handler, "localhost", 2222):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

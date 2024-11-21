import asyncio
import websockets
from aioconsole import ainput


async def send_messages(websocket):
    while True:
        try:
            message = await ainput()
            await websocket.send(message)
        except (asyncio.CancelledError, EOFError):
            break


async def receive_messages(websocket):
    while True:
        try:
            response = await websocket.recv()
            print(f"\n{response}")
        except (asyncio.CancelledError, websockets.ConnectionClosed):
            break


async def chat_client(uri: str):
    async with websockets.connect(uri) as websocket:
        print("You joined the chat\n")
        sender_task = asyncio.create_task(send_messages(websocket))
        receiver_task = asyncio.create_task(receive_messages(websocket))
        _, pending = await asyncio.wait(
            [sender_task, receiver_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

if __name__ == "__main__":
    username = input("Enter your name: ")
    uri = f"ws://127.0.0.1:8000/ws/{username}"
    try:
        asyncio.run(chat_client(uri))
    except KeyboardInterrupt:
        print("\nYou have disconnected from chat")

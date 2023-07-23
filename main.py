from typing import List
import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


# База
@app.get("/", response_class=HTMLResponse)
async def read_items():
    with open('index.html', encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Список для хранения всех подключенных WebSocket клиентов
connected_clients: dict[WebSocket] = {}
game_started = False

async def day_time(websocket):
    ...

async def night_time(websocket):
    ...


from counties import Country
from random import shuffle

# WebSocket endpoint для подключения
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients[websocket] = None

    try:
        global game_started
        while True:
            # for client in connected_clients:
            #     await client.send_text(json.dumps(
            #         {"content": f"В очереди {len(connected_clients)}."},  ensure_ascii=False
            #     ))

            # print(connected_clients)
            # await websocket.receive_text()

            if len(connected_clients) >= 4 and len(connected_clients) % 2 == 0 and not(game_started):
                game_started = True
                
                # Распределяем страны
                from counties import countries
                shuffle(countries)
                countries = countries[:len(connected_clients)]
                for i, client in enumerate(connected_clients.keys()):
                    connected_clients[client] = Country(countries[i])
                countries = [v for v in connected_clients.values()]
                
                # Распределяем врагов
                for i in range(len(countries) // 2):
                    countries[i].villain = countries[i + (len(countries) // 2)]
                    countries[i + (len(countries) // 2)].villain = countries[i]

                # Распределение союзников
                shuffle(countries)
                countries[-1].friend = countries[0]
                for i in range(len(countries) - 1):
                    countries[i].friend = countries[i + 1]

                for client in connected_clients:
                    print(connected_clients[client].name, ":", connected_clients[client].friend.name, connected_clients[client].villain.name)

                # while len(connected_clients) != 1:
                #     await day_time(websocket)
                #     await night_time(websocket)


            # data = await websocket.receive_text()
            # message = {"content": "Hello user!"}

            # await websocket.send_text(json.dumps(message))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        connected_clients.pop(websocket)
        print("WebSocket client disconnected.")
        

























@app.on_event("startup")
async def startup_event():
    print("Server started and running.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Server stopped.")
    for client in connected_clients:
        try:
            await client.close()
        except Exception as e:
            print(f"Error while closing WebSocket: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
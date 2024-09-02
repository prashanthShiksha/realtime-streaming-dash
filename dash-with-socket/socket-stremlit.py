import streamlit as st
import asyncio
import websockets

# Set up the Streamlit page configuration
st.set_page_config(page_title="Real-Time Dashboard", layout="centered")

# Title of the dashboard
st.title("Real-Time Number Dashboard")

# Placeholder for the big number
number_placeholder = st.empty()

async def fetch_number():
    uri = "ws://localhost:2222"  # WebSocket server address
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    number = await websocket.recv()
                    number_placeholder.markdown(
                        f"<h1 style='font-size: 72px; text-align: center;'>{number}</h1>",
                        unsafe_allow_html=True
                    )
        except websockets.exceptions.ConnectionClosedError as e:
            st.warning(f"Connection closed: {e}. Reconnecting...")
            await asyncio.sleep(1)  # Wait before reconnecting
        except Exception as e:
            st.error(f"An error occurred: {e}")
            break

# Run the WebSocket client within the Streamlit app
asyncio.run(fetch_number())

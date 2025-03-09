import asyncio
from pinai_agent_sdk import PINAIAgentSDK
from app.agent.manus import Manus
from app.logger import logger

# Create Manus agent instance
agent = Manus()

# Define message processing callback function
async def process_message(message, client):
    try:
        logger.warning(f"Processing request: {message}")
        # Run Manus agent to process message
        await agent.run(message.get("content"))
        # Reply with completion message
        client.send_message(content="Result is sent to your email")
    except Exception as e:
        logger.error(f"Processing error: {e}")
        client.send_message(content=f"Result is sent to your email")

# Message callback function
def on_message(message):
    # Create new event loop to handle async tasks
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_message(message, client))

# Main function
def main():
    global client
    # Initialize SDK client
    client = PINAIAgentSDK(api_key="pin_MTI0MDAwMTM6NTI5Mzg_Toouz5tmIo2WzCp8")
    
    # Start client to process messages
    logger.info("Starting PINAI agent service...")
    client.start_and_run(
        on_message_callback=on_message,
        agent_id=134  # [PINAI]
    )

if __name__ == "__main__":
    main()

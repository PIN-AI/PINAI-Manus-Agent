import asyncio
import threading
from pinai_agent_sdk import PINAIAgentSDK, AGENT_CATEGORY_SOCIAL
from app.agent.manus import Manus
from app.logger import logger

class ManusAgentHandler:
    def __init__(self, api_key, agent_id):
        self.agent = Manus()
        self.api_key = api_key
        self.agent_id = agent_id
        self.client = None
        # Create a dedicated event loop for handling async tasks
        self.loop = asyncio.new_event_loop()
        self.thread = None
    
    async def process_message(self, message):
        """Process message and run through Manus agent"""
        logger.warning(f"Processing request: {message}")
        try:
            # Assume agent.run processes the message and returns a response
            # If the run method doesn't return a response, the way to capture the response needs to be modified here
            response = await self.agent.run(message.get("content"))
            return response if response else "Processing completed"
        except Exception as e:
            logger.error(f"Exception processing message: {e}")
            return f"Request processing failed: {str(e)}"
    
    def on_message(self, message):
        """Message callback handler"""
        # Submit async task to the event loop
        future = asyncio.run_coroutine_threadsafe(
            self.process_message(message), 
            self.loop
        )
        try:
            # Get async processing result and send reply
            response = future.result(timeout=60)
            self.client.send_message(content=response)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.client.send_message(content=f"Error processing your request: {str(e)}")
    
    def run_event_loop(self):
        """Run event loop in a dedicated thread"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def start(self):
        """Start the agent service"""
        # Create and start event loop thread
        self.thread = threading.Thread(target=self.run_event_loop, daemon=True)
        self.thread.start()
        
        # Initialize SDK client
        self.client = PINAIAgentSDK(api_key=self.api_key)
        
        logger.info("Starting PINAI agent service...")
        # Start the client
        self.client.start_and_run(
            on_message_callback=self.on_message,
            agent_id=self.agent_id
        )

def main():
    # Create and start agent handler
    handler = ManusAgentHandler(
        api_key="pin_MTI0MDAwMTM6NTI5Mzg_Toouz5tmIo2WzCp8",
        agent_id=134
    )
    
    try:
        handler.start()
        # Keep main thread running
        while True:
            try:
                # Use simple command line interaction to keep the program running
                cmd = input("Enter 'exit' to quit the program: ")
                if cmd.lower() == 'exit':
                    break
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        logger.warning("Program interrupted")
    finally:
        # Add cleanup work here if needed
        logger.info("Agent service has been shut down")
        if handler.loop.is_running():
            handler.loop.call_soon_threadsafe(handler.loop.stop)
        

if __name__ == "__main__":
    main()

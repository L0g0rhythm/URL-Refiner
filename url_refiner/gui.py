import eel
import sys
import logging
from url_refiner.core import process_urls

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@eel.expose
def process_urls_py(urls: list[str], config: dict):
    """
    A wrapper function that calls the core processing logic.
    This is exposed to JavaScript and handles communication and errors.
    """
    logging.info(f"Received job from JS: {len(urls)} URLs, config: {config}")
    try:
        # The core logic now returns a dictionary with data and stats
        # For the GUI, the list is already in memory, so we pass it directly.
        result = process_urls(urls, config)
        logging.info("Processing successful. Sending data back to JS.")
        return {"status": "success", "data": result["data"], "stats": result["stats"]}
    except Exception as e:
        logging.error(f"An error occurred during URL processing: {e}", exc_info=True)
        # Return a structured error response
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}

def start_gui():
    """Initializes and starts the Eel GUI server and application window."""
    try:
        # Initialize Eel, pointing to the 'web' folder for assets
        # This path needs to be relative to where the script is run.
        # A better approach would be to use package resources.
        import os
        web_dir = os.path.join(os.path.dirname(__file__), '..', 'web')
        eel.init(web_dir)
        
        logging.info("Starting Eel GUI...")
        eel.start('index.html', size=(1280, 800), mode='chrome', host='localhost')

    except (SystemExit, MemoryError, KeyboardInterrupt):
        logging.info("GUI closing.")
        sys.exit()
    except Exception as e:
        logging.error(f"Could not start GUI. Is Chrome installed? Error: {e}")
        print("\nCould not start GUI. Eel requires Chrome or a compatible browser.", file=sys.stderr)
        print("Please see the Eel documentation for more details.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    start_gui()
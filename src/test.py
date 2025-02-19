from playwright.async_api import async_playwright
import asyncio
import signal
import sys

class AsyncPersistentBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.running = True
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        print("\nClosing browser gracefully...")
        self.running = False
        
    async def start(self):
        """Start the browser if it's not already running"""
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            self.context = await self.browser.new_context(
                viewport=None,
                no_viewport=True
            )
    
    async def get_page(self):
        """Get a new page in the existing browser context"""
        if not self.browser:
            await self.start()
        return await self.context.new_page()
    
    async def close(self):
        """Clean up resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def keep_alive(self):
        """Keep the browser running indefinitely"""
        try:
            print("Browser is running. Press Ctrl+C to stop...")
            while self.running:
                await asyncio.sleep(1)
        finally:
            await self.close()

async def main():
    browser = AsyncPersistentBrowser()
    await browser.start()
    
    # Example: Open a page and do some async operations
    page = await browser.get_page()
    await page.goto("https://example.com")
    
    # Keep the browser running
    await browser.keep_alive()

# Example with more complex usage
async def example_with_multiple_pages():
    browser = AsyncPersistentBrowser()
    await browser.start()
    
    # Open multiple pages concurrently
    pages = await asyncio.gather(
        browser.get_page(),
        browser.get_page(),
        browser.get_page()
    )
    
    # Navigate to different sites concurrently
    await asyncio.gather(
        pages[0].goto("https://example.com"),
        pages[1].goto("https://google.com"),
        pages[2].goto("https://github.com")
    )
    
    # Keep browser alive
    await browser.keep_alive()

if __name__ == "__main__":
    # Run the simple example
    asyncio.run(main())
    
    # Or run the complex example
    # asyncio.run(example_with_multiple_pages())
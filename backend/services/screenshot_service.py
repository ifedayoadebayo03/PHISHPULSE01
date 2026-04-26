"""
Screenshot capture service using Playwright.
"""

import os
import asyncio
from typing import Optional, Dict
from pathlib import Path

from backend.app.config import settings


class ScreenshotService:
    """Headless screenshot capture service."""
    
    def __init__(self):
        self.viewport = settings.SCREENSHOT_VIEWPORT
        self.timeout = settings.SCREENSHOT_TIMEOUT
        self.playwright = None
        self.browser = None
    
    async def _init_browser(self):
        """Initialize Playwright browser."""
        from playwright.async_api import async_playwright
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
    
    async def capture(
        self,
        url: str,
        output_path: Optional[str] = None,
        full_page: bool = True
    ) -> Dict:
        """
        Capture screenshot of URL.
        
        Args:
            url: URL to screenshot
            output_path: Optional output path (auto-generated if not provided)
            full_page: Capture full page or just viewport
        
        Returns:
            Dict with screenshot path and metadata
        """
        if not self.browser:
            await self._init_browser()
        
        # Generate output path if not provided
        if not output_path:
            import uuid
            filename = f"screenshot_{uuid.uuid4().hex[:8]}.png"
            output_path = os.path.join(settings.REPORTS_DIR, filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        result = {
            "url": url,
            "screenshot_path": None,
            "success": False,
            "error": None,
            "page_title": None,
            "final_url": None
        }
        
        try:
            page = await self.browser.new_page(
                viewport=self.viewport
            )
            
            # Navigate to URL
            response = await page.goto(
                url,
                wait_until='networkidle',
                timeout=self.timeout
            )
            
            # Get page info
            result["page_title"] = await page.title()
            result["final_url"] = page.url
            result["http_status"] = response.status if response else None
            
            # Take screenshot
            await page.screenshot(
                path=output_path,
                full_page=full_page,
                type='png'
            )
            
            result["screenshot_path"] = output_path
            result["success"] = True
            
            await page.close()
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def capture_element(
        self,
        url: str,
        selector: str,
        output_path: Optional[str] = None
    ) -> Dict:
        """Capture specific element on page."""
        if not self.browser:
            await self._init_browser()
        
        if not output_path:
            import uuid
            filename = f"element_{uuid.uuid4().hex[:8]}.png"
            output_path = os.path.join(settings.REPORTS_DIR, filename)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        result = {
            "url": url,
            "selector": selector,
            "screenshot_path": None,
            "success": False,
            "error": None
        }
        
        try:
            page = await self.browser.new_page(viewport=self.viewport)
            await page.goto(url, wait_until='networkidle', timeout=self.timeout)
            
            element = await page.wait_for_selector(selector, timeout=5000)
            if element:
                await element.screenshot(path=output_path)
                result["screenshot_path"] = output_path
                result["success"] = True
            else:
                result["error"] = f"Element not found: {selector}"
            
            await page.close()
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def close(self):
        """Close browser and playwright."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    def capture_sync(
        self,
        url: str,
        output_path: Optional[str] = None,
        full_page: bool = True
    ) -> Dict:
        """Synchronous wrapper for capture."""
        return asyncio.run(self.capture(url, output_path, full_page))

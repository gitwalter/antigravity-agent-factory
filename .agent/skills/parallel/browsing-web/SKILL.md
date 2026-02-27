---
agents:
- none
category: parallel
description: Web scraping with agents, browser automation, content extraction, and
  ethical scraping practices
knowledge:
- none
name: browsing-web
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Web Browsing

Web scraping with agents, browser automation, content extraction, and ethical scraping practices

Build AI agents that browse the web, scrape content, and automate browser interactions using Playwright, Selenium, and other tools.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Basic Web Scraping with httpx and BeautifulSoup

```python
import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

async def fetch_page(url: str, headers: Optional[Dict] = None) -> str:
    """Fetch HTML content from URL."""
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    if headers:
        default_headers.update(headers)

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(url, headers=default_headers)
        response.raise_for_status()
        return response.text

def parse_html(html: str) -> BeautifulSoup:
    """Parse HTML with BeautifulSoup."""
    return BeautifulSoup(html, "lxml")

async def scrape_basic(url: str) -> Dict[str, any]:
    """Basic web scraping example."""
    html = await fetch_page(url)
    soup = parse_html(html)

    return {
        "title": soup.title.string if soup.title else None,
        "headings": [h.get_text() for h in soup.find_all(["h1", "h2", "h3"])],
        "links": [a.get("href") for a in soup.find_all("a", href=True)],
        "text": soup.get_text()[:1000]  # First 1000 chars
    }

# Usage
result = await scrape_basic("https://example.com")
print(result)
```

### Step 2: Structured Content Extraction

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Article(BaseModel):
    """Structured article data."""
    title: str
    content: str
    author: Optional[str] = None
    published_date: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

def extract_article(soup: BeautifulSoup, url: str) -> Article:
    """Extract structured article data."""

    # Try common article selectors
    title_selectors = [
        "h1.article-title",
        "h1.post-title",
        "article h1",
        "h1"
    ]

    title = None
    for selector in title_selectors:
        elem = soup.select_one(selector)
        if elem:
            title = elem.get_text().strip()
            break

    # Extract content
    content_selectors = [
        "article .content",
        ".post-content",
        "article",
        "main"
    ]

    content = None
    for selector in content_selectors:
        elem = soup.select_one(selector)
        if elem:
            content = elem.get_text().strip()
            break

    # Extract author
    author_elem = soup.select_one(".author, [rel='author'], .byline")
    author = author_elem.get_text().strip() if author_elem else None

    # Extract date
    date_elem = soup.select_one("time, .date, .published")
    date = date_elem.get("datetime") or (date_elem.get_text() if date_elem else None)

    # Extract tags
    tag_elems = soup.select(".tags a, .tag, [rel='tag']")
    tags = [tag.get_text().strip() for tag in tag_elems]

    return Article(
        title=title or "Untitled",
        content=content or "",
        author=author,
        published_date=date,
        tags=tags
    )

# Usage
html = await fetch_page("https://example.com/article")
soup = parse_html(html)
article = extract_article(soup, "https://example.com/article")
print(article.model_dump_json(indent=2))
```

### Step 3: Browser Automation with Playwright

```python
from playwright.async_api import async_playwright, Page, Browser
from typing import Optional

class WebBrowser:
    """Browser automation wrapper."""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def start(self, headless: bool = True):
        """Start browser instance."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def close(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()

    async def navigate(self, url: str, wait_until: str = "networkidle"):
        """Navigate to URL."""
        await self.page.goto(url, wait_until=wait_until)

    async def get_content(self) -> str:
        """Get page HTML content."""
        return await self.page.content()

    async def get_text(self) -> str:
        """Get page text content."""
        return await self.page.inner_text("body")

    async def click(self, selector: str):
        """Click element by selector."""
        await self.page.click(selector)

    async def fill(self, selector: str, text: str):
        """Fill input field."""
        await self.page.fill(selector, text)

    async def screenshot(self, path: str):
        """Take screenshot."""
        await self.page.screenshot(path=path)

    async def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for element to appear."""
        await self.page.wait_for_selector(selector, timeout=timeout)

# Usage
browser = WebBrowser()
await browser.start(headless=True)
await browser.navigate("https://example.com")
content = await browser.get_content()
await browser.close()
```

### Step 4: JavaScript-Heavy Site Scraping

```python
async def scrape_spa(browser: WebBrowser, url: str) -> Dict:
    """Scrape Single Page Application (SPA)."""
    await browser.navigate(url, wait_until="networkidle")

    # Wait for content to load
    await browser.wait_for_selector(".content", timeout=10000)

    # Execute JavaScript to extract data
    data = await browser.page.evaluate("""
        () => {
            return {
                title: document.title,
                headings: Array.from(document.querySelectorAll('h1, h2')).map(h => h.textContent),
                articles: Array.from(document.querySelectorAll('.article')).map(article => ({
                    title: article.querySelector('.title')?.textContent,
                    content: article.querySelector('.content')?.textContent
                }))
            }
        }
    """)

    return data

# Usage
browser = WebBrowser()
await browser.start()
result = await scrape_spa(browser, "https://spa-example.com")
await browser.close()
```

### Step 5: Rate Limiting and Ethical Scraping

```python
import asyncio
from datetime import datetime, timedelta
from collections import deque
from typing import Deque

class RateLimiter:
    """Rate limiter for web requests."""

    def __init__(self, max_requests: int, time_window: int):
        """
        Args:
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Deque[datetime] = deque()

    async def acquire(self):
        """Wait if necessary to respect rate limit."""
        now = datetime.now()

        # Remove old requests outside time window
        while self.requests and (now - self.requests[0]).total_seconds() > self.time_window:
            self.requests.popleft()

        # Wait if at limit
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0]).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                return await self.acquire()

        self.requests.append(datetime.now())

class EthicalScraper:
    """Web scraper with ethical practices."""

    def __init__(self, requests_per_minute: int = 30):
        self.rate_limiter = RateLimiter(requests_per_minute, 60)
        self.session = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
            }
        )

    async def fetch(self, url: str) -> str:
        """Fetch URL with rate limiting."""
        await self.rate_limiter.acquire()

        # Check robots.txt (simplified - use robotparser in production)
        # Respect robots.txt in production

        response = await self.session.get(url)
        response.raise_for_status()
        return response.text

    async def scrape(self, url: str) -> Dict:
        """Scrape with ethical practices."""
        html = await self.fetch(url)
        soup = parse_html(html)

        return {
            "url": url,
            "title": soup.title.string if soup.title else None,
            "content": soup.get_text()[:5000]  # Limit content size
        }

    async def close(self):
        """Close session."""
        await self.session.aclose()

# Usage
scraper = EthicalScraper(requests_per_minute=30)
result = await scraper.scrape("https://example.com")
await scraper.close()
```

### Step 6: Content Extraction with LLM

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class LLMContentExtractor:
    """Extract structured content using LLM."""

    def __init__(self, llm):
        self.llm = llm

    async def extract(self, html: str, extraction_schema: BaseModel) -> BaseModel:
        """Extract structured data from HTML using LLM."""
        soup = parse_html(html)
        text_content = soup.get_text()[:8000]  # Limit for LLM context

        parser = PydanticOutputParser(pydantic_object=extraction_schema)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract structured data from web page content.

{format_instructions}

Extract only information that is clearly present in the content."""),
            ("user", "Extract data from this page:\n\n{content}")
        ])

        chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser

        result = await chain.ainvoke({"content": text_content})
        return result

# Usage
class ProductInfo(BaseModel):
    name: str
    price: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None

extractor = LLMContentExtractor(llm)
html = await fetch_page("https://example.com/product")
product = await extractor.extract(html, ProductInfo)
print(product)
```

### Step 7: Complete Web Browsing Agent

```python
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

class WebBrowsingAgent:
    """Complete web browsing agent."""

    def __init__(self, llm, browser: WebBrowser):
        self.llm = llm
        self.browser = browser
        self.scraper = EthicalScraper()

    @tool
    async def search_web(self, query: str) -> str:
        """Search the web and return results."""
        # In production, use a search API
        # For demo, simulate search
        return f"Search results for: {query}"

    @tool
    async def fetch_page(self, url: str) -> str:
        """Fetch and return page content."""
        html = await self.scraper.fetch(url)
        soup = parse_html(html)
        return soup.get_text()[:5000]

    @tool
    async def navigate_and_extract(self, url: str, selector: str) -> str:
        """Navigate to URL and extract content by selector."""
        await self.browser.navigate(url)
        try:
            element = await self.browser.page.query_selector(selector)
            if element:
                return await element.inner_text()
            return "Element not found"
        except Exception as e:
            return f"Error: {e}"

    async def research(self, question: str) -> str:
        """Research a question using web browsing."""
        # Step 1: Generate search query
        search_prompt = ChatPromptTemplate.from_messages([
            ("system", "Generate a web search query to answer the question."),
            ("user", "{question}")
        ])

        search_chain = search_prompt | self.llm | StrOutputParser()
        search_query = await search_chain.ainvoke({"question": question})

        # Step 2: Search
        search_results = await self.search_web(search_query)

        # Step 3: Extract relevant URLs (simplified)
        # In production, parse search results properly

        # Step 4: Fetch and summarize
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", "Summarize the web content to answer the question."),
            ("user", """Question: {question}
Content: {content}

Provide a comprehensive answer.""")
        ])

        # Fetch top result (simplified)
        content = await self.fetch_page("https://example.com")  # Use actual URL

        summary_chain = summary_prompt | self.llm | StrOutputParser()
        answer = await summary_chain.ainvoke({
            "question": question,
            "content": content
        })

        return answer

# Usage
browser = WebBrowser()
await browser.start()
agent = WebBrowsingAgent(llm, browser)
answer = await agent.research("What is the latest news about AI?")
print(answer)
await browser.close()
```

```

### Step 8: Tavily Integration (New)

Use the `tavily` MCP server for advanced search and research capabilities:

```python
# Perform a comprehensive research task
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Research the impact of quantum computing on cryptography"}],
    tools=[{
        "type": "mcp",
        "name": "tavily",
        "command": "npx",
        "args": ["-y", "tavily-mcp"]
    }]
)
```

## Scraping Patterns

| Pattern | Use Case | Tool |
|---------|----------|------|
| Static HTML | Simple sites | httpx + BeautifulSoup |
| JavaScript-heavy | SPAs, React apps | Playwright/Selenium |
| API endpoints | Data APIs | httpx (direct API calls) |
| Rate-limited | Many requests | RateLimiter |
| Structured data | E-commerce, articles | LLM extraction |

## Best Practices

- Respect robots.txt and rate limits
- Use appropriate User-Agent headers
- Implement retry logic with exponential backoff
- Cache responses when possible
- Handle errors gracefully
- Use async/await for concurrent requests
- Limit content size for LLM processing
- Respect website terms of service
- Use browser automation only when necessary
- Clean and validate extracted data

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No rate limiting | Implement RateLimiter |
| Ignoring robots.txt | Check and respect robots.txt |
| Synchronous requests | Use async/await |
| No error handling | Wrap in try/except |
| Hardcoded selectors | Use flexible extraction |
| No timeout handling | Set appropriate timeouts |
| Ignoring HTTP status | Check response.status_code |
| Scraping too frequently | Implement delays between requests |
| No content validation | Validate extracted data |
| Ignoring legal/ethical | Review ToS and use responsibly |

## Related

- Knowledge: `{directories.knowledge}/api-integration-patterns.json`
- Skill: `tool-usage`
- Skill: `using-langchain`
- Skill: `mcp-integration`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

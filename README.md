# Tag Scraper

Using a breadth-first search (BFS) approach using a deque and `asyncio` event loop/`aiohttp` for asynchronous HTTP requests to search for your specific tag's(along with optional style and class names) child elements across your given domain.

## Requirements

| Dependency     | Version |
|----------------|---------|
| aiohttp        | 3.8.4   |
| asyncio        | 3.4.3   |
| beautifulsoup4 | 4.12.2  |
| python         | 3.11.2  |

## Usage
Ensure you are in the parent directory of `tag-scraper.py` and run:
``` bash
python3 tag-scraper.py
```

You shall then recieve the following promps where you shall input:
```
Enter your domain (i.e. www.google.com): <enter your domain here>
Enter a tag to search for (i.e. h1, p, a): <enter your tag here>
Enter a className to search for: <optional: enter your class name here>
Enter style to search for (i.e. margin-bottom: 37px;): <optional: enter styles here>
```

## Contributing

[James O'Connell](https://github.com/oconnellj2) - jdoconnell@pm.me
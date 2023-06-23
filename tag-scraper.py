"""
	tag-scraper.py
	=======
	Purpose:
	--------
		Using a breadth-first search (BFS) approach using a deque and `asyncio`
		event loop/`aiohttp` for asynchronous HTTP requests to search for your
		specific tag's(along with optional style and class names) child
		elements across your given domain.
	Contributing:
	-------------
		James O'Connell | Software Engineer
"""

from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
from collections import deque
import asyncio
import aiohttp
import ssl

sslcontext = ssl.create_default_context()
sslcontext.check_hostname = False
sslcontext.verify_mode = ssl.CERT_NONE


async def scrape_domain_specific_tag(domain, tagSearch, classSearch, styleSearch, max_depth=3):
	base_url = f"https://{domain}"
	specific_tags = set()
	visited = set()

	async def traverse_links(url, route, depth):
		visited.add(url)

		async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=sslcontext)) as session:
			async with session.get(url) as response:
				if response.status == 200:
					content = await response.text()
					soup = BeautifulSoup(content, "html.parser")

					tag_elements = soup.find_all(
						tagSearch, class_=re.compile(classSearch), style=styleSearch)
					tags_text = [tag.get_text() for tag in tag_elements]
					specific_tags.update(tags_text)
					print("Page:", url)

					if depth > 0:
						internal_links = soup.find_all(
							"a", href=re.compile(r"^\/"))
						tasks = []
						for link in internal_links:
							absolute_link = urljoin(url, link["href"])
							parsed_link = urlparse(absolute_link)
							if (
									parsed_link.netloc == domain
									and absolute_link not in visited
									and not any(absolute_link.endswith(ext) for ext in [".pdf", ".jpg", ".png", ".docx", ".xlsm", ".xlsx", ".dwg", ".doc"])
							):
								tasks.append(traverse_links(
									absolute_link, route, depth - 1))
						await asyncio.gather(*tasks)

	# Create a deque to implement BFS
	queue = deque([(base_url, base_url, max_depth)])

	while queue:
		url, route, depth = queue.popleft()
		await traverse_links(url, route, depth)

	return specific_tags


def main():
	# "h1", class_=re.compile(r"display4|display-4"), style="text-align: center; color: rgb(var(--light-blue)); margin-bottom: 37px;"
	domain = input("Enter your domain (i.e. www.example.com): ")
	tag = input("Enter a tag to search for (i.e. h1, p, a): ")
	className = input("Enter a className to search for: ")
	style = input("Enter style to search for (i.e. margin-bottom: 37px;): ")

	scraped_specific_tags = asyncio.run(scrape_domain_specific_tag(
		domain, tag, className, style, max_depth=3))
	# Print the scraped tags
	if not scraped_specific_tags:
		print("No Results Found!")
	for tag in scraped_specific_tags:
		print(tag)


if __name__ == "__main__":
	main()

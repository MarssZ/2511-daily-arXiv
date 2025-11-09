"""
NeurIPS Conference Papers Spider

Crawls NeurIPS conference oral/spotlight papers from neurips.cc virtual conference site.
Outputs standardized JSONL format compatible with existing AI enhancement pipeline.
"""

import scrapy
from typing import Iterator, Dict, Optional
import re


class NeuripsSpider(scrapy.Spider):
    """
    Spider for crawling NeurIPS conference papers.

    Supports:
    - Oral papers (default)
    - Spotlight papers (future)
    - Multiple years

    Usage:
        scrapy crawl neurips -o neurips-2024-oral.jsonl
        scrapy crawl neurips -a year=2024 -a category=oral
    """

    name = "neurips"
    allowed_domains = ["neurips.cc", "openreview.net"]

    def __init__(self, year: str = "2024", category: str = "oral", *args, **kwargs):
        """
        Initialize NeurIPS spider.

        Args:
            year: Conference year (default: "2024")
            category: Paper category - "oral" or "spotlight" (default: "oral")
        """
        super().__init__(*args, **kwargs)
        self.year = year
        self.category = category.lower()
        self.start_urls = [
            f"https://neurips.cc/virtual/{year}/events/{self.category}"
        ]

        # Statistics counters
        self.failed_count = 0
        self.no_pdf_count = 0

        self.logger.info(f"NeurIPS Spider initialized: year={year}, category={category}")

    # Custom settings: disable Pipeline + polite crawling
    custom_settings = {
        'ITEM_PIPELINES': {},  # Disable Pipeline (spider outputs complete data)
        'DOWNLOAD_DELAY': 1,   # 1 second between requests
        'CONCURRENT_REQUESTS': 1,  # Single-threaded crawling
        'ROBOTSTXT_OBEY': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        'DOWNLOAD_TIMEOUT': 30,
    }

    def parse(self, response):
        """
        Parse the NeurIPS papers list page.

        Extracts basic paper information and generates requests for detail pages.
        """
        self.logger.info("Parsing NeurIPS list page...")

        papers_found = 0

        # Each paper is in a <div class="displaycards">
        for paper_card in response.css('div.displaycards'):
            # Extract title and detail link from <a class="small-title">
            title_link = paper_card.css('div.virtual-card a.small-title')
            title = title_link.css('::text').get()
            detail_url_path = title_link.css('::attr(href)').get()

            if not title or not detail_url_path:
                continue

            detail_url = response.urljoin(detail_url_path)

            # Extract authors from <div class="author-str">
            authors_text = paper_card.css('div.author-str::text').get()
            authors = []
            if authors_text and '·' in authors_text:
                authors = [a.strip() for a in authors_text.split('·') if a.strip()]

            # Extract abstract from <details><summary>Abstract</summary>
            abstract_text = paper_card.css('details summary:contains("Abstract") + div.text-start::text').get()
            if not abstract_text:
                # Try alternative: get all text inside the div after "Abstract"
                abstract_div = paper_card.css('details div.text-start')
                if abstract_div:
                    abstract_text = abstract_div.css('::text').getall()
                    abstract_text = ' '.join([t.strip() for t in abstract_text if t.strip()])

            # Validate required fields
            if not title or not title.strip():
                self.logger.warning(f"Skipping paper: missing title")
                continue

            if not abstract_text or not abstract_text.strip():
                self.logger.warning(f"Skipping paper '{title}': missing abstract")
                continue

            papers_found += 1
            self.logger.info(f"Found paper: {title[:60]}...")

            # Build item with basic info
            item = {
                'title': title.strip(),
                'authors': authors if authors else [],
                'summary': abstract_text.strip() if isinstance(abstract_text, str) else abstract_text,
                'abs': detail_url,
                'categories': [f"NeurIPS {self.year} {self.category.capitalize()}"],
                'comment': None,
                'source': 'neurips',
            }

            # Request detail page to get OpenReview link
            yield scrapy.Request(
                detail_url,
                callback=self.parse_detail,
                meta={'item': item},
                errback=self.errback_detail,
                dont_filter=True,
            )

        self.logger.info(f"Found {papers_found} papers on list page")

    def parse_detail(self, response):
        """
        Parse paper detail page for OpenReview link.

        Extracts OpenReview forum link and generates PDF URL.
        """
        item = response.meta['item']

        # Extract paper ID from URL (e.g., /virtual/2024/oral/97958 -> 97958)
        paper_id = self._extract_paper_id(response.url)
        if paper_id:
            item['id'] = f"neurips{self.year}_{self.category}_{paper_id}"
        else:
            # Fallback: use URL hash
            import hashlib
            url_hash = hashlib.md5(response.url.encode()).hexdigest()[:8]
            item['id'] = f"neurips{self.year}_{self.category}_{url_hash}"
            self.logger.warning(f"Could not extract paper ID from {response.url}, using hash: {item['id']}")

        # Extract OpenReview link
        openreview_link = self._extract_openreview_link(response)

        if openreview_link:
            item['pdf'] = self._generate_pdf_url(openreview_link)
            if item['pdf']:
                self.logger.debug(f"OpenReview link found: {openreview_link}")
            else:
                self.no_pdf_count += 1
                self.logger.info(f"No OpenReview link found for {item['id']}, PDF field left empty")
        else:
            item['pdf'] = ""
            self.no_pdf_count += 1
            self.logger.info(f"No OpenReview link found for {item['id']}, PDF field left empty")

        yield item

    def errback_detail(self, failure):
        """
        Handle errors when fetching detail pages.

        Outputs item with basic info but empty PDF field.
        """
        self.failed_count += 1
        item = failure.request.meta['item']
        item['pdf'] = ""
        item['id'] = f"neurips{self.year}_{self.category}_unknown_{self.failed_count}"

        self.logger.error(f"Failed to fetch detail page for '{item['title'][:50]}...': {failure.value}")
        self.logger.info(f"Outputting basic info without PDF for {item['id']}")

        # Still yield the item with basic info
        yield item

    def _extract_paper_id(self, url: str) -> Optional[str]:
        """
        Extract paper ID from detail page URL.

        Args:
            url: Detail page URL (e.g., https://neurips.cc/virtual/2024/oral/97958)

        Returns:
            Paper ID (e.g., "97958") or None if not found
        """
        # Match pattern: /oral/12345 or /spotlight/12345
        match = re.search(r'/(?:oral|spotlight)/(\d+)', url)
        if match:
            return match.group(1)
        return None

    def _extract_openreview_link(self, response) -> str:
        """
        Extract OpenReview forum link from detail page.

        Uses multiple fallback selectors for robustness.

        Args:
            response: Scrapy response object

        Returns:
            OpenReview forum URL or empty string if not found
        """
        # Multiple candidate selectors (in priority order)
        selectors = [
            'a:contains("OpenReview")::attr(href)',
            'a[href*="openreview.net/forum"]::attr(href)',
            'a[href*="openreview.net"]::attr(href)',
        ]

        for selector in selectors:
            link = response.css(selector).get()
            if link:
                # Ensure it's a full URL
                if link.startswith('http'):
                    return link
                else:
                    return response.urljoin(link)

        return ""

    def _generate_pdf_url(self, openreview_link: str) -> str:
        """
        Generate PDF download URL from OpenReview forum link.

        Args:
            openreview_link: OpenReview forum URL (e.g., https://openreview.net/forum?id=ABC123)

        Returns:
            PDF URL (e.g., https://openreview.net/pdf?id=ABC123) or empty string
        """
        if not openreview_link:
            return ""

        # Extract OpenReview ID from forum link
        # Pattern: https://openreview.net/forum?id=ABC123
        match = re.search(r'[?&]id=([^&]+)', openreview_link)
        if match:
            openreview_id = match.group(1)
            return f"https://openreview.net/pdf?id={openreview_id}"

        return ""

    def closed(self, reason):
        """
        Called when spider closes. Outputs statistics.

        Args:
            reason: Spider close reason
        """
        total = self.crawler.stats.get_value('item_scraped_count', 0)
        failed_rate = self.failed_count / total if total > 0 else 0

        self.logger.info(f"""
        ===== NeurIPS Crawler Statistics =====
        Total papers processed: {total}
        Successful items: {total}
        Failed detail pages: {self.failed_count}
        Papers without PDF: {self.no_pdf_count}
        ======================================
        """)

        # Alert if failure rate is too high
        if failed_rate > 0.5:
            self.logger.error(
                f"ALERT: Over 50% of papers failed to crawl ({failed_rate:.1%}). "
                f"Please check if the website structure has changed."
            )

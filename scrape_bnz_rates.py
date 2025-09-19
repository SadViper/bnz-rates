import asyncio
from playwright.async_api import async_playwright

URL = "https://www.bnz.co.nz/personal-banking/home-loans/compare-bnz-home-loan-rates"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Go to BNZ rates page
        await page.goto(URL)

        # Wait for the table
        await page.wait_for_selector("table")

        first_table = await page.query_selector("table")

        # Get all rows
        rows = await first_table.query_selector_all("tr")

        table_data = []
        for row in rows:
            cells = await row.query_selector_all("td, th")
            cell_texts = [await cell.inner_text() for cell in cells]
            table_data.append(cell_texts)

        for cell in range(len(table_data[0])):
            table_data[0][cell] = table_data[0][cell].split('\n')[0]

        print(table_data)

        # Write markdown file
        with open("bnz_rates.md", "w", encoding="utf-8") as f:
            f.write("Public Page for BNZ Rates\n\n")
            if table_data:
                # Header row
                header = table_data[0]
                f.write("| " + " | ".join(header) + " |\n")
                f.write("| " + " | ".join("---" for _ in header) + " |\n")

                # Data rows
                for row in table_data[1:]:
                    f.write("| " + " | ".join(row) + " |\n")

        print("✅ Scraped rates saved to bnz_rates.md")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

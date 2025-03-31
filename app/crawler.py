import asyncio
import re
import logging
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



async def crawling_prices(url: str, xpath: str) -> float:
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
    options.add_argument("--headless=new")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    driver = webdriver.Chrome(options=options)
    price = None

    try:
        driver.get(url)
        row_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        price_text = row_data.text.strip()
        price = price_handler(price_text)
    except Exception as e:
        logging.error(f"Ошибка при выгрузке {url}: {e}")
    finally:
        driver.quit()

    if price is None:
        logging.warning(f"Не удалось получить цену с {url}")
    return price


def price_handler(price_string: str) -> float:
    price_string = price_string.replace(',', '.')
    price_string = re.sub(r'[^0-9.]', '', price_string)

    try:
        return float(price_string)
    except ValueError:
        raise ValueError(f"Невозможно преобразовать строку в число: '{price_string}'")


async def get_average_price(sources):
    results = []
    total_price = 0
    count = 0

    # Вложенная функция для запуска краулера в отдельных потоках
    def run_crawling(source):
        try:
            price = asyncio.run(crawling_prices(source.url, source.xpath))
            return price, source
        except Exception as e:
            logging.error(f"Ошибка при выгрузке {source.url}: {e}")
            return "Сайт недоступен", source

    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, run_crawling, source) for source in sources]

        for future in asyncio.as_completed(futures):
            try:
                price_result, source_item = await future
                if isinstance(price_result, float):
                    total_price += price_result
                    count += 1
                    results.append(
                        f"Цена на сайте {source_item.title}: {price_result} р.")
                else:
                    results.append(
                        f"Цена на сайте {source_item.title}: {price_result}")

            except Exception as e:
                logging.error(f"Ошибка при выгрузке: {e}")

    average_price = total_price / count if count > 0 else 0
    return results, average_price

import re
import json

# Read receipt text from file
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


# Extract all prices from the receipt
prices = re.findall(
    r"\n(\d[\d ]*,\d{2})\nСтоимость",
    text
)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]


# Find all product names
products = re.findall(
    r"\d+\.\n([^\n]+)",
    text
)


# Calculate total amount
total_match = re.search(
    r"ИТОГО:\n([\d ]+,\d{2})",
    text
)
total = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else sum(prices)


# Extract date and time information
date_time_match = re.search(
    r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}",
    text
)
date_time = date_time_match.group() if date_time_match else None


# Find payment method
payment_method = "Bank card" if "Банковская карта" in text else None


# Create a structured output (JSON or formatted text)
receipt = {
    "date_time": date_time,
    "payment_method": payment_method,
    "products": products,
    "prices": prices,
    "total": total
}

print(json.dumps(receipt, indent=4, ensure_ascii=False))
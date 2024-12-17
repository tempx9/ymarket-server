import requests

# Ваши данные
campaign_id = "133861273"  # ID кампании
api_key = "ACMA:NwYSpjAxp01IrnCVNLSLy4sS5m1GygrR3EyaNHJ1:45f09711"

# Заголовки для авторизации
headers = {
    "Api-Key": api_key,
    "Content-Type": "application/json"
}

# Получение списка заказов
orders_url = f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders?fake=true"

response = requests.get(orders_url, headers=headers)

if response.status_code == 200:
    orders = response.json().get("orders", [])
    if not orders:
        print("Нет заказов для обработки.")
    else:
        for order in orders:
            order_id = order.get("id")
            status = order.get("status")

            # Обрабатываем только заказы в статусе PROCESSING
            if status == "PROCESSING":
                print(f"Обрабатывается заказ: {order_id}")

                # Формирование данных для передачи цифрового ключа
                items = order.get("items", [])
                payload_items = []

                for item in items:
                    item_id = item.get("id")
                    if item_id:
                        payload_items.append({
                            "id": item_id,
                            "codes": ["ACTIVATION-CODE-12345"],
                            "activate_till": "2024-12-31",
                            "slip": "Спасибо за покупку! Активируйте ключ до 2024-12-31."
                        })

                # URL для передачи ключа
                deliver_url = f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders/{order_id}/deliverDigitalGoods"

                payload = {"items": payload_items}

                # Отправка POST-запроса
                deliver_response = requests.post(deliver_url, headers=headers, json=payload)

                # Проверка ответа
                if deliver_response.status_code == 200:
                    print(f"Цифровой товар успешно отправлен для заказа {order_id}.")
                else:
                    print(f"Ошибка при отправке ключа для заказа {order_id}: {deliver_response.status_code}")
                    print(deliver_response.text)
else:
    print(f"Ошибка при получении заказов: {response.status_code}")
    print(response.text)
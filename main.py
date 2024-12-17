import requests
import json

def handler(request):
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

    try:
        response = requests.get(orders_url, headers=headers)

        if response.status_code == 200:
            orders = response.json().get("orders", [])
            if not orders:
                return {"statusCode": 200, "body": "Нет заказов для обработки."}
            else:
                output = []
                for order in orders:
                    order_id = order.get("id")
                    status = order.get("status")

                    # Обрабатываем только заказы в статусе PROCESSING
                    if status == "PROCESSING":
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

                        if deliver_response.status_code == 200:
                            output.append(f"Цифровой товар успешно отправлен для заказа {order_id}.")
                        else:
                            output.append(f"Ошибка для заказа {order_id}: {deliver_response.status_code}")
                            output.append(deliver_response.text)
                return {"statusCode": 200, "body": json.dumps(output)}
        else:
            return {"statusCode": response.status_code, "body": response.text}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
from django.core.mail import send_mail


def info_about_order(order, products):
    products_text = str()
    for product in products:
        products_text += f'{product.product.name}, количество {product.amount}, стоимость всего {product.amount * product.product.price}\n'

    info_order = (f'Информация о заказе:\n'
                  f'Заказ №{order.id}, дата оформления - {order.date_ordered}\n'
                  f'{products_text}\n'
                  f'Общая стомисоть заказа - {order.total_cost}\n'
                  f'Информация о доставке:\n'
                  f'Город доставки - {order.city}, адрес доставки - {order.address}\n'
                  f'Способ доставки - {order.shipping_method}\n'
                  f'\n'
                  f'Комментарии к заказу:\n'
                  f'{order.comment}')

    return info_order


def sent_email_to_user_ordering(order, products):
    """отправка письма пользователю после оформления заказа"""

    mail_title = f'Заказ №{order.id} оформлен.'
    mail_text = (f'Здравствуйте, {order.user.first_name} {order.user.last_name}!\n'
                 f'Ваш заказ №{order.id} оформлен.\n'
                 f'{info_about_order(order, products)}\n'
                 f'\n'
                 f'В ближайшее время с вами свяжется менеджер магазина, чтобы уточнить все детали.')

    send_mail(mail_title,
              mail_text,
              'remi_info@remi.ru',
              [order.user.email],
              fail_silently=False)


def sent_email_to_manager_ordering(order, products):
    """отправка письма менеджеру после оформления заказа"""

    mail_title = f'Заказ №{order.id} оформлен.'
    mail_text = (f'Пользователь {order.user} оформил заказ №{order.id}\n'
                 f'{info_about_order(order, products)}\n'
                 f'\n'
                 f'Просим связаться с пользователем {order.user.email} для оформления заказа.')

    send_mail(mail_title,
              mail_text,
              'remi_info@remi.ru',
              ['manager@remi.ru'],
              fail_silently=False)

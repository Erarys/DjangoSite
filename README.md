# Проект GreenApple

GreenApple - Веб сайт сделанный на основе популярных интернет магазинов мебели.
Сайт позволяет пользователям выбрать любимый товар и поместить его в корзинку.
Админы могут добавлять новый товар. Есть возможность редактировать профиль. 


## Установка
1. Клонируйте репозиторий с GitLab
2. Создайте виртуальное окружение
3. Активируйте его `venv\Scripts\activate `
3. Установите зависимости `pip install -r requirements.txt`
4. Активируйте БД `python mysite/manage.py migrate`
5. Сделайте миграцию, чтобы добавить модели `python mysite/manage.py makemigrations`
6. Добавить модели в БД `python mysite/manage.py migrate`
7. Создайте админа `python mysite/manage.py createsuperuser`
Нужно написать имя например admin
Почту можно пропустить и пароль например admin
Согласимся с условиями `y`
8. Запустите сервер `python mysite/manage.py runserver`
![2024-04-15_19-26-38.png](mysite%2Fmedia%2Freadme_image%2F2024-04-15_19-26-38.png)
![2024-04-15_19-27-20.png](mysite%2Fmedia%2Freadme_image%2F2024-04-15_19-27-20.png)
![2024-04-15_19-27-38.png](mysite%2Fmedia%2Freadme_image%2F2024-04-15_19-27-38.png)
![2024-04-15_19-28-36.png](mysite%2Fmedia%2Freadme_image%2F2024-04-15_19-28-36.png)


<span style="color:red">
!!Важно помнить что исходный путь в терминале может оказаться другим. 
В таком случае код выдаст ошибку и с самого начала следите чтобы пути совпадали
</span>


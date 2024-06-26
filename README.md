# ml_team_project_hse

## Описание проекта
Проект по созданию небольшого сервиса в виде Telegramm бота, способного рекомендовать фильмы на основе некоторых признаков пользователя и фильма, истории взаимодействий.

## Gif визуализация работы проекта

![TG bot gif](https://drive.google.com/uc?export=download&id=1ELcW_U7RovNkAysTTQNRn7SHbO16sEAu)

## Что реализовано?
- Сервис на основе Telegram бота
- База данных с пользователями
- Микросервис с API для рекомендации набора фильмов по определенным признакам пользователя или фильма
- Контейнеризация сервисов и объединение в одну сеть

## Что было иследовано?
- Разработка сервиса на Python + парсинг данных из открытых источников
- Модели классического машинного обучения для рекомендательных систем (User2User, Item2Item и Popular подходы, библиотеки: LigthFM, Implicit)
- Модели поиска похожих названий: индекс MinHash LSH на биграммах и TFIDF
- Модели глубинного обучения: классификатор для определния настроения (sentiment) + NER на зафайнтюненой RoBERTa

## План работы над проектом
1. Разведочный анализ данных и первичная аналитика данных, формирование гипотез и списка задач
2. ML часть: построение рекомендательной системы и продуктивизация
3. Разработка архитектуры проекта, создание продуктивнрой среды, обертка в Telegram бота
3. DL часть: построение NLP модели для обработки пользовательсих запросов и рекомендации им фильмы по набору слов, также продуктивизация

## Состав команды проекта:
- Роман Гасымов - куратор проекта
- Дмитрий Булгаков - ML разработчик
- Данила Югай - ML разработчик
- Никита Кошелев - ML разработчик

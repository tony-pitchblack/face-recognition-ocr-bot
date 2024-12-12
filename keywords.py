# -*- coding: utf-8 -*-
import re

keywords = [
 '112',
 'аварийный',
 'авария',
 'авиакатастрофа',
 'автодор',
 'автодороги',
 'Автоматизированная система управления объединенной диспетчерской службы',
 'Автоматизированная система учета потребления ресурсов',
 'автомобильные дороги',
 'Акимов Юрий',
 'Аомосгаз',
 'Аомосгорсвет',
 'Артем Злыднев',
 'АСУ ОДС',
 'АСУПР',
 'асфальт',
 'баллон',
 'Баранов Дмитрий',
 'бензин',
 'бетон',
 'Бирюков',
 'битца',
 'Битцевский',
 'благоустроители',
 'благоустроить',
 'благоустройство',
 'бомбоубежище',
 'Бордюринг',
 'бордюры',
 'Букатов Александр',
 'бюджетники',
 'вакцинация',
 'Валентин Волков',
 'Валентин Самборский',
 'Вартан Авакян',
 'Васильев Владислав',
 'ВДНХ',
 'вертолет',
 'ветер',
 'взнос',
 'взорвался',
 'взрыв',
 'Виталий Видяпин',
 'вице-мэр',
 'Владимир Глухоедов',
 'вода',
 'водные спасатели',
 'водолазы',
 'водопровод',
 'водопроводная станция',
 'водосток',
 'военкомат',
 'поджог',
 'возгорание',
 'воздух',
 'воздушная тревога',
 'восстановление',
 'вторичное использование',
 'выброс в атмосферу',
 'выброс вредных веществ',
 'выброс химикатов',
 'выбросы',
 'выбросы предприятий',
 'вырубка',
 'газ',
 'ГАУ',
 'ГБУ',
 'ГБУ автомобильные дороги',
 'ГБУ МАЦ',
 'ГБУ Озеленение',
 'ГБУ Экспертный центр',
 'гбу-гормост',
 'гбуавтодор',
 'гбуавтодороги',
 'гбуавтомобильныедороги',
 'гбудоринвест',
 'гбумац',
 'гбуэважд',
 'гибель рабочего во время ремонта',
 'ГКУ ДКР',
 'ГКУ ДПО УМЦ ГО И ЧС',
 'ГКУ МАЦ',
 'ГКУ МГПСС',
 'ГКУ ПСЦ',
 'ГКУ УКРИС',
 'ГКУ Энергетика',
 'гкудпоумцгоичс',
 'гкуэнергетика',
 'главное управление',
 'го чс',
 'гор мост',
 'горит',
 'ГОРМОСТ',
 'городская поисково спасательная служба',
 'городские',
 'городские службы',
 'городские указатели',
 'городские часы',
 'городское хозяйство',
 'городской',
 'Городской центр жилищных субсидий',
 'Горячая вода',
 'Государственна жилищная инспекция города Москвы',
 'Государственное бюджетное учреждение Автомобильные дороги',
 'государственное бюджетное учреждение города москвы озеленение',
 'государственное бюджетное учреждение москвы озеленение',
 'государственное бюджетное учреждение озеленение',
 'Государственный природоохранный центр',
 'гочс и пб',
 'ГОЧСИПБ',
 'град',
 'гражданская оборона',
 'громкоговорители',
 'грунт',
 'ГУ',
 'ГУ ИС',
 'ГУИС',
 'ГУП',
 'ГУП СППМ',
 'гупэважд',
 'ГЦЖС',
 'Даев',
 'дезинфекция',
 'дендрологические изыскания',
 'дендроплан',
 'День эколога',
 'Департамент жилищно-коммунального хозяйства',
 'департамент жилищного хозяйства',
 'департамент жкх',
 'департамент кап ремонта',
 'ДЕПАРТАМЕНТ КАПИТАЛЬНОГО РЕМОНТА',
 'Департамент капремонта',
 'департамент коммунального хозяйства',
 'департамент охраны окружающей среды',
 'департамент пиоос',
 'департамент экологии и охраны окружающей среды',
 'департаментжкх',
 'депутат МГД',
 'депутат Мосгордумы',
 'дерево',
 'джкх',
 'джкхиб',
 'джкхибцао',
 'диоксид',
 'дкр',
 'ДКРовской',
 'дождь',
 'дом',
 'дом требуется капремонт',
 'дома',
 'домов',
 'домовые счетчики',
 'домовые указатели',
 'дор инвест',
 'доринвест',
 'Доркина Ирина',
 'дорога',
 'дорожная разметка',
 'дорожно-коммунальная техника',
 'дорожные ямы',
 'дохлые птицы',
 'дохлые утки',
 'ДПИООС',
 'дым',
 'Евгений Балашов',
 'едац',
 'единая',
 'Единый диспетчерский центр',
 'Единый диспетчерско-аналитический центр',
 'единый информационно-расчетный центр',
 'ЕИРЦ',
 'Елена Самсонова',
 'Елисеев Алексей',
 'елочный круговорот',
 'жалоба',
 'железнодорожный',
 'Желтов Сергей',
 'жил.хозяйства',
 'жилищник',
 'жилищники',
 'жилищно-коммунального хозяйства',
 'жилищного хозяйства',
 'жилхозяйства',
 'жилых',
 'ЖКУ',
 'ЖКХ',
 'ЖКХ капремонт',
 'жкхиб',
 'жулищник',
 'загрязнение',
 'загрязнение воды',
 'загрязнение воздуха',
 'задымление',
 'заказник',
 'залитие',
 'зам мэра',
 'замена',
 'замены лифтов',
 'заместитель',
 'заместитель Мэра',
 'заммэра',
 'замуровали',
 'замурованные',
 'замурованный',
 'запах',
 'запах гари',
 'запах канализации',
 'запах сероводорода',
 'затопило',
 'затопление',
 'затопления подвалов',
 'Захарова Полина',
 'защитные сооружения',
 'здание',
 'здания',
 'Зеленоград',
 'Зеленоградводоканал',
 'зеленые стандарты',
 'землетрясение',
 'Зоорассвет',
 'Иванков Игорь',
 'Изутдинов',
 'инспекция',
 'инженерные сооружения',
 'Ирина Кузьма',
 'Ишханян Константин',
 'канализация',
 'Капинус',
 'капитальный',
 'капитальный ремонт дома',
 'капитальный ремонт здания',
 'капремонт',
 'капремонт дома',
 'катастрофа',
 'качели',
 'качество воздуха',
 'квартира',
 'КГУ МАЦ',
 'КГХ',
 'Кескинов Артур',
 'климатический форум',
 'клумбы',
 'Комиссия по чрезвычайным ситуациям и пожарной безопасности',
 'комитет',
 'коммунальные службы',
 'коммунальные тарифы',
 'коммунальный',
 'коммунальный мусор',
 'коммунальщики',
 'коммунальные',
 'коммуникационный коллектор',
 'Комплекс городского Хозяйства',
 'комунальщики',
 'Коробов Константин',
 'КП МЭД',
 'кпмэд',
 'кровля',
 'крыша',
 'Курьяновская',
 'Курьяновские очистные',
 'Кусково',
 'Кутузов Александр',
 'Лезина Елена',
 'Леонид Хрунов',
 'лес',
 'ливень',
 'ливневая канализация',
 'листва',
 'лифт',
 'Люберецкие очистные',
 'люлька',
 'МАЦ',
 'машина',
 'мгпсс',
 'мгупмослифт',
 'медицинские отходы',
 'менять',
 'Местная противовоздушная оборона',
 'метеорит',
 'метро',
 'МЖИ',
 'министерство рф по чрезвычайным ситуациям',
 'Михаил Дмитриев',
 'МКАД',
 'МКД',
 'Молния попала',
 'Молния ударила',
 'Молодежный совет ДЖКХ',
 'Мосводоканал',
 'Мосводопровод',
 'Мосводосток',
 'Мосгаз',
 'Мосгорсвет',
 'МОСЖИЛИНСПЕКЦИЯ',
 'Мосжилниипроект',
 'Мосжкх',
 'Москапремонт',
 'Москва',
 'Москвичи',
 'московская городская поисково-спасательная служба',
 'московская объединенная электро сетевая компания',
 'московская объединенная электросетевая компания',
 'московская объединенная энергетическая компания',
 'московская теплосетевая компания',
 'Московская экорезиденция',
 'московская электросетевая компания',
 'московская энергетическая дирекция',
 'московская энергосбытовая компания',
 'московский',
 'Московский авиационный центр',
 'Московский аналитический центр в сфере городского хозяйства',
 'московский департамент природопользования',
 'московский оператор капремонта',
 'московское управление гражданской защиты',
 'москоллектор',
 'Мослифт',
 'Мосприрода',
 'Мосремонт',
 'моссвет',
 'мост',
 'мостеплосеть',
 'Мосэкомониторинг',
 'мосэнерго',
 'Мосэнергосбыт',
 'моэк',
 'МОЭСК',
 'мсгормост',
 'мусор',
 'мусорная реформа',
 'мусорный',
 'мусоровоз',
 'мусоросжигательный завод',
 'МЧС',
 'МЭД',
 'мэр',
 'мэрия',
 'набережная',
 'набережные',
 'навигационные указатели',
 'навигация',
 'Наводнение',
 'Наталия Ремезова',
 'натуральное обследование территории',
 'неделя городского хозяйства',
 'неделя жкх',
 'нефтеперерабатывающий завод',
 'нефтепродукты',
 'нефтяные',
 'нечем дышать',
 'Николай Капинус',
 'Николай Кудрявцев',
 'обвал',
 'обвалы',
 'обесточен',
 'обесточены',
 'обращение с отходами',
 'обрушения лесов при ремонте фасада',
 'Обрушилась',
 'обрушился асфальт',
 'Обрушился фасад',
 'Обслуживание приборов учета',
 'обустраивать',
 'обустроить',
 'общедомовой',
 'общественные туалеты',
 'объединенная диспетчерская служба',
 'Объединенная энергетическая компания',
 'объект дорожного хозяйства',
 'огнеборцы',
 'ОДУУ',
 'озеленение',
 'Оползень',
 'особо охраняемая природная территория',
 'отключение',
 'отопительный сезон',
 'отопление',
 'отслоения краски после ремонта фасада',
 'отходы',
 'охрана окружающей среды',
 'очистные сооружения',
 'ОЭК',
 'оэковцы',
 'Павел Скородумов',
 'памятник',
 'Памятник садово-паркового искусства',
 'парк',
 'парк победы',
 'Паспорт территории',
 'Первомайское производственное управление',
 'перекладывать',
 'Переплата',
 'песчаная буря',
 'Петр Бирюков',
 'пешеходная',
 'пешеходная доступность',
 'ПиООС',
 'План капремонта',
 'плата за капремонт',
 'плачевное состояние дома',
 'плитка',
 'повредил',
 'погиб',
 'подвал',
 'поддержка',
 'Поджег',
 'Подтопление',
 'подъезд',
 'пожар',
 'пожар после ремонта электрики',
 'Пожарно спасательный центр',
 'Пожарно-спасательный центр',
 'пожарные',
 'пожаро спасательный центр',
 'поисково спасательная станция',
 'Покровское',
 'Покровское-стрешнево',
 'поливомоечная машина',
 'полигон отходов',
 'полотно',
 'Пономаренко Александр',
 'посадка деревьев',
 'посадка кустарников',
 'последствия',
 'пострадали',
 'пострадало',
 'потоп',
 'потопление',
 'префектура',
 'природа',
 'природно-исторический парк',
 'природоохранная',
 'природоохранное законодательство',
 'природоохранный центр',
 'природопользование',
 'приют',
 'провал',
 'провал грунта',
 'проверка',
 'проверка автомобильные дороги',
 'проверка жилищник',
 'проверка территории',
 'программа озеленения города',
 'проезжей части',
 'происшествие',
 'промзона',
 'прорыв',
 'прорыв магистралей после ремонта',
 'проседание',
 'простой лифтов',
 'протестная акция',
 'Протечка',
 'птица-синица',
 'Пылевое облако',
 'пыль',
 'пыльная буря',
 'пыльное облако',
 'пятна',
 'пятна бензина',
 'работы',
 'рабочий',
 'радиация',
 'раздельный сбор',
 'раздельный сбор мусора',
 'разметка',
 'Разрушение',
 'Разрушение дороги',
 'Разрушение дорожного покрытия',
 'разумное потребление',
 'реагенты',
 'регион',
 'регоператор',
 'режим готовности',
 'режим повышенной готовности',
 'река',
 'реконструкция и капитальный ремонт',
 'Ремезова',
 'ремонт',
 'ремонт водостока',
 'ремонт кровли',
 'ремонт подъездов',
 'ремонт электрики',
 'реновация',
 'реставрация',
 'реформа',
 'речка',
 'РМ 10',
 'РМ10',
 'Россети',
 'россети московский регион',
 'россети мр',
 'Российская энергетическая неделя',
 'российской федерации',
 'Ротмистров Яков',
 'Рябов',
 'Самборский',
 'Самсонова',
 'свалка',
 'свалочный газ',
 'Святенко Кирилл',
 'Семутникова Евгения',
 'Сильный град',
 'Сильный ливень',
 'сирена',
 'система навигации',
 'система оповещения',
 'Система-112',
 'слив',
 'сливается',
 'сливаются',
 'службы',
 'снег',
 'снежный',
 'собиратор',
 'Собянин',
 'собянинская',
 'Собянинские',
 'совет молодых специалистов мосэнерго',
 'Соловьев Александр',
 'социальная',
 'соцразвития',
 'спасатели',
 'спасли',
 'Стихийное бедствие',
 'стихия',
 'столица',
 'столичные службы',
 'столичный',
 'столичный департамент природопользования',
 'столичный оператор капитального ремонта',
 'столичный оператор капремонта',
 'столичный фонд капремонта',
 'стояков',
 'Стрешнево',
 'Субсидии',
 'ТБО',
 'территория',
 'Техногенный',
 'Титов Владимир',
 'ТКО',
 'токсичные',
 'тоннель',
 'топливно-энергетического комплекса',
 'топливно-энергетического хозяйства',
 'торфяник',
 'торфянник',
 'транспортная доступность',
 'труб',
 'тэх',
 'убирать',
 'Уборка',
 'угарный газ',
 'узел учета',
 'УКРИС',
 'умцгочс',
 'умцгочсипб',
 'упал',
 'упала',
 'управа',
 'управление по обеспечению мероприятий гражданской защиты',
 'управление топливно-энергетического хозяйства',
 'управляющая компания',
 'ураган',
 'установить',
 'утечка',
 'Утилизация ТБО',
 'учебно методический центр по го и чс',
 'учебно методический центр по гражданской обороне и чрезвычайным ситуациям',
 'Фасад обрушился',
 'фасадная плитка обрушилась',
 'фауна',
 'фгбу',
 'фгку',
 'ФКР',
 'фонд капитального ремонта',
 'фонд капремонта',
 'фонтан',
 'хозяйство',
 'Хрунов',
 'цветники',
 'цветы',
 'центр координации',
 'центр координации гу ис',
 'центр координации деятельности государственных учреждений инженерных служб',
 'центр по выполнению работ и оказанию услуг природоохранного назначения',
 'Центр управления комплекса городского хозяйства',
 'ЦУ КГХ',
 'Час земли',
 'Чермянка',
 'Чиненков алексей',
 'чистить',
 'Чистов Сергей',
 'чп',
 'Чрезвычайная ситуация',
 'Чрезвычайное',
 'ЧС',
 'Штормовой ветер',
 'шум стройки',
 'ЭВАЖД',
 'экологическая безопасность',
 'экологические тропы',
 'экологический рейтинг',
 'экология',
 'Эколого-просветительский центр',
 'Экомарафон',
 'экотехнопарк',
 'экотехпром',
 'экотропы',
 'Экоцентр',
 'Экспертавтодор',
 'эксплуатация',
 'Электрозаводская',
 'Электронная паспортизация',
 'электростанция',
 'Энергетика',
 'энергетическая система',
 'ЭС',
 'Юлия Чижова',
 'Юрий Насимович',
 'Яворский Владимир',
 'ядерный',
 'Яков Ротмистров',
 'Яуза'
]


# Приводим все слова к верхнему регистру
keywords_up = [word.upper() for word in keywords]
# print(keywords_up)

exclude_words = [
    "реновация",
    "«Здоровая Москва»",
    "Москомархитектура",
    "Музей транспорта",
    "Велогонка",
    "Депстрой",
    "Бочкарев",
    "Росгидромет",
    "НАК",
    "ФСБ",
    "Путин",
    "Роспотребнадзор",
    "Дептранс",
    "Ракова",
    "ЕМИАС",
    "Песков",
    "Росавиация",
    "Ликсутов",
    "Ефимов",
    "Немерюк",
    "Соцблок",
    "Сергунина",
]

exclude_words_up = [word.upper() for word in exclude_words]


def find_keywords(keywords, text, exclude_words=None):
    if exclude_words is None:
        exclude_words = []

    # Преобразуем текст и ключевые слова в нижний регистр для регистронезависимого сравнения
    text = text.lower()
    keywords = [keyword.lower() for keyword in keywords]
    exclude_words = [word.lower() for word in exclude_words]

    for keyword in keywords:
        pattern = re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)
        match = re.search(pattern, text)
        if match:
            matched_word = match.group(0)
            print("Ф-я ключей, ключ слово: ", matched_word)

            exc_detected = False
            for exclude_word in exclude_words:
                pattern_exc = re.compile(r"\b" + re.escape(exclude_word) + r"\b", re.IGNORECASE)
                match_exc = re.search(pattern_exc, text)
                if match_exc:
                    matched_exc_word = match_exc.group(0)
                    print("Ф-я ключей, исключение: ", matched_exc_word)

                    # Если есть совпадение для исключения, обновляем matched_word
                    exc_detected = True

            if not exc_detected:
                return matched_word

    return None


def check_symbols(text):
    pattern = r'[<>*=_\]&@]'
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False
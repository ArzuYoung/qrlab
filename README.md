# Лабораторная работа QR и штрих коды

**QR-код** (англ. quickresponse — быстрый отклик) — матричный код, разработанный и 
представленный японской компанией "Denso-Wave" в 1994 году. QR-код является двумерным 
представлением обычного штрихкода, помещаемого практически на любую производимую продукцию.
QR символизирует мгновенный доступ к информации, хранимой в коде. Закодированная информация
может состоять из данных любого типа (например, двоичных, буквенно-цифровых символов или 
символов Кандзи(китайско-японские иероглифы)).

## Количество символов, которое можно закодировать

**Максимальное число символов**, которое можно внести в QR-код (версия 40,
177×177 модулей):

- Цифры — 7089; 
- Цифры и буквы латинского алфавита — 4296;
- Иероглифы — 1817;
- Двоичный код — 2953 байта (следовательно, около 2953 букв кириллицы в кодировке 
windows-1251 или 1450 букв кириллицы в utf-8).

Если выражать размеры в битах — 10 бит на 3 цифры и 11 бит на 2 алфавитно-цифровых символа.

В данной работе я использовала **QR код 3 версии** (29×29 модулей), которым можно закодировать:

- Цифры — 127; 
- Цифры и буквы латинского алфавита — 77;
- Иероглифы — 32;
- Двоичный код — 53 байта.

## Уровни коррекции ошибок

- L-уровень коррекции. При его использовании можно восстановить 7% информации.
- М-уровень коррекции. Восстановление 15% информации.
- О-уровень коррекции. Восстановление 25% информации.
- Н-уровень коррекции. Восстановление 30% информации.

Для исправления ошибок используется алгоритм Рида-Соломона.
Данный алгоритм используется как при создании QR-кода, так и при его дешифрации.

## Преимущества QR-кода

- Больше данных, чем в штрих-коде
- Меньше ошибок
- Легко считывать
- Легко печатать
- Повышенная надежность

## Недостатки QR-кода
- Необходимо быть уверенным, что адресат сможет его прочесть;
- Вмещает в себя относительно мало информации, например, закодировать целую книгу в 
один стандартный QR-код не представляется возможным;
- QR-код является общедоступной технологией, следовательно, нельзя хранить важную 
информацию в виде QR-кода, так как код не предоставляет соответствующий уровень защиты 
информации.

## Анализ стойкости

В процессе анализа стойкости я проводила различные преобразования над изображениями 
кодов:

- увеличивала яркость изображения:

    <img src="/brightness/done_qr.png" height="200"> пример qr кода, который еще считывается

    <img src="/brightness/none_qr.png" height="200"> пример qr кода, который уже не считывается

- поворачивала код на различные углы:

    <img src="/rotate/done_10_qr.png" height="200"> пример qr кода, который еще считывается

    <img src="/rotate/none_15_qr.png" height="200"> пример qr кода, который уже не считывается

    Предельное значение поворота 15 градусов (не включая это значение) от прямого угла
(т.е. +-15 градусов от поворота на 0, 90, 180, 270)

- отзеркаливала:

    <img src="/flip/vertical_flipqr.png" height="200"> по вертикали

    <img src="/flip/horizontal_flip_qr.png" height="200"> и горизонтали

    В результате преобразований код декодировался в обоих случаях правильно

- размывала:

    <img src="/blur/done_qr.png" height="200"> пример qr кода, который еще считывается

    <img src="/blur/none_qr.png" height="200"> пример qr кода, который уже не считывается

    При ядре размытия в 11 пикселей (для изображения 370×370) код перестает считываться

- вырезала относительно центра:

    <img src="/center_crop/done_qr.png" height="200"> пример qr кода, который еще считывается

    <img src="/center_crop/none_qr.png" height="200"> пример qr кода, который уже не считывается

- закрашивала куски кода в разных углах:

    <img src="/side_crop/done_left_down_qr.png" height="200"> пример qr кода, который еще считывается

    <img src="/side_crop/none_left_down_qr.png" height="200"> пример qr кода, который уже не считывается


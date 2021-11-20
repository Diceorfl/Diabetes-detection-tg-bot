# Diabetes-detection-tg-bot
### A Recommendation System For Diabetes Detection And Treatment  
Данная система помогает определить наличие или отсутствие сахарного диабета у пациент(а/ов), указывает его тип при наличии и даёт рекомендации по лечению и профилактике.  
  
### ОСНОВНЫЕ КОМАНДЫ:  
**/start**-вызывает описание бота.  
**/help**-бот присылает файл с инструкцией по своей эксплуатации.  
**/1type**-присылает рекомендации по лечению и профилактике пациента с первым типом сахарного диабета.  
**/2type**- присылает рекомендации по лечению и профилактике пациента со вторым типом сахарного диабета.  
**/examplefiles**-присылает примеры, как должны выглядеть ваши файлы в формате csv и json для загрузки в бота.  
  
### КАК ЗАГРУЖАТЬ ДАННЫЕ О ПАЦИЕНТАХ:  
1. Это можно сделать в формате обычного текстового сообщения. Удобно, если пациент один или не очень много.  
2. Если пациентов много, то можно отправить боту файл в формате csv или json. Бот вернет файл в том же формате, который вы ему отправили. В файле result, к данным о пациентах будет добавлен признак “Outcome”, в котором будет содержаться информация о сахарном диабете для каждого из пациентов.  
  
### КАКИЕ ДАННЫЕ УКАЗЫВАТЬ ДЛЯ ПАЦИЕНТОВ И ЧТО ОНИ ОЗНАЧАЮТ:  
**HbA1C**- гликированный гемоглобин, специфическое соединение гемоглобина эритроцитов с глюкозой, концентрация которого отражает среднее содержание глюкозы в крови за период около трех месяцев. Единицы измерения: % (процент). Более подробная информация: https://helix.ru/kb/item/06-014  
**UBP**-Верхнее артериальное давление. Более подробная информация: https://beurer-belarus.by/reviews/poleznaya-informatsiya/verkhnee-i-nizhnee-davlenie-chto-eto/  
**LBP**-Нижнее артериальное давление.  Более подробная информация: https://beurer-belarus.by/reviews/poleznaya-informatsiya/verkhnee-i-nizhnee-davlenie-chto-eto/  
**BMI**-Индекс массы тела. Более подробная информация: https://ru.wikipedia.org/wiki/%D0%98%D0%BD%D0%B4%D0%B5%D0%BA%D1%81_%D0%BC%D0%B0%D1%81%D1%81%D1%8B_%D1%82%D0%B5%D0%BB%D0%B0  
**AGE**- Возраст пацианта.  
**Glycemia**- уровень гликемии натощак. Более подробная информация: https://ru.wikipedia.org/wiki/%D0%93%D0%BB%D0%B8%D0%BA%D0%B5%D0%BC%D0%B8%D1%8F   
**Gender**- пол пациента, где 1-мужской, 0-женский.  
**Insulin**-уровень инсулина натощак. Более подробная информация: https://avklinik.ru/stati/endokrinolog/tri-glavnyix-analiza-na-diabet.html  
  
![image](https://user-images.githubusercontent.com/63186837/142740723-a69098ec-cb23-463a-bc02-cd3758fe03fd.png)

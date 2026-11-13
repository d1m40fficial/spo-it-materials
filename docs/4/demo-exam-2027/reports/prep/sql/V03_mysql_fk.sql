USE `dkip2027_v03`;

ALTER TABLE `Цены`
  ADD CONSTRAINT `fk_ceny_resurs`
  FOREIGN KEY (`КодРесурса`) REFERENCES `Номенклатура` (`КодРесурса`);

ALTER TABLE `Спецификации`
  ADD CONSTRAINT `fk_spec_izdelie`
  FOREIGN KEY (`КодИзделия`) REFERENCES `Номенклатура` (`КодРесурса`);

ALTER TABLE `Спецификации`
  ADD CONSTRAINT `fk_spec_izgotovitel`
  FOREIGN KEY (`КодИзготовителя`) REFERENCES `Заказчики` (`КодЗаказчика`);

ALTER TABLE `СоставСпецификации`
  ADD CONSTRAINT `fk_sostav_spec`
  FOREIGN KEY (`КодСпецификации`) REFERENCES `Спецификации` (`КодСпецификации`);

ALTER TABLE `СоставСпецификации`
  ADD CONSTRAINT `fk_sostav_resurs`
  FOREIGN KEY (`КодРесурса`) REFERENCES `Номенклатура` (`КодРесурса`);

ALTER TABLE `ЗаказыПокупателя`
  ADD CONSTRAINT `fk_zakaz_customer`
  FOREIGN KEY (`КодЗаказчика`) REFERENCES `Заказчики` (`КодЗаказчика`);

ALTER TABLE `ЗаказыПокупателя`
  ADD CONSTRAINT `fk_zakaz_executor`
  FOREIGN KEY (`КодИсполнителя`) REFERENCES `Заказчики` (`КодЗаказчика`);

ALTER TABLE `СтрокиЗаказа`
  ADD CONSTRAINT `fk_stroka_zakaz`
  FOREIGN KEY (`КодЗаказа`) REFERENCES `ЗаказыПокупателя` (`КодЗаказа`);

ALTER TABLE `СтрокиЗаказа`
  ADD CONSTRAINT `fk_stroka_tovar`
  FOREIGN KEY (`КодТовара`) REFERENCES `Номенклатура` (`КодРесурса`);

ALTER TABLE `ПродукцияКВыпуску`
  ADD CONSTRAINT `fk_produkciya_proizv`
  FOREIGN KEY (`КодПроизводственногоЗаказа`) REFERENCES `ЗаказыНаПроизводство` (`КодПроизводственногоЗаказа`);

ALTER TABLE `ПродукцияКВыпуску`
  ADD CONSTRAINT `fk_produkciya_tovar`
  FOREIGN KEY (`КодТовара`) REFERENCES `Номенклатура` (`КодРесурса`);

ALTER TABLE `РесурсыПроизводства`
  ADD CONSTRAINT `fk_resursy_proizv`
  FOREIGN KEY (`КодПроизводственногоЗаказа`) REFERENCES `ЗаказыНаПроизводство` (`КодПроизводственногоЗаказа`);

ALTER TABLE `РесурсыПроизводства`
  ADD CONSTRAINT `fk_resursy_resurs`
  FOREIGN KEY (`КодРесурса`) REFERENCES `Номенклатура` (`КодРесурса`);

ALTER TABLE `Заметки`
  ADD CONSTRAINT `fk_zametki_polzovatel`
  FOREIGN KEY (`КодПользователя`) REFERENCES `Пользователи` (`КодПользователя`);

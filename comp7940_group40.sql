--phphMyadmin



SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE `comp7940_group40` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `comp7940_group40`;

CREATE TABLE `hiking` (
  `id` int(11) NOT NULL,
  `District` varchar(128) NOT NULL,
  `Trails` varchar(128) NOT NULL,
  `Path` varchar(256) NOT NULL,
  `Desination_Transport` varchar(128) NOT NULL,
  `Leaving_Transport`varchar(128) NOT NULL,
  `RequireTime_Hours` FLOAT(10,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hikecomment` (
  `id` int(11) NOT NULL,
  `hikingid` int(11) NOT NULL,
  `comment` text NOT NULL,
  `userid` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `hiking` (`id`, `District`,`Trails`, `Path`, `Desination_Transport`, `Leaving_Transport`, `RequireTime_Hours`) VALUES
(1, "九龍","獅子山", "在慈雲山北巴士總站後方的梯級開步，沿水泥路走經修建妥善的石級抵達沙田坳。在馬路轉角處見麥理浩徑的告示牌，循徑上行，攀升一段後路徑漸見平緩，及後遇上分支直走（左路可下走至沙田坳村）。
在一山坳處，隨指示牌登上獅子山再往前走，輕攀大石可到達獅位置，頭眺望九龍半島。從獅子頭側的明顯小徑接回麥理浩徑，不久便到達回歸紀念亭。由此續走至畢架山發射站的馬路，沿徑續走至涼亭。及後離開麥理浩徑左走，在支路再左轉下走至龍翔道，最後橫越公路便可下走抵蘇屋村。", "小巴 37A", "巴士 2/112 號", 4),
(2, "香港島","龍脊", "路線的起點在土地灣。下車便會看見港島徑的地圖資料牌。沿徑而上，路線明確。直至分支處的涼亭，需右轉登山（左方路徑可通往龍脊後段）。到達平台後，石澳與大頭洲等地盡收眼底。在木椅後登山片刻，可到達一個更為開揚更廣闊石台。此處鮮有遊人到達，實為極佳的休息處。隨後返回木椅處，縱走龍脊線上，先後賞白筆山、大浪灣景致。及後輕降山徑至分岔口，右方踏上平緩徑（左方可返回土地灣），其後右轉接上水泥路（左方可走至石澳道），續下降山徑至屋村，再往大浪灣完成行程（經過士多可往停車場乘車離去）。", "巴士 9 號", "巴士 9 號", 3),
(3, "新界","川龍", "在小巴站下車後，往川龍的農地走，之後轉入林中小徑。走過了山邊小屋，便到達引水道 (即緩跑徑)。在引水道左轉，走至扶輪亭，在右方豎立著指示牌的水泥梯級下走至荃錦公路畢(可在此乘車或走約10分鐘經至愉景新城)。", "小巴 80 號", "小巴 80 號", 1.5),
(4, "新界", "蒲台島", "在蒲台碼頭下船後左走，先略過「第三段」指示牌，直往天后廟。而天后廟旁就是「響螺石」。返回「第三段」指示牌，靠左方設有綠色欄杆的小徑上山。繞過電力站路段漸開揚，沿空白的指示牌往上走，時而傾斜，時而茂密，最後接回蒲台島郊遊徑。沿徑直走至涼亭小休（右沿郊遊徑經棺材石往碼頭）。及後再緩步而下，見支路經「靈龜上山」、「僧人石」等名勝直往燈塔（右沿郊遊徑可往碼頭。續沿徑而走便見「佛手巖」，接回剛才支路，踏海岸小徑，往觀「摩崖石刻」返回碼頭。", "街渡(星期二、四、六、日及公眾假期)", "街渡(星期二、四、六、日及公眾假期)", 2.5),
(5, "新界", "大東山", "在南山的牌樓上走至直昇機坪，輕降後便開始登山。沿徑一路攀升，便可到達雙東坳。再往前走，經過黃龍坑郊遊徑的地圖指示牌，便會到達大東山的爛頭營。從石屋間的小徑繼續前進，輕攀山坳，再走過一段較平坦的路段，便要往下走。最後隨著石級下降至伯公坳完成旅程。", "巴士 1/2/3M/4 號", "巴士 11/23 號", 3.5);

ALTER TABLE `hiking`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `hiking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `hikecomment`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `hikecomment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
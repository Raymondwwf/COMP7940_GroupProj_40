CREATE DATABASE `comp7940` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `comp7940`;

DROP TABLE IF EXISTS `hiking`;
CREATE TABLE `hiking` (
  `id` int(11) NOT NULL,
  `District` varchar(128) NOT NULL,
  `Trails` varchar(128) NOT NULL,
  `Path` text NOT NULL,
  `Desination_Transport` varchar(128) NOT NULL,
  `Leaving_Transport`varchar(128) NOT NULL,
  `RequireTime_Hours` FLOAT(10,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `hikecomment`;
CREATE TABLE `hikecomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `hikingid` int(11) NOT NULL,
  `comment` text NOT NULL,
  `userid` int NOT NULL,
  `photo` text NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `movieshare`;
CREATE TABLE `movieshare` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `moviename` text NOT NULL,
  `moviesharing` text NOT NULL,
  `userid` int NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `hiking` (`id`, `District`,`Trails`, `Path`, `Desination_Transport`, `Leaving_Transport`, `RequireTime_Hours`) VALUES
(1, "kw","Lion Rock", "Starting from the stairs behind the Tsz Wan Shan North bus station, follow the road and the stone grade then reach to the Shatin Col. The Maclehose Trailnotice board can be seen in the corner of the road, follow the trail and then meet the branch and go straight(you can take the left road and go down to Sha Tin Au Village).
Follow the Lion Rock notice board and keep straight on a small mountain. After climbing the boulder gently to reach the Lion, you may enjoy the view of Kowloon Peninsula. For leaving, take the Maclehose Trail from the Lion's Head side, soon will arrive the handover memroial pavilion. From here, continue to the road to the Beacon Hill launch station, and continue along the path to the pavilion. Then leave Maclehose Trail and go left", "Minibus 37A", "Bus no. 2/112 ", 4),
(2, "hk","Dragon Back", "Starting from Land Bay. After get off the bus, the map information board of HK Island Trail will be seen.Follow the path up to the pavilion at the branch, turn right to climb the mountain(the path on the left leads to the rear section of the Dragon's Back)。After reaching the platform, you can have a view of Shek O and Da Tau Chau. Behind the wood chair we can keep hiking for a while, then reach a more open and wider stone platform. Go back to the wooden chair, Walk along the Dragon Back line and enjoy the view of Baibi Mountain. Then go down to the trail to the branch,Take the path on the right(return to Land Bay on the left), then turn right onto the road(take left to Shek O Road), keep go down in the tail to the estate, Then go to Bisg Wave Bay to complete the trip(you can take car to the parking lot after passing through the store).", "Bus no. 9", "Bus no. 9", 3),
(3, "nt","Chuen Lung", "After get off at the minibus stop, go to the farmland of Chuen Lung, and then turn into the forest trail. After passing the mountain hut, you will reach the aquenduct(that is, the jogging track), turn left at the aqueduct and walk to the Rotary Pavilion, Walk down the concrete steps with a sign on the right to the end of the Tsuen Jin Highway(you can take a bus here or walk for about 10 minutes to D.PARK)。", "Minibus no. 80", "Minibus no. 80", 1.5),
(4, "nt", "Po Toi", "Turn left after disembarking at Po Toi Pier, skip the Third Stage sign, Go Straight to Tin Hau Temple. And next to the Tin Hau Temple is the Sound Loose Stone. Return to the Third Stage' sign, the trail with green railings on the left goes up the hill. The road that bypasses the power station gradually opens up and walks up along the blank sign, Finally, return to Po Toi Country Trail. Go staight to the pavilion for a short break(right along the country tail through the coffin stone to the pier). And then slow go down, we will see the branch road and go straight to the lighthouse via famous places such as Tortoise Climbing up the Mountain and Monk Stone. Follow the country tail on the right to the pier Continue to walk along the trail and you will see the Bergamot rock, take the slip road just now, walk on the path, go to watch the Cliff Rock Carving and return to the pier.", "Kaito(Ferry)(Tuesday, Thursday, Saturday, Sunday and public holidays)", "Kaito(Ferry)(Tuesday, Thursday, Saturday, Sunday and public holidays)", 2.5),
(5, "nt", "Sunset Peak", "Walk to the helipad on the archway of Nanshan Mountain, and start climbing after a light descent. Climb all the way up the trail to Shuangdong Col. Go further, pass the map sign of the Huanglongkeng Countryside Trail, and you will reach the Bad Head Camp in Sunset Peak. Continue on the path between the stone houses, lightly climb the mountain pass, and then walk down a relatively flat section of the road. Finally, the journey is completed as the stone level descends to Bogong Au.", "Bus no. 1/2/3M/4", "Bus no. 11/23", 3.5);

ALTER TABLE `hiking`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `hiking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

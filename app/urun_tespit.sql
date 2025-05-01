-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 01 May 2025, 15:06:22
-- Sunucu sürümü: 10.4.32-MariaDB
-- PHP Sürümü: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `urun_tespit`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `deformasyon_kayitlari`
--

CREATE TABLE `deformasyon_kayitlari` (
  `id` int(11) NOT NULL,
  `deformasyon_orani` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `deformasyon_kayitlari`
--

INSERT INTO `deformasyon_kayitlari` (`id`, `deformasyon_orani`, `created_at`) VALUES
(294, '0.0', '2025-04-27 08:27:36'),
(295, '0.4964192708333333', '2025-04-27 08:27:46'),
(296, '0.2682291666666667', '2025-04-27 08:27:57'),
(297, '0.5162760416666667', '2025-04-27 08:28:07'),
(298, '0.2884114583333333', '2025-04-27 08:53:10'),
(299, '0.5126953125', '2025-04-27 08:53:20'),
(300, '0.4654947916666667', '2025-04-27 08:53:30'),
(301, '4.499674479166667', '2025-04-27 08:53:40'),
(302, '1.0514322916666667', '2025-04-27 09:05:34'),
(303, '0.51171875', '2025-04-27 09:26:36'),
(304, '0.5563151041666666', '2025-04-27 09:26:46'),
(305, '3.0393880208333335', '2025-04-27 09:26:56'),
(306, '0.9358723958333334', '2025-04-27 09:27:07'),
(307, '2.4303385416666665', '2025-04-27 09:27:17'),
(308, '1.501953125', '2025-04-27 09:27:27'),
(309, '1.7174479166666665', '2025-04-27 09:27:37'),
(310, '3.212239583333333', '2025-04-27 09:27:47'),
(311, '3.692708333333333', '2025-04-27 09:27:57'),
(312, '0.7929687499999999', '2025-04-27 09:28:07'),
(313, '2.9674479166666665', '2025-04-27 09:28:17'),
(314, '0.6497395833333334', '2025-04-27 09:55:44'),
(315, '0.9527994791666666', '2025-04-27 09:55:54'),
(316, '0.587890625', '2025-04-27 09:56:07'),
(317, '0.0', '2025-04-27 09:56:17'),
(318, '0.5208333333333333', '2025-04-27 09:56:27'),
(319, '0.9876302083333334', '2025-04-27 12:16:03'),
(320, '1.4075520833333335', '2025-04-27 12:16:13'),
(321, '0.0', '2025-04-27 12:16:23'),
(322, '0.9807942708333333', '2025-05-01 16:04:23'),
(323, '0.4225260416666667', '2025-05-01 16:04:33'),
(324, '0.0', '2025-05-01 16:04:43'),
(325, '0.71875', '2025-05-01 16:04:53'),
(326, '0.0', '2025-05-01 16:05:03'),
(327, '0.0', '2025-05-01 16:05:13');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `urun`
--

CREATE TABLE `urun` (
  `id` int(11) NOT NULL,
  `firma_adi` varchar(255) NOT NULL,
  `urun_adi` varchar(255) NOT NULL,
  `bolge` varchar(100) DEFAULT NULL,
  `stok_seviyesi` int(11) DEFAULT 0,
  `satis_fiyati` decimal(10,2) DEFAULT NULL,
  `indirim` int(11) NOT NULL,
  `rakip_fiyati` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `deformasyon_kayitlari`
--
ALTER TABLE `deformasyon_kayitlari`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `urun`
--
ALTER TABLE `urun`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `deformasyon_kayitlari`
--
ALTER TABLE `deformasyon_kayitlari`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=328;

--
-- Tablo için AUTO_INCREMENT değeri `urun`
--
ALTER TABLE `urun`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

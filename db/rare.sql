CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` TEXT NOT NULL,
  `last_name` TEXT NOT NULL,
  `display_name` TEXT NOT NULL,
  `email` TEXT NOT NULL,
  `created_on` DATETIME
);

CREATE TABLE `categories` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL
);

CREATE TABLE `posts` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `category_id` INTEGER,
  `publication_date` DATETIME NOT NULL,
  `user_id` INTEGER NOT NULL,
  `header_img_url` TEXT NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
);

CREATE TABLE `tags` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL
);

CREATE TABLE `postTags` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `post_id` INTEGER NOT NULL,
  `tag_id` INTEGER NOT NULL, 
  FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
);

CREATE TABLE `comments` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `post_id` INTEGER,
  `subject` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `created_on` DATETIME NOT NULL,
  `is_edited` BOOLEAN,
  FOREIGN KEY (`post_id`) REFERENCES `posts` ('id')
);

ALTER TABLE users
  ADD `created_on` DATETIME;

SELECT * from tags

PRAGMA table_info(comments);

ALTER TABLE users
RENAME COLUMN new_column_name TO created_on;

INSERT INTO `tags` VALUES (null, "tag1");
INSERT INTO `tags` VALUES (null, "tag2");
INSERT INTO `tags` VALUES (null, "tag3");

INSERT INTO `categories` VALUES (null, "categories1");
INSERT INTO `categories` VALUES (null, "categories2");

INSERT INTO `users` VALUES (null, 'Jonathan', 'north', "Jon", "gaikwad@ddd.com", "");
INSERT INTO `users` VALUES (null, 'Phonesalo', 'south', "Phone", "nikhil@ddd.com", "");

INSERT INTO `postTags` VALUES (null, 1, 1);
INSERT INTO `postTags` VALUES (null, 1, 2);
INSERT INTO `postTags` VALUES (null, 1, 3);
INSERT INTO `postTags` VALUES (null, 2, 1);
INSERT INTO `postTags` VALUES (null, 2, 2);
INSERT INTO `postTags` VALUES (null, 2, 3);

INSERT INTO `posts` VALUES (null, "Mo Silvera", "201 Created St tag1", 1, 'jan 1 2009 13:22:15', 1, "imageURL");
INSERT INTO `posts` VALUES (null, "Bryan Nilsen", "500 Internal Error Blvd", 1, 'jan 1 2010 13:22:15', 1, "imageURL");
INSERT INTO `posts` VALUES (null, "Jenna Solis", "301 Redirect Ave", 2, 'jan 1 2011 13:22:15', 2, "imageURL");
INSERT INTO `posts` VALUES (null, "Emily Lemmon", "454 Mulberry Way", 2, 'jan 1 2012 13:22:15', 2, "imageURL");

INSERT INTO `comments` VALUES (null, 1, "Snickers", "Recreation", "jan 1 2019 13:22:15", true);
INSERT INTO `comments` VALUES (null, 2, "Jax", "Treatment", "jan 1 2020 13:22:15", false);
INSERT INTO `comments` VALUES (null, 3, "Falafel", "Treatment", "jan 1 2021 13:22:15", true);
INSERT INTO `comments` VALUES (null, 4, "Doodles", "Kennel", "jan 1 2022 13:22:15", false);

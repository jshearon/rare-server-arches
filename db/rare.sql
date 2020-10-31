CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` TEXT NOT NULL,
  `last_name` TEXT NOT NULL,
  `display_name` TEXT NOT NULL,
  `email` TEXT NOT NULL
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
  `is_edited` BOOLEAN DEFAULT(FALSE),
  FOREIGN KEY (`post_id`) REFERENCES `posts` ('id')
);

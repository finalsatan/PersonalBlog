-- schema.sql

use personalblog;

create table posts (
    `id` varchar(50) not null,
    `post_type` varchar(50) not null,
    `post_name` varchar(50) not null,
    `post_content` mediumtext not null,
    `post_link` varchar(200) not null,
    `post_time` real not null,
    key `idx_post_time` (`post_time`),
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table apps (
    `id` varchar(50) not null,
    `app_name` varchar(50) not null,
    `app_link` varchar(200) not null,
    `app_time` real not null,
    key `idx_app_time` (`app_time`),
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;


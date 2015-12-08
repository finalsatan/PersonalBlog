-- schema.sql

drop database if exists personalblog;

create database personalblog;

use personalblog;

grant select, insert, update, delete on personalblog.* to 'ubuntu'@'localhost' identified by 'ubuntu';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table posts (
    `id` varchar(50) not null,
    `post_type` varchar(50) not null,
    `post_title` varchar(500) not null,
    `post_owner` varchar(100) not null,
    `post_content` mediumtext not null,
    `post_link` varchar(500) not null,
    `post_time` real not null,
    key `idx_post_time` (`post_time`),
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table apps (
    `id` varchar(50) not null,
    `app_name` varchar(500) not null,
    `app_link` varchar(500) not null,
    `app_time` real not null,
    key `idx_app_time` (`app_time`),
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table push_options (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_email` varchar(50) not null,
    `need_push` bool not null,
    `posts_type` varchar(50) not null,
    `keywords` varchar(500),
    `created_at` real not null,
    unique key `idx_user_id` (`user_id`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;



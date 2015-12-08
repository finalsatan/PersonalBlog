-- schema.sql



use personalblog;


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


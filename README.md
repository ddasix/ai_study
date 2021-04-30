# ai_study

## Create DB

1. [XAMPP](https://www.apachefriends.org/index.html "target='_blank'")를 이용 하여 mysql server 설치
2. DB 생성
    ~~~sql
    CREATE DATABASE ai_study;
    ~~~
3. DB User 생성 하고 권한부여
    ~~~sql
    GRANT ALL PRIVILEGES ON `ai_study`.* TO `YOUR ID`@localhost IDENTIFIED BY `YOUR PASSWORD` WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ~~~
4. Table 생성
    - Member
        ~~~sql
        CREATE TABLE `member` (
            `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
            `userid` VARCHAR(20) NULL DEFAULT NULL COMMENT '아이디' COLLATE 'utf8mb4_general_ci',
            `userpw` VARCHAR(200) NULL DEFAULT NULL COMMENT '비밀번호' COLLATE 'utf8mb4_general_ci',
            `name` VARCHAR(20) NULL DEFAULT NULL COMMENT '이름' COLLATE 'utf8mb4_general_ci',
            `img` VARCHAR(50) NULL DEFAULT NULL COMMENT '아바타 이미지' COLLATE 'utf8mb4_general_ci',
            `level` CHAR(1) NULL DEFAULT '1' COMMENT '권한' COLLATE 'utf8mb4_general_ci',
            `created_at` TIMESTAMP NULL DEFAULT current_timestamp(),
            `updated_at` DATETIME NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
            PRIMARY KEY (`id`) USING BTREE
        )
        COLLATE='utf8mb4_general_ci'
        ENGINE=InnoDB
        ;
        ~~~
    - News
        ~~~sql
        CREATE TABLE `news` (
            `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
            `category` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `subject` VARCHAR(200) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `content` LONGTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `comment` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `name` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `userid` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `img1` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `img2` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `img3` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `likenum` INT(11) NULL DEFAULT '0',
            `viewnum` INT(11) NULL DEFAULT '0',
            `created_at` TIMESTAMP NOT NULL DEFAULT current_timestamp(),
            `updated_at` TIMESTAMP NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
            PRIMARY KEY (`id`) USING BTREE
        )
        COLLATE='utf8mb4_general_ci'
        ENGINE=InnoDB
        ;
        ~~~
5. 기초데이터 Insert
    ~~~sql
    insert into member set userid = 'admin', userpw = password('123123'), name = '관리자', img = 'member.png';
    ~~~
    ~~~sql
    insert into news set category='정치', subject='제목', content='내용', comment='요약', name='작성자', userid='admin', img1='img_1.jpg', img2='img_2.jpg', img3='img_3.jpg';
    ~~~
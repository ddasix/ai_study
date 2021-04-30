# ai_study

## Create DB

1. [XAMPP](https://www.apachefriends.org/index.html)를 이용 하여 mysql server 설치
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
5. 기본 사용자 추가(관리자)
    ~~~sql
    insert into member set userid = 'admin', userpw = password('123123'), name = '관리자', img = 'member.png';
    ~~~
-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS db_eventos;

-- Use the created database
USE db_eventos;

-- User table
CREATE TABLE IF NOT EXISTS tb_usuario (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(150) NOT NULL,
    user_email VARCHAR(254) NOT NULL UNIQUE,
    user_password VARCHAR(90) NOT NULL,
    user_cpf VARCHAR(14) NOT NULL UNIQUE,
    user_phone VARCHAR(15),
    user_image BLOB,
    user_type BOOLEAN NOT NULL
);

-- Event location table
CREATE TABLE IF NOT EXISTS tb_local (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    address_state CHAR(2) NOT NULL,
    address_city VARCHAR(90) NOT NULL
);

-- Event table
CREATE TABLE IF NOT EXISTS tb_eventos (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    owner_event INT NOT NULL,
    location_event INT NOT NULL,
    location_address VARCHAR(150) NOT NULL,
    event_name VARCHAR(90) NOT NULL,
    event_description LONGTEXT,
    event_instagram VARCHAR(90),
    event_add_status BOOLEAN NOT NULL,
    event_space BOOLEAN NOT NULL,
    event_daily_price VARCHAR(90) NOT NULL,
    event_size VARCHAR(20),
    event_email VARCHAR(254),
    event_telefone VARCHAR(15),
    FOREIGN KEY (owner_event) REFERENCES tb_usuario(user_id),
    FOREIGN KEY (location_event) REFERENCES tb_local(address_id)
);

-- Event categories table
CREATE TABLE IF NOT EXISTS tb_categoria (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_categoria VARCHAR(90) NOT NULL UNIQUE
);

-- Event-category junction table
CREATE TABLE IF NOT EXISTS tb_evento_e_categoria (
    event_id INT NOT NULL,
    event_category INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES tb_eventos(event_id),
    FOREIGN KEY (event_category) REFERENCES tb_categoria(category_id),
    PRIMARY KEY (event_id, event_category)
);

-- Event images table
CREATE TABLE IF NOT EXISTS tb_imagem_evento (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    image_event_id INT NOT NULL,
    event_images BLOB,
    image_description VARCHAR(150),
    FOREIGN KEY (image_event_id) REFERENCES tb_eventos(event_id)
);

-- Reviews table
CREATE TABLE IF NOT EXISTS tb_review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_review_id INT NOT NULL,
    event_review_id INT NOT NULL,
    rating DECIMAL(3,2) NOT NULL,
    comments TEXT NOT NULL,
    review_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_review_id) REFERENCES tb_usuario(user_id),
    FOREIGN KEY (event_review_id) REFERENCES tb_eventos(event_id)
);

-- Password verification codes table
CREATE TABLE IF NOT EXISTS tb_verificacao_senha (
    user_id INT PRIMARY KEY,
    user_email VARCHAR(254) NOT NULL UNIQUE,
    verification_code VARCHAR(100) NOT NULL UNIQUE,
    expiration_time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tb_usuario(user_id)
);

-- Example data insertion
-- INSERT INTO tb_usuario (user_id, user_name, user_password, user_email, user_cpf) VALUES (1, 'Vinicius', '12345', 'viviserrao03@gmail.com', '05400140106');
-- INSERT INTO tb_verificacao_senha (user_id, verification_code, expiration_time) VALUES (1, '12345', NOW() + INTERVAL 10 MINUTE);

-- Example data cleanup
-- DELETE FROM tb_verificacao_senha WHERE expiration_time < NOW();

-- Criar o banco de dados se não existir
CREATE DATABASE IF NOT EXISTS db_eventos;

-- DROP DATABASE db_eventos;
-- Usar o banco de dados criado
USE db_eventos;

-- Tabela do usuário
CREATE TABLE IF NOT EXISTS tb_usuario(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(150) NOT NULL,
    user_email VARCHAR(90) NOT NULL UNIQUE,
    user_password VARCHAR(90) NOT NULL,
    user_cpf VARCHAR(90) NOT NULL UNIQUE,
    user_uf VARCHAR(2),
    user_image BLOB,
    user_type BOOLEAN
);

-- Tabela do endereço do evento
CREATE TABLE IF NOT EXISTS tb_local(
    local_id INT PRIMARY KEY AUTO_INCREMENT,
    owner_supplier_id INT NOT NULL,
    address VARCHAR(150) NOT NULL,
    address_lat DECIMAL,
    address_long DECIMAL,
    FOREIGN KEY (owner_supplier_id) REFERENCES tb_usuario(user_id)
);

-- Tabela das categorias do evento
CREATE TABLE IF NOT EXISTS tb_categoria_eventos (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_categoria VARCHAR(90) NOT NULL UNIQUE
);

-- Tabela do evento
CREATE TABLE IF NOT EXISTS tb_eventos(
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    owner_event INT NOT NULL,
    location_event INT NOT NULL,
    event_name VARCHAR(90) NOT NULL,
    event_category INT NOT NULL,
    event_description LONGTEXT,
    FOREIGN KEY (owner_event) REFERENCES tb_usuario(user_id),
    FOREIGN KEY (location_event) REFERENCES tb_local(local_id),
    FOREIGN KEY (event_category) REFERENCES tb_categoria_eventos(category_id)
);

-- Tabela das imagens dos eventos
CREATE TABLE IF NOT EXISTS tb_imagem_evento (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    image_event_id INT NOT NULL,
    event_images BLOB,
    FOREIGN KEY (image_event_id) REFERENCES tb_eventos(event_id)
);

-- Tabela dos reviews
CREATE TABLE IF NOT EXISTS tb_review(
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_review_id INT NOT NULL,
    event_review_id INT NOT NULL,
    rating DECIMAL NOT NULL,
    comments TEXT NOT NULL,
    review_time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_review_id) REFERENCES tb_usuario(user_id),
    FOREIGN KEY (event_review_id) REFERENCES tb_eventos(event_id)
);

-- Tabela para armazenar códigos de verificação de senha
CREATE TABLE IF NOT EXISTS tb_verificacao_senha (
    user_id INT PRIMARY KEY,
    user_email VARCHAR(90) NOT NULL UNIQUE,
    verification_code VARCHAR(100) NOT NULL UNIQUE,
    expiration_time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tb_usuario(user_id)
);

-- INSERT INTO tb_usuario (user_id, user_name , user_password , user_email , user_cpf) VALUES (1,'Vinicius','12345','viviserrao03@gmail.com','05400140106');
-- INSERT INTO tb_verificacao_senha ( user_id , verification_code , expiration_time) VALUES (1, '12345',NOW() + INTERVAL 10 MINUTE);

-- DELETE FROM tb_verificacao_senha WHERE expiration_time < NOW();

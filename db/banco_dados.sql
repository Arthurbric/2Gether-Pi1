-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS db_eventos;

-- DROP DATABASE db_eventos;

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
    user_image LONGBLOB,
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
    location_cep INT NOT NULL,
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
    event_images LONGBLOB,
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

-- Insert into tb_usuario
INSERT INTO tb_usuario (user_name, user_email, user_password, user_cpf, user_phone, user_type) VALUES ('Vinicius Gurgel','viviserrao03@gmail.com', '12345678', '05400140106','61981479944',TRUE);
INSERT INTO tb_usuario (user_name, user_email, user_password, user_cpf, user_phone, user_type) VALUES ('Maria Silva', 'maria.silva@gmail.com', '12345678', '12345678900', '11987654321', FALSE);
INSERT INTO tb_usuario (user_name, user_email, user_password, user_cpf, user_phone, user_type) VALUES ('João Souza', 'joao.souza@gmail.com', '12345678', '23456789011', '11976543210', FALSE);
INSERT INTO tb_usuario (user_name, user_email, user_password, user_cpf, user_phone, user_type) VALUES ('Ana Pereira', 'ana.pereira@gmail.com', '12345678', '34567890122', '11965432109', FALSE);

-- INSERT INTO tb_verificacao_senha (user_id, verification_code, expiration_time) VALUES (1, '12345', NOW() + INTERVAL 10 MINUTE);

-- Example data cleanup
-- DELETE FROM tb_verificacao_senha WHERE expiration_time < NOW();


-- Insert into tb_categoria
INSERT INTO tb_categoria (tipo_categoria) VALUES 
('aniversario'),
('casamento'),
('festa social'),
('conferencia'),
('seminario'),
('workshop'),
('show musical'),
('festival'),
('reuniao de negocios'),
('feira de exposicao');

INSERT INTO tb_local (address_state, address_city) VALUES 
('SP', 'São Paulo'),
('RJ', 'Rio de Janeiro'),
('MG', 'Belo Horizonte');

-- Inserir registros na tabela tb_eventos
INSERT INTO tb_eventos (owner_event,location_event,location_address,location_cep,event_name,event_description, 
    event_instagram,event_add_status,event_space,event_daily_price,event_size,event_email,event_telefone) 
VALUES (2,1,'Rua das Flores, 123','12345678','Festa de Aniversário',
    'Venha celebrar um aniversário inesquecível! Música, dança, comidas deliciosas e muita diversão aguardam por você. Não perca!',
    '@festa_aniversario',TRUE,TRUE,'500','100','aniversario@gmail.com','11987654321'),
(2,2,'Avenida Paulista, 456','23456789','Casamento dos Sonhos',
    'Participe de um casamento dos sonhos! Decoração de tirar o fôlego, buffet de alta gastronomia e um ambiente mágico para celebrar o amor.',
    '@casamento_sonhos',TRUE,TRUE,'2000','500','casamento@gmail.com','11976543210'),
(3,3,'Praça Central, 789','98765432','Workshop de Tecnologia',
    'Junte-se aos melhores especialistas em tecnologia para um workshop inovador! Descubra as tendências mais recentes e avance na sua carreira.',
    '@workshop_tec',TRUE,TRUE,'1500','300','workshop@gmail.com','11965432109');

INSERT INTO tb_evento_e_categoria (event_id,event_category) VALUES (1,1) , (2,2) , (3,6);


INSERT INTO tb_review (user_review_id, event_review_id, rating, comments) VALUES 
(2, 1, 4.5, 'A festa foi incrível!'),
(3, 2, 5.0, 'O casamento foi perfeito!'),
(4, 3, 4.0, 'O workshop foi muito informativo.');

INSERT INTO tb_imagem_evento (image_event_id, event_images, image_description) VALUES (2, load_file('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\profile2.png'), 'Descrição da imagem');

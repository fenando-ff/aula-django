CREATE DATABASE crud_escola charset utf8mb4;
USE crud_escola;


-- Tabela e manipulaçao turma
CREATE TABLE turma(
	id_turma INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_turma VARCHAR(45) NOT NULL
);

DELIMITER //
CREATE PROCEDURE insert_turma(IN p_nome_turma VARCHAR(45))
BEGIN
	INSERT INTO turma(nome_turma) VALUES (p_nome_turma);
END //
DELIMITER ;

CALL insert_turma("1º ANO");
CALL insert_turma("2º ANO");
CALL insert_turma("3º ANO");
CALL insert_turma("4º ANO");
CALL insert_turma("5º ANO");

SELECT * FROM turma;


-- Tabela e manipulaçao aluno
CREATE TABLE aluno(
	id_aluno INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_aluno VARCHAR(45) NOT NULL,
    dataNasc_aluno DATE NOT NULL,
    cpf_aluno VARCHAR(11) NOT NULL,
    obs_aluno TEXT,
    id_turma INT NOT NULL, 
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

DELIMITER //
CREATE PROCEDURE insert_aluno(
	IN p_nome_aluno VARCHAR(45), 
	IN p_dataNasc_aluno DATE, 
	IN p_cpf_aluno VARCHAR(11), 
	IN p_obs_aluno TEXT, 
	IN p_id_turma INT
)
BEGIN
	-- Verifica se o CPF já existe na tabela aluno
    IF EXISTS (SELECT 1 FROM aluno WHERE cpf_aluno = p_cpf_aluno) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: CPF já cadastrado!';
	ELSE
		INSERT INTO aluno(nome_aluno, dataNasc_aluno, cpf_aluno, obs_aluno, id_turma) VALUES (p_nome_aluno, p_dataNasc_aluno, p_cpf_aluno, p_obs_aluno, p_id_turma);
	END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_aluno(
    IN p_id_aluno INT,
    IN p_nome_aluno VARCHAR(45),
    IN p_dataNasc_aluno DATE,
    IN p_cpf_aluno VARCHAR(11),
    IN p_obs_aluno TEXT,
    IN p_id_turma INT
)
BEGIN
    -- Verifica se o aluno com o id_aluno fornecido existe
    IF NOT EXISTS (SELECT 1 FROM aluno WHERE id_aluno = p_id_aluno) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Aluno com o ID fornecido não existe!';
    END IF;

    -- Verifica se o CPF já está sendo usado por outro aluno (excluindo o aluno atual)
    IF EXISTS (SELECT 1 FROM aluno WHERE cpf_aluno = p_cpf_aluno AND id_aluno != p_id_aluno) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: CPF já cadastrado para outro aluno!';
    END IF;

    -- Verifica se a turma existe
    IF NOT EXISTS (SELECT 1 FROM turma WHERE id_turma = p_id_turma) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Turma com o ID fornecido não existe!';
    END IF;

    -- Atualiza o registro do aluno
    UPDATE aluno
    SET
        nome_aluno = p_nome_aluno,
        dataNasc_aluno = p_dataNasc_aluno,
        cpf_aluno = p_cpf_aluno,
        obs_aluno = p_obs_aluno,
        id_turma = p_id_turma
    WHERE id_aluno = p_id_aluno;
END //
DELIMITER ;

CALL insert_aluno("Paulo Plino", "2005-06-25", "15278974250", "Precisa de atenção", 100);

SELECT * FROM aluno;

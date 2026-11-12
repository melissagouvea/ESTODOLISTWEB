INSERT INTO tarefa (nomeTarefa, descricao, categoria, dataPrazo, prioridade, status)
VALUES 
    ('Trabalho história', 'Capítulo 4 e resumo página de 7 páginas', 'Escola', '2026-12-10', 'ALTA', 'Pendente'),
    ('Trabalho de mat', 'Realizar atividade 19 do livro didático', 'Escola', '2026-11-15', 'ALTA', 'Pendente'),
    ('Resumo biologia', 'Estudar o capítulo 8 sobre genética', 'Escola', '2026-11-18', 'BAIXA', 'Concluida'),
    ('Mapa mental lp', 'Fazer mapa mental com os conceitos do cap 3', 'Escola', '2026-11-20', 'MEDIA', 'Pendente'),
    ('Revisão de Física', 'Resolver lista de exercícios sobre cinemática', 'Estudos', '2026-11-22', 'ALTA', 'Pendente'),
    ('Apresentação de slides', 'Montar slides do seminário em grupo', 'Escola', '2026-11-25', 'MEDIA', 'Pendente'),
    ('Organizar pasta de projetos', 'Separar arquivos e fazer backup da semana', 'Trabalho', '2026-11-28', 'BAIXA', 'Concluida'),
    ('Redação modelo ENEM', 'Escrever texto dissertativo sobre tecnologia e educação', 'Estudos', '2026-12-02', 'ALTA', 'Pendente');

    SELECT * FROM tarefa;
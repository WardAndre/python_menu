import oracledb

def get_conexao():
    return oracledb.connect(user = "", password = "", dsn = "")

def inserir_alerta(alerta):
    sql = "insert into alerta_py(email, assunto, mensagem, id_estacao) values(:email, :assunto, :mensagem, :id_estacao)"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, alerta)
        con.commit()

def consultar_estacoes():
    sql = "select * from estacao_py order by id"
    dados = None
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            dados = cur.fetchall()
    return dados

def obter_estacao_por_nome(nome_estacao):
    sql = "select * from estacao_py where lower(nome) = lower(:nome)"
    dados = None
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"nome": nome_estacao})
            dados = cur.fetchone()
    return dados

def obter_alerta_por_id_estacao(id_estacao):
    sql = "select * from alerta_py where id_estacao = :id_estacao"
    dados = None
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id_estacao": id_estacao})
            dados = cur.fetchall()
    return dados

def consultar_linha_esmeralda():
    resultado = []
    estacoes = consultar_estacoes()
    for id_estacao, nome, conexao in estacoes:
        alertas_db = obter_alerta_por_id_estacao(id_estacao)
        alertas = []
        for alerta in alertas_db:
            _, email, assunto, mensagem, _ = alerta
            alertas.append({
                "email": email,
                "assunto": assunto,
                "mensagem": mensagem
            })
        resultado.append({
            "nome": nome,
            "conexão": conexao,
            "alertas": alertas
        })
    return resultado

def consultar_todos_alertas():
    sql = "SELECT a.id, e.nome, a.email, a.assunto, a.mensagem FROM alerta_py a JOIN estacao_py e ON a.id_estacao = e.id ORDER BY e.id, a.id"
    dados = None
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            dados = cur.fetchall()
    return dados

def atualizar_alerta(id_alerta, email, assunto, mensagem):
    sql = "UPDATE alerta_py SET email = :email, assunto = :assunto, mensagem= :mensagem WHERE id = :id_alerta"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {
                "email": email,
                "assunto": assunto,
                "mensagem": mensagem,
                "id_alerta": id_alerta
            })
        con.commit()

def deletar_alerta(id_alerta):
    sql = "DELETE FROM alerta_py WHERE id = :id_alerta"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id_alerta": id_alerta})
        con.commit()

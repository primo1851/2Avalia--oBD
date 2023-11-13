from neo4j import GraphDatabase


class Database:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(
            self.uri, auth=(self.username, self.password)
        )

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return result


database = Database("bolt://localhost:7687", "primo", "Didyoumissme?")


# Query 1
query1 = (
    "MATCH (prof:Teacher {name: 'Renzo'}) "
    "RETURN prof.ano_nasc AS ano_nasc, prof.cpf AS cpf"
)
result1 = database.run_query(query1)

for record in result1:
    print("Ano de Nascimento:", record["ano_nasc"])
    print("CPF:", record["cpf"])

# Query 2
query2 = (
    "MATCH (prof:Teacher) "
    "WHERE prof.name STARTS WITH 'M' "
    "RETURN prof.name AS name, prof.cpf AS cpf"
)
result2 = database.run_query(query2)

for record in result2:
    print("Nome:", record["name"])
    print("CPF:", record["cpf"])

# Query 3
query3 = "MATCH (city:City) RETURN city.name AS nome_cidade"
result3 = database.run_query(query3)

print("Nomes de todas as cidades:")
for record in result3:
    print(record["nome_cidade"])

# Query 4
query4 = (
    "MATCH (school:School) "
    "WHERE school.number >= 150 AND school.number <= 550 "
    "RETURN school.name AS nome_escola, school.address AS endereco, school.number AS numero"
)
result4 = database.run_query(query4)

print("\nEscolas com number entre 150 e 550:")
for record in result4:
    print("Nome da Escola:", record["nome_escola"])
    print("Endereço:", record["endereco"])
    print("Número:", record["numero"])

# Query 5
query5 = (
    "MATCH (prof:Teacher) "
    "WITH MIN(prof.ano_nasc) AS mais_jovem, MAX(prof.ano_nasc) AS mais_velho "
    "RETURN mais_jovem, mais_velho"
)
result5 = database.run_query(query5)

for record in result5:
    print("Ano de Nascimento do Professor Mais Jovem:", record["mais_jovem"])
    print("Ano de Nascimento do Professor Mais Velho:", record["mais_velho"])

# Query 6
query6 = (
    "MATCH (city:City) "
    "WITH AVG(city.population) AS media_populacional "
    "RETURN media_populacional"
)
result6 = database.run_query(query6)

for record in result6:
    print(
        "\nMédia Populacional de Todas as Cidades:",
        record["media_populacional"],
    )

# Query 7
query7 = (
    "MATCH (city:City {CEP: '37540-000'}) "
    "RETURN REPLACE(city.name, 'a', 'A') AS nome_modificado"
)
result7 = database.run_query(query7)

for record in result7:
    print(
        "\nNome da Cidade com CEP '37540-000' (substituindo 'a' por 'A'):",
        record["nome_modificado"],
    )

# Query 8
query8 = "MATCH (prof:Teacher) " "RETURN SUBSTRING(prof.name, 2, 1) AS terceira_letra"
result8 = database.run_query(query8)

print("\nCaractere a partir da 3ª letra do nome dos professores:")
for record in result8:
    print(record["terceira_letra"])


class TeacherCRUD:
    def __init__(self, database):
        self.database = database

    def create(self, name, ano_nasc, cpf):
        query = "CREATE (prof:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})"
        parameters = {"name": name, "ano_nasc": ano_nasc, "cpf": cpf}
        self.database.run_query(query, parameters)

    def read(self, name):
        query = "MATCH (prof:Teacher {name: $name}) RETURN prof"
        parameters = {"name": name}
        result = self.database.run_query(query, parameters)
        return result.single()

    def delete(self, name):
        query = "MATCH (prof:Teacher {name: $name}) DELETE prof"
        parameters = {"name": name}
        self.database.run_query(query, parameters)

    def update(self, name, new_cpf):
        query = "MATCH (prof:Teacher {name: $name}) SET prof.cpf = $new_cpf"
        parameters = {"name": name, "new_cpf": new_cpf}
        self.database.run_query(query, parameters)


teacher_crud = TeacherCRUD(database)

teacher_crud.create("Chris Lima", 1956, "189.052.396-66")
result_Teacher_search = teacher_crud.read("Chris Lima")

print("Resultados para o professor Chris Lima:")
print(result_Teacher_search)

teacher_crud.update("Chris Lima", "162.052.777-77")

database.close()

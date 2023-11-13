from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
username = "primo"
password = "Didyoumissme?"


def create_node(tx, label, property1, property2):
    query = f"{label} {{{property}, 2:'{property2}'}}"
    tx.run(query)


with open("AV2_Neo4J_BD.txt", "r") as file:
    lines = file.readlines()

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            for line in lines:
                data = line.strip().split(",")
                label = data[0]

                # Check if there are enough elements in the data list
                if len(data) >= 3:
                    property1, property2 = data[1], data[2]
                    session.write_transaction(create_node, label, property1, property2)
                else:
                    print(f"Skipping line: {line.strip()} - Not enough properties")

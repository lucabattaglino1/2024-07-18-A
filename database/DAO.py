from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT g.Chromosome
                        FROM genes g
                        ORDER BY g.Chromosome"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(c1, c2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT g.GeneID, g.Chromosome, g.Function
                    FROM genes g
                    WHERE g.Chromosome >= %s
                    and g.Chromosome <= %s
                    """

        cursor.execute(query, (c1, c2))

        for row in cursor:
            results.append(Gene(row["GeneID"], row["Chromosome"], row["Function"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppieRaw(c1, c2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []

        query = """SELECT DISTINCT g1.GeneID as id1, g2.GeneID as id2, i.Expression_Corr as peso
                    FROM genes g1, genes g2, classification cl1, classification cl2, interactions i
                    WHERE g1.GeneID = cl1.GeneID
                    and g2.GeneID = cl2.GeneID
                    and cl1.Localization = cl2.Localization
                    and g1.GeneID < g2.GeneID
                    and g1.Chromosome >= %s
                    and g1.Chromosome <= %s
                    and g2.Chromosome >= %s
                    and g2.Chromosome <= %s
                    and ((cl1.GeneID = i.GeneID1 and cl2.GeneID = i.GeneID2)
                         or
                         (cl2.GeneID = i.GeneID1 and cl1.GeneID = i.GeneID2))"""

        cursor.execute(query, (c1, c2, c1, c2))

        for row in cursor:
            results.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return results
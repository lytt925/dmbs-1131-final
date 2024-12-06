from app.database import db

class StatisticsService:
    @staticmethod
    def get_total_application_statistics():
        query = '''
            SELECT DATE_TRUNC('month', update_at) AS month, 
            COUNT(*) AS total_applications, 
            SUM(CASE WHEN status = 'S' THEN 1 ELSE 0 END) AS successful_rate,
            SUM(CASE WHEN status = 'F' THEN 1 ELSE 0 END) AS fail_rate
            FROM application AS app
            GROUP BY month;            
        '''
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                statistics = cur.fetchall()
                if len(statistics) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, s)) for s in statistics]
                    return response
                return None
    @staticmethod
    def get_filtered_application_statistics(filter: str):
        if filter not in ['size', 'species', 'breed', 'sex', 'shelter_id']:
            return None
        query = f'''
            SELECT {filter},
            DATE_TRUNC('month', update_at) AS month, 
            COUNT(*) AS total_applications, 
            SUM(CASE WHEN status = 'S' THEN 1 ELSE 0 END) AS successful_rate,
            SUM(CASE WHEN status = 'F' THEN 1 ELSE 0 END) AS fail_rate
            FROM application AS app
            JOIN animal AS ani ON 
                app.animal_id = ani.animal_id
            GROUP BY month, {filter};            
        '''
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                statistics = cur.fetchall()
                if len(statistics) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, s)) for s in statistics]
                    return response
                return None
            
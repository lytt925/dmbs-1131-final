def get_applications(user_id: int = None, animal_id: int = None, shelter_id: int = None):
        # 動態組裝條件
        conditions = []
        params = []

        if user_id is not None:
            conditions.append("app.user_id = %s")
            params.append(user_id)
        if animal_id is not None:
            conditions.append("app.animal_id = %s")
            params.append(animal_id)
        if shelter_id is not None:
            conditions.append("ani.shelter_id = %s")
            params.append(shelter_id)

        # 基本查詢語句
        base_query = """
            SELECT app.*, ani.shelter_id
            FROM application app
            JOIN animal ani ON app.animal_id = ani.animal_id
        """

        if conditions:
            # 使用 AND 串接條件
            where_clause = " WHERE " + " AND ".join(conditions)
            query = base_query + where_clause
            print(query)
        else:
            # 如果沒有條件，返回所有記錄（也可以視需求限制此行為）
            query = base_query
            print(query)

get_applications(None,None,2)
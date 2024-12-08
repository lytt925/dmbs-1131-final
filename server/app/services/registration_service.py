from app.database import db

class RegistrationService:
    @staticmethod
    def sign_up_for_activity(user_id: int, activity_id: int):
        select_activity_query = """
            SELECT remain_tickets 
            FROM activity 
            WHERE activity_id = %s
            FOR UPDATE;
        """

        check_registration_query = """
            SELECT * FROM registration
            WHERE user_id = %s AND activity_id = %s AND status IN ('R', 'A', 'X');
        """

        update_activity_query = """
            UPDATE activity
            SET remain_tickets = remain_tickets - 1
            WHERE activity_id = %s;
        """

        insert_registration_query = """
            INSERT INTO registration (user_id, activity_id, status)
            VALUES (%s, %s, 'R');
        """

        with db.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    # Lock the activity row 
                    cur.execute(select_activity_query, (activity_id,))
                    activity = cur.fetchone()

                    if not activity:
                        return {"error": "Activity does not exist"}

                    remain_seats = activity[0]
                    if remain_seats <= 0:
                        return {"error": "No remaining tickets for this activity"}

                    # Check if the user is already registered
                    cur.execute(check_registration_query, (user_id, activity_id))
                    existing_registration = cur.fetchone()

                    if existing_registration:
                        return {
                            "error": "User has already signed up for this activity",
                        }

                    # Update remaining seats
                    cur.execute(update_activity_query, (activity_id,))
                    if cur.rowcount == 0:
                        # This happens if no rows match the `remain_seats > 0` condition
                        return {"error": "No remaining tickets for this activity"}

                    # Insert new registration
                    cur.execute(
                        insert_registration_query, (user_id, activity_id)
                    )

                    # Commit the transaction
                    conn.commit()
                    return {"data": {"user_id": user_id, "activity_id": activity_id}}

            except Exception as e:
                conn.rollback()
                return {"error": str(e)}

    @staticmethod
    def cancel_activity_registration(user_id: int, activity_id: int):
        update_query = """
            UPDATE registration
            SET status = 'C'
            WHERE user_id = %s AND activity_id = %s AND status = 'R'
            RETURNING user_id, activity_id, status;
        """

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(update_query, (user_id, activity_id))
                result = cur.fetchone()  # Fetch the updated row
                conn.commit()
                if result:
                    return {
                        "data": {
                            "user_id": result[0],
                            "activity_id": result[1],
                            "status": result[2],
                        }
                    }
                else:
                    return {
                        "error": "No registration record found for the user and activity",
                    }

    @staticmethod
    def get_registration_by_user_id(
        user_id: int, page: int = 1, per_page: int = 10
    ) -> dict:
        query = """
            SELECT r.*, a.activity_type, a.time, a.location
            FROM registration r 
            JOIN activity a ON r.activity_id = a.activity_id
            WHERE user_id = %s
            LIMIT %s OFFSET %s;
        """

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                # Calculate offset
                offset = (page - 1) * per_page

                # Fetch paginated data
                cur.execute(query, (user_id, per_page, offset))
                registrations = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                results = [
                    dict(zip(columns, registration)) for registration in registrations
                ]

        return {
            "data": results,
            "meta": {
                "page": page,
                "per_page": per_page,
            },
        }

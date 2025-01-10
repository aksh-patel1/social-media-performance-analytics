class AstraDBOperations:
    def __init__(self, session):
        self.session = session
        # Set the keyspace
        self.session.set_keyspace('social_media_analytics')

    def create_schema(self):
        # Create table with post_type as part of the primary key
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                post_type text,
                posted_at timestamp,
                post_id text,
                likes int,
                shares int,
                comments int,
                PRIMARY KEY ((post_type), posted_at, post_id)
            )
        """)

    def insert_post(self, post):
        query = """
            INSERT INTO posts 
            (post_type, posted_at, post_id, likes, shares, comments)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.session.execute(query, (
            post['post_type'],
            post['posted_at'],
            post['post_id'],
            post['likes'],
            post['shares'],
            post['comments']
        ))

    def get_engagement_metrics(self, post_type=None):
        if post_type:
            query = """
                SELECT post_type, 
                       CAST(AVG(CAST(likes AS double)) AS double) as avg_likes,
                       CAST(AVG(CAST(shares AS double)) AS double) as avg_shares,
                       CAST(AVG(CAST(comments AS double)) AS double) as avg_comments
                FROM posts
                WHERE post_type = %s
            """
            results = self.session.execute(query, [post_type])
            return results
        else:
            query = """
                SELECT post_type, likes, shares, comments
                FROM posts
            """
            rows = self.session.execute(query)
            
            metrics = {}
            for row in rows:
                if row.post_type not in metrics:
                    metrics[row.post_type] = {
                        'likes': [], 'shares': [], 'comments': []
                    }
                metrics[row.post_type]['likes'].append(row.likes)
                metrics[row.post_type]['shares'].append(row.shares)
                metrics[row.post_type]['comments'].append(row.comments)
            
            results = []
            for post_type, data in metrics.items():
                if data['likes']:  # Check if there's data to avoid division by zero
                    avg_likes = sum(data['likes']) / len(data['likes'])
                    avg_shares = sum(data['shares']) / len(data['shares'])
                    avg_comments = sum(data['comments']) / len(data['comments'])
                    
                    results.append({
                        'post_type': post_type,
                        'avg_likes': avg_likes,
                        'avg_shares': avg_shares,
                        'avg_comments': avg_comments
                    })
            
            return results

    def drop_table(self):
        """Helper method to drop the table if needed for reset"""
        self.session.execute("DROP TABLE IF EXISTS posts")
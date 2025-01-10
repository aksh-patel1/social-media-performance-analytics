import random
from datetime import datetime, timedelta

class MockDataGenerator:
    def __init__(self):
        self.post_types = ['carousel', 'reel', 'static']
        self.base_engagement_rates = {
            'carousel': {'likes': 100, 'shares': 20, 'comments': 15},
            'reel': {'likes': 150, 'shares': 30, 'comments': 25},
            'static': {'likes': 80, 'shares': 15, 'comments': 10}
        }

    def generate_mock_data(self, num_posts=100):
        posts = []
        current_date = datetime.now()
        for _ in range(num_posts):
            post_type = random.choice(self.post_types)
            base_rates = self.base_engagement_rates[post_type]
            variance = random.uniform(0.8, 1.2)
            post = {
                'post_id': f'post_{_}',
                'post_type': post_type,
                'posted_at': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                'likes': int(base_rates['likes'] * variance),
                'shares': int(base_rates['shares'] * variance),
                'comments': int(base_rates['comments'] * variance)
            }
            posts.append(post)
            current_date -= timedelta(hours=random.randint(1, 24))
        return posts

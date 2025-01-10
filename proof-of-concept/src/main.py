from cassandra.cluster import Cluster
from config.astra_config import AstraDBConfig
from data.mock_data_generator import MockDataGenerator
from db.astra_operations import AstraDBOperations
from analytics.processor import AnalyticsProcessor

def main():
    config = AstraDBConfig()
    cluster = Cluster(cloud=config.get_cloud_config(), auth_provider=config.get_auth_provider())
    session = cluster.connect()
    
    db_ops = AstraDBOperations(session)

    try:
        db_ops.create_schema()
    
        data_generator = MockDataGenerator()
        mock_posts = data_generator.generate_mock_data()
        for post in mock_posts:
            db_ops.insert_post(post)
    except Exception as e:
        print(e)
    
    analytics = AnalyticsProcessor(db_ops)
    gpt_prompt = analytics.prepare_gpt_prompt()
    
    session.shutdown()
    cluster.shutdown()

    print(gpt_prompt)

if __name__ == "__main__":
    main()

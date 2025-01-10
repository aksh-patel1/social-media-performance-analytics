import pandas as pd

class AnalyticsProcessor:
    def __init__(self, db_ops):
        self.db_ops = db_ops

    def prepare_gpt_prompt(self):
        metrics = self.db_ops.get_engagement_metrics()
        print(f"## metrics retrieved from Astra DB ## \n{metrics}")
        metrics_df = pd.DataFrame(list(metrics))
        prompt = "Based on the following social media metrics:\n\n"
        for _, row in metrics_df.iterrows():
            prompt += f"Post Type: {row['post_type']}\n"
            prompt += f"Average Likes: {row['avg_likes']:.1f}\n"
            prompt += f"Average Shares: {row['avg_shares']:.1f}\n"
            prompt += f"Average Comments: {row['avg_comments']:.1f}\n\n"
        prompt += "Please provide insights about:\n"
        prompt += "1. Which post type performs best overall\n"
        prompt += "2. Specific engagement patterns\n"
        prompt += "3. Recommendations for content strategy\n"
        return prompt

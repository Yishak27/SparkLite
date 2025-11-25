class NarationSummary:
    def __init__(self):
        pass
    def generate_summary(self, user_query, result, df):
        try:
            return "This is ai summary....."
        except Exception as e:
            print('ai summary exception error:', e)
            return "Unable to generate summary."
        
        
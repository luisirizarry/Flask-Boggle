from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_boogle_home(self):
        """Test the home route and initialization of session variables."""
        res = self.client.get('/')
        html = res.get_data(as_text=True)

        """Test the response status code and the content of the page."""
        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1>Boggle Game!</h1>', html)
        
        """Test the initialization of session variables."""
        with self.client.session_transaction() as session:
            self.assertEqual(session.get('highscore'), 0)
            self.assertEqual(session.get('games_played'), 0)
            self.assertEqual(session.get('word_set'), [])

    def test_check_word(self):
        """Test the /check-guess route for valid, duplicate, and invalid words."""
        # Finish here


    def test_post_score(self):
        """Test the /post-score route."""
        self.client.get('/')  # Initialize session
        """Test when the score is updated."""
        new_score = 100
        res = self.client.post('/post-score', json={"score": new_score})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['score'], new_score)
        
        with self.client.session_transaction() as session:
            self.assertEqual(session.get('score'), new_score)

    def test_post_high_score(self):
        """Test the /post-high-score route for updating highscore and games played."""
        self.client.get('/')  # Initialize session
        new_score = 200
        
        # Test when new score is higher than existing highscore
        res = self.client.post('/post-high-score', json={"score": new_score})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['highscore'], new_score)
        self.assertEqual(res.json['games_played'], 1)
        
        # Test when new score is lower or equal to existing highscore
        current_score = 150
        with self.client.session_transaction() as session:
            session['highscore'] = current_score
        res = self.client.post('/post-high-score', json={"score": 100})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['highscore'], current_score)
        self.assertEqual(res.json['games_played'], 2)

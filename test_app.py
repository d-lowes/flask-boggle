from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertEquals(response.status_code, 200)
            self.assertIn('<!-- This is the homepage -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            ...
            response = client.post('/api/new-game')
            json = response.get_json()

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertIsInstance(json["gameId"], str)
            self.assertIsInstance(json["board"], list)

    def test_score_word(self):
        """Create a client instance, retrieve JSON data, create a game board
        test if a word is on the board, not a word, and not on board"""

        with self.client as client:
            ...
            response = client.post('/api/new-game')
            json = response.get_json()

            game_id = json["gameId"]
            game = games[game_id]
            game.board = [["P","E","C","A","N"],
                          ["P","A","L","I","N"],
                          ["E","R","U","L","E"],
		                  ["T","R","E","T","O"],
                          ["F","F","E","U","S"]]
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}
            test = client.post('/api/score-word' ,
                                        json={"gameId":game_id, "word":"PECAN"})
            data = test.get_json()
            self.assertEqual({"result":"ok"}, data)

            test = client.post('/api/score-word' ,
                                        json={"gameId":game_id, "word":"BLAH"})
            data = test.get_json()
            self.assertEqual({"result":"not-on-board"}, data)

            test = client.post('/api/score-word' ,
                                        json={"gameId":game_id, "word":"JKSIJ"})
            data = test.get_json()
            self.assertEqual({"result":"not-word"}, data)
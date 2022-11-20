import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import *

from App.main import create_app
from App.database import create_db, db
from App.models import User, Author, Publication
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    create_publication,
    get_all_authors_json,
    create_author,
    create_publication,
    get_all_publications_json,
    get_author
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
## Fixtures ##
@pytest.fixture
def setup_User_1():
    testUsername = "bob"
    testPassword = "bobpass"
    testID = 1
    user1 = User(testUsername, testPassword, testID)
    return user1

@pytest.fixture
def setup_User_2():
    testUsername = "rick"
    testPassword = "bobpass"
    testID = 2
    user2 = User(testUsername, testPassword, testID)
    return user2
## end fixtures ## 


class UserUnitTests():

    def test_new_user(setup_User):
        assert user.username == "bob"

    def test_user_toJSON(setup_User):
        user_json = user.toJSON()
        assert user_json == {"id":None, "username":"bob", "authorId":1}
    
    def test_hashed_password(self):
        hashed = generate_password_hash(password, method='sha256')
        assert user.password != password

    def test_check_password(self):
        assert user.check_password(password)

class AuthorUnitTests(unittest.TestCase):

    def test_new_author(setupAuthor):
        assert author.name == "Bob Moog" and author.dob == datetime.strptime("05/08/2001", "%d/%m/%Y") and author.qualifications == "BSc. Computer Science"

    def test_author_toJSON(self):
        author_json = author.toJSON()
        self.assertDictEqual(author_json, {
            "id": None,
            "name": "Bob Moog",
            "dob": datetime.strptime("05/08/2001", "%d/%m/%Y"),
            "qualifications": "BSc. Computer Science"
        })

class PublicationUnitTests(unittest.TestCase):
    def test_new_publication(self):
        coauthors = []
        author = Author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        coauthor = Author("Bob Dule", "06/09/2002", "BSc. Computer Engineering")
        coauthors.append(coauthor)
        publication = Publication("Intro to Computer Science", author.id, coauthors)
        assert (
            publication.title=="Intro to Computer Science" 
            and publication.authorId==author.id
            and publication.coauthors==coauthors
        )

    def test_publication_toJSON(self):
        coauthors = []
        author = Author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        coauthor = Author("Bob Dule", "06/09/2002", "BSc. Computer Engineering")
        coauthors.append(coauthor)
        publication = Publication("Intro to Computer Science", author.id, coauthors)
        publication_json = publication.toJSON()
        self.assertDictEqual(publication_json, {
            "id": None,
            "title": "Intro to Computer Science",
            "author": None,
            "coauthors": [coauthor.toJSON() for coauthor in coauthors]
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    create_all(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

@pytest.fixture(scope="module")
def setup_Authors():
    #author 1
    testName1 = "Bob Moog"
    testDoB1 = "05/08/2001"
    testQualifications1 = "BSc. Computer Science"
    author1 = Author(testName1, testDoB1, testQualifications1)

    #author 2
    testName2 = "Bob Moog"
    testDoB2 = "05/08/2001"
    testQualifications2 = "BSc. Computer Science"
    author2 = Author(testName2, testDoB2, testQualifications2)
    



# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests():
    def test_authenticate(setup_User_1):
        assert authenticate("bob", "bobpass") != None

    def test_create_user(setup_User_2):
        # user = create_user("bob", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(setup_User_1, setup_User_2):
        users_json = get_all_users_json()
        assert [{"id":1, "username":"bob", "authorId":1}, {"id":2, "username":"rick", "authorId":2}] == users_json

    # Tests data changes in the database
    def test_update_user(setup_User_1):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class AuthorIntegrationTests():
    def test_create_author(setup_Author):
        assert author.name == "Bob Moog"

    def test_get_all_authors_json(setup_Author):
        author_json=get_all_authors_json()
        self.assertListEqual([{
            'id': 1,
            "name": "Bob Moog",
            "dob":datetime.strptime("05/08/2001", "%d/%m/%Y"),
            "qualifications":"BSc. Computer Science"
            }
            ], author_json)

class PublicationIntegrationTests():
    def test_create_publication(setup_Author):
        author = get_author(1)
        if not author:
            author = create_author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        coauthors = []
        publication=create_publication("Intro to Computer Science",author.id, coauthors)
        assert publication.title=="Intro to Computer Science"

    def test_get_publication_json(self):
        publication_json = get_all_publications_json()
        self.assertListEqual([
            {
                "id": 1,
                "title":"Intro to Computer Science",
                "author":1,
                "coauthors":[]
            }
        ], publication_json)
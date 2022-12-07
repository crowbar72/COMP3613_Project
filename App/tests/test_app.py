import os, tempfile, pytest, logging
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

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class.
# This is for the integration tests!
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

@pytest.fixture()
def username_1():
    return "bob"

@pytest.fixture()
def username_2():
    return "rick"

@pytest.fixture()
def name_1():
    return "bob"

@pytest.fixture()
def name_2():
    return "rick"

@pytest.fixture()
def password():
    return "speakFriendAndEnter"

@pytest.fixture()
def ID_1():
    return 1

@pytest.fixture()
def ID_2():
    return 2

@pytest.fixture()
def DoB():
    return datetime.strptime("05/08/2001 00:00:00", "%d/%m/%Y %H:%M:%S")

@pytest.fixture()
def qualification_1():
    return "BSc. Computer Science"

@pytest.fixture()
def qualification_2():
    return "MSc. Computer Science"

@pytest.fixture()
def title_1():
    return "Argonian Literature in The Elder Scrolls series: an Anaysis."

@pytest.fixture()
def abstract():
    return "Bethesda writers are arguably some of the most hardcore nerds in the industry. Rivalling the likes of J.R.R. Tolkien, these career creatives designed a lore delivery system for the elder scroll series that functions on collecting..."

@pytest.fixture()
def publication_Date():
    now = date.today()
    return now

@pytest.fixture()
def userT( username_1, password, ID_1):
    user = User( username_1, password, ID_1)
    return user

@pytest.fixture()
def userT2( username_2, password, ID_2):
    user = User( username_2, password, ID_2)
    return user

@pytest.fixture()
def authorT(name_1, DoB, qualification_1):
    author = Author(name_1, DoB, qualification_1)
    return author

@pytest.fixture()
def authorT2(name_2, DoB, qualification_2):
    author = Author(name_2, DoB, qualification_2)
    return author

@pytest.fixture()
def pubTest(title_1, ID_1, authorT2, publication_Date, abstract):
    coauthors = []
    coauthors.append(authorT2)
    publication = Publication(title_1, ID_1, coauthors, abstract, publication_Date)
    return publication


## end fixtures ## 
#----------------#

class TestUserUnit():
    
    def test_new_user(self, userT):
        assert userT.username == 'bob'

    def test_user_toJSON(self, userT):
        user_json = userT.toJSON()
        assert user_json == {"id":None, "username":"bob", "authorId":1}
    
    def test_hashed_password(self, userT, password):
        hashed = generate_password_hash(password, method='sha256')
        assert userT.password != "speakFriendAndEnter"

    def test_check_password(self, userT, password):
        assert userT.check_password(password)

class TestAuthorUnit():

    def test_new_author(self, name_1, DoB, qualification_1):
        author = Author(name_1, DoB, qualification_1)
        assert author.name == "bob" and author.dob == datetime.strptime("05/08/2001", "%d/%m/%Y") and author.qualifications == "BSc. Computer Science"

    def test_author_toJSON(self, name_1, DoB, qualification_1):
        author = Author(name_1, DoB, qualification_1)
        author_json = author.toJSON()
        assert author_json == {
            "id": None,
            "name": "bob",
            "dob": datetime.strptime("05/08/2001", "%d/%m/%Y"),
            "qualifications": "BSc. Computer Science"
        }

class TestPublicationUnit():

    def test_new_publication(self, pubTest, authorT2):
        assert pubTest.title=="Argonian Literature in The Elder Scrolls series: an Anaysis." and pubTest.authorId==1 and pubTest.coauthors==[authorT2]

    def test_publication_toJSON(self, pubTest):
        publication_json = pubTest.toJSON()
        assert publication_json == {
            "id": None,
            "title": "Argonian Literature in The Elder Scrolls series: an Anaysis.",
            "author": 1,
            "coauthors": [coauthor.toJSON() for coauthor in pubTest.coauthors],
            "abstract":"Bethesda writers are arguably some of the most hardcore nerds in the industry. Rivalling the likes of J.R.R. Tolkien, these career creatives designed a lore delivery system for the elder scroll series that functions on collecting...",
            "dateOfPublication": date.today()
        }

'''
    Integration Tests
'''

class TestUsersIntegration():
    def test_authenticate(self, username_1, password, ID_1):
        user = create_user(username_1, password, ID_1)
        assert authenticate(username_1, password) != None
        
    def test_create_user(self, userT2):
        user = create_user(userT2.username, userT2.password, userT2.authorId)
        assert user.username == "rick"

    def test_get_all_users_json(self, userT2):
        users_json = get_all_users_json()
        assert [{"id":1, "username":"bob", "authorId":1}, {"id":2, "username":"rick", "authorId":2}] == users_json

    # Tests data changes in the database
    def test_update_user(self, username_1, password, ID_1):
        user = create_user(username_1, password, ID_1)
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

class TestAuthorIntegration():
    def test_create_author(self, authorT, DoB):
        author = create_author(authorT.name, DoB, authorT.qualifications)
        assert author.name == "bob"

    def test_get_all_authors_json(self):
        author_json = get_all_authors_json()
        assert [{
            'id': 1,
            "name": "bob",
            "dob": datetime.strptime("05/08/2001 00:00:00", "%d/%m/%Y %H:%M:%S"),
            "qualifications":"BSc. Computer Science"
            }] == author_json

class TestPublicationIntegration():
    def test_create_publication(self, pubTest):
        assert pubTest.title=="Argonian Literature in The Elder Scrolls series: an Anaysis."

    def test_get_publication_json(self, pubTest, authorT2):
        pub = create_publication(pubTest.title, pubTest.authorId, pubTest.coauthors, pubTest.abstract, pubTest.dateOfPublication)
        publication_json = get_all_publications_json()
        assert [
            {
                "id": 1,
                "title":"Argonian Literature in The Elder Scrolls series: an Anaysis.",
                "author":1,
                "coauthors":[authorT2.toJSON()],
                "abstract":"Bethesda writers are arguably some of the most hardcore nerds in the industry. Rivalling the likes of J.R.R. Tolkien, these career creatives designed a lore delivery system for the elder scroll series that functions on collecting...",
                "dateOfPublication": date.today()
            } 
        ] == publication_json
        #I think date of publication fails here in the off chance that you create the fixture at 11:59pm and then this runs at 12:00 am. That's one hell of an edge case, though.
            

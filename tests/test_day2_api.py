import requests

# Query Params
# 1. Fetch all comments for post ID 2 and verify that all returned comments belong to that post.
def test_post_id2():
    r = requests.get("https://jsonplaceholder.typicode.com/posts/2/comments")
    data = r.json()
    for comment in data:
        assert comment["postId"] == 2, f"Comentário {comment['id']} não pertence ao post 2"
    print(f"Todos os {len(data)} comentários pertencem ao post 2")

# 2. List all todos for user ID 5 and verify that the list is not empty.
def test_list_all():
    r = requests.get("https://jsonplaceholder.typicode.com/user/5/todos")
    data = r.json()
    total = len(data)
    assert total > 0
    print (f'o total de todos para o usuário com id 5 é: {total}')

# 3. Fetch all albums for user ID 9 and count how many they have (should be 10).
def test_all_albums():
    r = requests.get("https://jsonplaceholder.typicode.com/user/9/albums")
    data = r.json()
    total = len(data)
    assert total == 10
    print(f'o total de álbums do usuário com id 9 é: {total}')

# 4. List all completed todos (completed: true) for user ID 1 and verify that all in the response are indeed completed.
def test_todos_id1():
    r = requests.get("https://jsonplaceholder.typicode.com/user/1/todos")
    data = r.json()
    completed_data = []
    for n in data:
        if n["completed"]:
            completed_data.append(n)
    
    assert all(n["completed"] for n in completed_data)
    print(f"Total de tarefas completadas: {len(completed_data)}")

# Headers
# 5. Send a request to httpbin.org/headers with the custom header X-Custom-Header: MyValue and validate the response.
#def test_custom_header():
    #r = requests.get("")

# 6. Send a request to httpbin.org/response-headers to set a custom response header (e.g., My-Test-Header: Hello) and check if it is present in the response headers.
# def test_

# 7. Send a request to httpbin.org/headers with a custom User-Agent header ("My-Test-Agent/1.0") and validate if it was received correctly.
# def test_

# 8. Send multiple custom headers (X-Header-1: Value1, X-Header-2: Value2) in a single request to httpbin.org/headers and validate all of them.
# def test_

# Authentication
# 9. Test the httpbin Basic Auth endpoint (/basic-auth/user/passwd) with the correct credentials (user, passwd) and validate the 200 status.
# def test_

# 10. Test the same Basic Auth endpoint with a correct user but wrong password and validate the 401 status.
# def test_

# 11. Send a request to httpbin.org/bearer with a valid Bearer Token (mock, e.g., "my-mock-token") and validate the successful authentication.
# def test_

# 12. Send a request to httpbin.org/bearer without any authorization header and validate if the response is 401.
# def test_

# Advanced Assertions
# 13. Fetch user with ID 1 from JSONPlaceholder and validate the data types of the keys id (int), name (str), address (dict), and company (dict).
def test_user_id1():
    r = requests.get("https://jsonplaceholder.typicode.com/users/1")
    data = r.json()
    id = data["id"]
    name = data["name"]
    address = data["address"]
    company = data["company"]

    assert type(id) == int
    assert type(name) == str
    assert type(address) == dict
    assert type(company) == dict

    print(f'os tipos das keys são: id:{type(id)}, name: {type(name)}, address: {type(address)}, company: {type(company)}')

# 14. For the same user, check if the address key contains the sub-keys street, city, and zipcode.
def test_address_id1():
    r = requests.get("https://jsonplaceholder.typicode.com/users/1")
    data = r.json()
    address = data["address"]
    
    for n in ["street", "city","zipcode"]:
        assert n in address

    print(f'as keys são: {address["street"]}, {address["city"]} e {address["zipcode"]}')

# 15. Fetch post with ID 10 and validate if the keys userId and id are integers and if title and body are non-empty strings.
def test_check_post_id10():
    r = requests.get("https://jsonplaceholder.typicode.com/posts/10")
    data = r.json()
    userId = data["userId"]
    id = data["id"]
    title = data["title"]
    body = data["body"]

    assert type(userId) and type(id) == int
    assert title and body != ""
    print(f'conteúdo das chaves: id do usuário: {userId}, id do post: {id}, título do post: {title}, conteúdo do post: {body}')

    if title and body == "":
        print("título e corpo do post vazios!")

# 16. List the photos from album with ID 1 and check if each photo in the response contains the keys albumId, id, title, url, and thumbnailUrl.
def test_photo_album_id1():
    r = requests.get("https://jsonplaceholder.typicode.com/albums/1/photos")
    data = r.json()

    for i in data:
        for n in ["albumId", "id", "title", "url", "thumbnailUrl"]:
            assert n in i 

    print("album validado!")

# 17. Check if the email key of user with ID 3 follows a valid email format (contains "@" and "." in the domain part).
def test_email_id3():
    r = requests.get("https://jsonplaceholder.typicode.com/users/3")
    data = r.json()
    email = data["email"]

    # 1. Tem exatamente um '@'
    assert email.count("@") == 1, "Email deve conter exatamente um @"

    # 2. Tem '.' depois do '@'
    at_index = email.index("@")
    assert "." in email[at_index:], "Email deve conter ponto após o @"

    # 3. Não começa ou termina com '.' ou '@'
    assert not (email.startswith("@") or email.endswith("@")), "Email começa ou termina com @"
    assert not (email.startswith(".") or email.endswith(".")), "Email começa ou termina com ."

    # 4. Não contém vírgula
    assert "," not in email, "Email contém vírgula"

    print(f"O email '{email}' é válido!")

# 18. Fetch the comments for post with ID 5 and check if the list of comments is not empty.
def test_comments_post_id5():
    r = requests.get("https://jsonplaceholder.typicode.com/posts/5/comments")
    data = r.json()
    assert data != []
    print("A lista não está vazia!")

# 19. For the first comment from the previous list, validate the types of postId (int), id (int), name (str), email (str), and body (str).
def test_first_comment_id5():
    r = requests.get("https://jsonplaceholder.typicode.com/posts/5/comments")
    data = r.json()
    comment = data[0]
    postId = comment["postId"]
    id = comment["id"]
    name = comment["name"]
    email = comment["email"]
    body = comment["body"]

    assert type(postId) == int
    print("a variável postId é um int")
    assert type(id) == int
    print("a variável id é um int")
    assert type(name) == str
    print("a variável name é uma string")
    assert type(email) == str
    print("a variável email é uma sring")
    assert type(body) == str
    print("a variável body é uma string")

# 20. Fetch the todo with ID 199 and check if the value of the completed key is a boolean (True or False).
def test_todo_id199():
    r = requests.get("https://jsonplaceholder.typicode.com/todos/199")
    data = r.json()
    completed = data["completed"]

    assert type(completed) == bool
    print("a variável completed é um boolean")
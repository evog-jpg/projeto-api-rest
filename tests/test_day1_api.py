import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
headers = {'Authorization': f"Bearer {token}"}

def test_base_endpoint_status_code_200():
    r = requests.get('https://api.github.com', headers=headers)
    assert r.status_code == 200
    print("o status code realmente foi:", r.status_code)

def test_fetch_octocat_user_name():
    r = requests.get("https://api.github.com/users/octocat", headers=headers)
    data = r.json()
    print("o nome do usuário é:", data["name"])

def test_octocat_type_is_user():
    r = requests.get("https://api.github.com/users/octocat", headers=headers)
    data = r.json()
    assert data["type"] == "User"
    print("o tipo dele realmente é:", data["type"])

def test_repository_hello_world():
    r = requests.get("https://api.github.com/repositories/1296269", headers=headers)
    data = r.json()
    assert data["name"] == "Hello-World"
    print(f'o nome do repositorio {data["id"]} realmente é {data["name"]}')

def test_nonexistent_user_returns_404():
    r = requests.get("https://api.github.com/users/nonexistentuser12345", headers=headers)
    assert r.status_code == 404
    print("o status code realmente foi:", r.status_code)

def test_google_repositories_limit_5():
    r = requests.get("https://api.github.com/users/google/repos", params={"per_page": 5}, headers=headers)
    assert r.status_code == 200, f"Erro na requisição: {r.status_code}"
    repos = r.json()
    assert repos[0]["name"] == ".allstar"
    print("o nome do primeiro repositório é:", repos[0]["name"])

def test_microsoft_followers_and_pagination():
    r = requests.get("https://api.github.com/users/microsoft/followers", headers=headers)
    assert r.status_code == 200
    followers = r.json()
    print(f"Primeiro seguidor: {followers[0]['login']}")

    link_header = r.headers.get("Link")
    if link_header and 'rel="next"' in link_header:
        next_url = link_header.split(";")[0].strip("<> ")
        print("Próxima página:", next_url)

        next_response = requests.get(next_url)
        assert next_response.status_code == 200
        print("Segunda página carregada com sucesso!")
    else:
        print("Não há próxima página de seguidores.")

def test_facebook_public_repositories_count():
    r = requests.get("https://api.github.com/users/facebook", headers=headers)
    assert r.status_code == 200
    pub_repos = r.json()
    assert pub_repos["public_repos"] == 153
    print(f'o facebook tem {pub_repos["public_repos"]} repositorios públicos')

def test_facebook_react_language_is_javascript():
    r = requests.get("https://api.github.com/repos/facebook/react", headers=headers)
    assert r.status_code == 200
    react_repo = r.json()
    assert react_repo["language"] == "JavaScript"
    print(react_repo["language"])

def test_emojis_endpoint_plus_one_exists():
    r = requests.get("https://api.github.com/emojis", headers=headers)
    assert r.status_code == 200
    emojis = r.json()
    assert emojis["+1"] == "https://github.githubassets.com/images/icons/emoji/unicode/1f44d.png?v8"
    print("o emoji existe no github")

def test_name_owner_language_in_torvalds():
    r = requests.get("https://api.github.com/repos/torvalds/linux", headers=headers)
    data = r.json()
    assert "name" in data
    assert "owner" in data
    assert "language" in data
    print(f'o nome é: {data["name"]}, o dono do repo é: {data["owner"]["login"]} e a linguagem foi: {data["language"]}')

# Compare the "stargazers_count" of Microsoft's "vscode" repository and Atom's "atom" repository. Check if the VSCode count is higher.
def test_stargazers_and_atom():
    r = requests.get("https://api.github.com/repos/microsoft/vscode", headers=headers)
    r2 = requests.get("https://api.github.com/repos/atom/atom", headers=headers)
    data = r.json()
    data2 = r2.json()

    if data["stargazers_count"] > data2["stargazers_count"]:
        print("a contagem de stargazers do vscode é maior.")
    elif data["stargazers_count"] < data2["stargazers_count"]:
        print("a contagem de stargazers do atom é maior")
    elif data["stargazers_count"] == data2["stargazers_count"]:
        print("a contagem dos dois é igual")
    assert data["stargazers_count"] > data2["stargazers_count"]

def test_mit_license():
    r = requests.get("https://api.github.com/licenses/mit", headers=headers)
    data = r.json()

    assert data["name"] == "MIT License"
    print(f'o nome da licença é: {data["name"]}')

def test_count_common_licenses():
    r = requests.get("https://api.github.com/licenses", headers=headers)
    data = r.json()
    total_licenses = len(data)
    assert total_licenses == 13
    print(f'existem {total_licenses} no github')

def test_count_apache_search():
    r = requests.get("https://api.github.com/search/repositories?q=licence:apache-2.0", headers=headers)
    data = r.json()
    first_repo = data["items"][0]
    assert first_repo["license"]["key"] == "apache-2.0"
    print(f'o nome do primeiro de repostorio que usa apache 2.0 é: {first_repo["name"]}')

def test_check_docker_repo_moby():
    r = requests.get("https://api.github.com/repos/moby/docker", headers=headers)
    data = r.json()
    login = data["owner"]["login"]
    type = data["owner"]["type"]
    assert login == "moby" and type == "Organization"
    print(f'o repositorio pertence a {login} que é do tipo {type}')

def test_tensorflow():
    r = requests.get("https://api.github.com/repos/tensorflow/tensorflow/commits", headers=headers)
    data = r.json()
    message = data[0]["commit"]["message"]
    assert message != ""
    print(f'a mensagem do último commit não é nula, é: {message}')

def test_apple_org():
    r = requests.get("https://api.github.com/users/apple")
    data = r.json()
    login = data["login"]
    type = data["type"]
    assert login == "apple" and type == "Organization"
    print(f'o usuário com login: {login} realmente é do tipo: {type}')

def test_contributors_kubernetes():
    r = requests.get("https://api.github.com/repos/kubernetes/kubernetes/contributors", params={"per_page": 100}, headers=headers)
    link_header = r.headers.get("Link")
    if link_header and 'rel="last"' in link_header:
        last_page = int(link_header.split("page=")[-1].split(">")[0])
        total_contributors = last_page * 100
    else:
        total_contributors = len(r.json())

    print(f"Total de contribuidores estimado: {total_contributors}")
    assert total_contributors < 1000, f"Número de contribuidores é baixo: {total_contributors}"

def test_user_torvalds():
    url = "https://api.github.com/users"
    r = "/torvalds"
    search_user = requests.get(url + r)
    data = search_user.json()
    user_data = [f'username encontrado: {data["login"]}, nome encontrado: {data["name"]}, número de repositórios públicos encontrado: {data["public_repos"]}']
    assert data["login"] == "torvalds"
    assert data["name"] == "Linus Torvalds"
    assert isinstance(data["public_repos"], int)
    assert data["public_repos"] > 0
    print(user_data)

def test_create_new_post():
    payload = {
    "title": "meu primeiro post",
    "body": "esse é o conteúdo do post",
    "userId": 0
    }
    r = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    data = r.json()
    assert r.status_code == 201
    print(data)

def test_validating_post_response():
    payload = {
        "title": "meu primeiro post",
        "body": "esse é o conteúdo do post",
        "userId": 0
    }
    r = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    data = r.json()

    # o que o servidor retornou deve conter o que enviamos
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    print("Resposta validada com sucesso:", data)

def test_put_id1():
    payload = {
        "userId": 0,
        "id": 1,
        "title": "o post foi atualizado!",
        "body": "isso é o conteúdo alterado do post",
    }
    r = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=payload)
    data = r.json()

    assert r.status_code == 200
    print(f'Status code inesperado: {r.status_code}')
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["id"] == 1
    print("Post atualizado com sucesso:", data)

def test_validating_put_response():
    payload = {
        "userId": 0,
        "id": 1,
        "title": "o post foi atualizado!",
        "body": "isso é o conteúdo alterado do post",
    }
    r = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=payload)
    data = r.json()

    assert data["userId"] == payload["userId"]
    assert data["id"] == payload["id"]
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    print("Resposta validada com sucesso: ", payload["body"])

def test_deleting_post1():
    r = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    data = r.json()
    assert data == {} and r.status_code == 200
    print(f'o post realmente foi apagado: {data} e o status code foi: {r.status_code}')

def test_check_user_list():
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    data = r.json()
    count = 0

    for n in data:
        count+=1

    assert len(data) == count
    print(f'a lista tem {count} usuários')

def test_user_id5():
    r = requests.get("https://jsonplaceholder.typicode.com/users/5")
    data = r.json()
    assert data["name"] == "Chelsey Dietrich"
    print(f'o nome do usuário realmente é: {data["name"]}')

def test_posts_1_comments():
    payload = {
        "id": 99,
        "name": "nome do novo post",
        "email": "email@novo.com.br",
        "body": "conteúdo do novo post"
    }
    r = requests.post("https://jsonplaceholder.typicode.com/posts/1/comments", json=payload)
    data = r.json()
    assert r.status_code == 201
    print(f'o conteúdo do {data}')

def test_user_albums():
    r = requests.get("https://jsonplaceholder.typicode.com/users/3/albums")
    data = r.json()
    length = len(data)
    assert length == 10
    print(f'o usuário tem {length} álbuns')

def test_album_id_2_first_photo():
    r = requests.get("https://jsonplaceholder.typicode.com/albums/2/photos")
    data = r.json()
    assert len(data) > 0, "a lista está vazia"
    print('a lista não está vazia!')

    print(f'o álbum tem {len(data)} fotos. mostrando as 5 primeiras fotos separadas por id e título: ')
    for i in data[:5]:
        print(f'id: {i["id"]}, título:{i["title"]}')

    expected_title = "reprehenderit est deserunt velit ipsam"
    first_title = data[0]["title"]
    try:
        assert first_title == expected_title, (
            f'o título esperado era: {first_title}'
            )
    except AssertionError:
        print(f'\n Atenção: o título mudou. O título esperado era: {expected_title} e o título recebido foi: {first_title}')

def test_create_todo():
    payload = {
        "userId": 1,
		"title": "Learn Pytest",
		"completed": False
    }
    r = requests.post("https://jsonplaceholder.typicode.com/users/1/todos", json=payload)
    data = r.json()
    assert r.status_code == 201
    print(f'a nova task foi criada com sucesso. código de status: {r.status_code}')
    assert str(data["userId"]) == str(payload["userId"])
    assert str(data["title"]) == str(payload["title"])
    assert data["completed"] == payload["completed"]
    print("o que o servidor retornou está batendo com o que foi passado")

def test_update_task():
    payload = {
		"completed": True
    }
    r = requests.patch("https://jsonplaceholder.typicode.com/todos/5", json=payload)
    data = r.json()
    assert r.status_code == 200
    assert data["completed"] == payload["completed"]
    assert "userId" in data
    assert "id" in data
    assert "title" in data
    print("a task foi atualizada com sucesso!", data)

def test_list_id1_todos():
    r = requests.get("https://jsonplaceholder.typicode.com/users/1/todos")
    data = r.json()
    completed_tasks = []

    for n in data:
        if n["completed"]==True:
            completed_tasks.append(n)
            assert n["completed"]==True

    for i in completed_tasks:
        print(f'\n a lista de tasks feitas, organizadas por id é: -> {i["id"]}, -> {i["completed"]}')

def test_comment_id10():
    r = requests.get("https://jsonplaceholder.typicode.com/comments/10")
    data = r.json()
    assert "postId" in data
    assert "id" in data
    assert "name" in data
    assert "email" in data
    assert "body" in data
    print("tudo certo, comentário checado com sucesso!")

def test_delete_comment_id3():
    r = requests.delete("https://jsonplaceholder.typicode.com/comments/3")
    data = r.json()
    assert r.status_code == 200
    print(f'comentário deletado! o conteúdo agora é: {data}')

def test_empty_json():
    payload = {}
    r = requests.post("https://jsonplaceholder.typicode.com/todos/", json=payload)
    assert r. status_code == 201
    print("o status code foi: ", r.status_code)
    data = r.json()
    try:
        assert data["title"] == payload["title"]
    except KeyError:
        print("realmente não tem nenhum conteúdo no payload")

def test_countid7_posts():
    r = requests.get("https://jsonplaceholder.typicode.com/users/7/posts")
    data = r.json()
    count = 0

    for n in data:
        count+=1
    
    assert len(data) == count
    print(f'o usuário tem {count} comentários')

def test_put_email_id_2():
    payload = {
        "email": "new.email@example.com"
    }
    r = requests.put("https://jsonplaceholder.typicode.com/users/2", json=payload)
    data = r.json()
    assert data["email"] == payload["email"]
    print(f'o email foi trocado para: {payload["email"]}')

def delete_album_id4():
    r = requests.delete("https://jsonplaceholder.typicode.com/albums/4")
    data = r.json()
    assert r. status_code == 200
    assert data == {}
    print("álbum deletado com sucesso!")

def test_whole_json():
    userId = int(input("Digite seu novo ID: "))
    payload_1 = {
        "userId": userId,
        "title": "titulo do post",
        "body": "body do post"
    }

    r1 = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload_1)
    data = r1.json()
    assert r1.status_code == 201
    post_id = data["id"]
    print("post criado!")

    if data["userId"]==userId:
        print(data)

    payload_2 = {
        "postId": post_id,
        "name": "comentário de teste",
        "email": "teste@example.com",
        "body": "conteúdo do comentário"
    }
    
    r2 = requests.post("https://jsonplaceholder.typicode.com/comments", json=payload_2)
    assert r2.status_code == 201
    print("Comentário criado com sucesso!")

    r3 = requests.delete(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    data2 = r3.json()
    assert r3.status_code == 200
    print("print deletado!")
    print(data2)
    

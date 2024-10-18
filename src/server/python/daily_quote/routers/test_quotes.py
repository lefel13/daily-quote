from fastapi.testclient import TestClient


class TestQuotes:
    def test_post_response(self, client: TestClient):
        author = "John Doe"
        text = "Hello World!"
        payload = {"author": author, "text": text}
        response = client.post("/quotes", json=payload)
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["author"] == author
        assert response.json()["text"] == text

    def test_post_primary_key(self, client: TestClient):
        payload = {"author": "John Doe", "text": "The first quote"}
        n = 10
        for i in range(1, n + 1):
            response = client.post("/quotes", json=payload)
            print(f"{i} --- {response.json()['id']}")
        assert response.json()["id"] == n

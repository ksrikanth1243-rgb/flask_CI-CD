from app import mongo


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Student" in response.data


def test_add_student(client):
    response = client.post(
        "/add",
        data={
            "name": "New User",
            "email": "new@user.com",
            "course": "Python"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"New User" in response.data


def test_update_student(client):
    student_id = "66fddff25f4b5f6a0a123456"

    response = client.post(
        f"/update/{student_id}",
        data={
            "name": "Updated Name",
            "email": "updated@student.com",
            "course": "Updated Course"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Updated Name" in response.data


def test_delete_student(client):
    result = mongo.db.students.insert_one({
        "name": "Temp User",
        "email": "temp@user.com",
        "course": "Temp Course"
    })

    response = client.get(f"/delete/{result.inserted_id}", follow_redirects=True)

    assert response.status_code == 200
    assert b"Temp User" not in response.data

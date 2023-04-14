from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import secrets
import datetime

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:8088",
    "http://localhost:8000",
    "http://localhost:8081",
    "http://localhost:5000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class authStudent(BaseModel):
    id: str
    password: str

class signUpInfo(BaseModel):
    id: str
    password: str
    fullname: str

class authToken(BaseModel):
    token: str

@app.post("/student/auth/login")
async def authLogin(loginInfo: authStudent):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT password FROM students WHERE id=%s", (loginInfo.id,))
        row = cur.fetchone()
        if row and loginInfo.password == row[0]:
            token = secrets.token_hex(16)
            cur.execute("UPDATE students SET authToken = %s WHERE id = %s", (token, loginInfo.id))
            conn.commit()
            return token
        else:
            return False
    finally:
        cur.close()
        conn.close()

@app.post("/student/signup")
async def signUp(signUpInfo: signUpInfo):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM students WHERE id=%s", (signUpInfo.id,))
        row = cur.fetchone()
        if row:
            return False
        else:
            token = secrets.token_hex(16)
            cur.execute("INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)", (signUpInfo.id, signUpInfo.password, signUpInfo.fullname, '{}', '{}', token))
            conn.commit()
            return token
    finally:
        cur.close()
        conn.close()

@app.post("/student/auth/token")
async def checkToken(tokenInfo: authToken):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:       
        cur.execute("SELECT id, fullname, findingList, course FROM students WHERE authToken=%s", (tokenInfo.token,))
        row = cur.fetchone()
        if not row: return False
        student = {
            "id": row[0],
            "fullname": row[1],
            "findingList": row[2],
            "course": row[3],
        }
        return student
    finally:
        cur.close()
        conn.close()

@app.get("/student/{studentID}")
async def getStudent(studentID: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT id, fullname, findingList, course FROM students WHERE id=%s", (studentID,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    student = {
        "id": row[0],
        "fullname": row[1],
        "findingList": row[2],
        "course": row[3]
    }
    return student

@app.get("/student/{token}/findGroup/{course}/{setTo}")
async def lookingForGroup(token: str, course: str, setTo: bool ):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        if(setTo):
            cur.execute("UPDATE students SET findingList = findingList || %s WHERE authToken = %s ", ([course], token,))
        else:
            cur.execute("UPDATE students SET findingList = array_remove(findingList, %s) WHERE authToken = %s ", (course, token,))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/students/finding/{course}/count")
async def getFindingCount(course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM students WHERE findingGroup=true AND %s = ANY (findingList)", (course,))
    row = cur.fetchone()
    count = row[0]
    cur.close()
    conn.close()
    return count

@app.get("/students/finding/{course}")
async def getFindingStudents(course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT id, fullname FROM students WHERE findingGroup=true AND %s = ANY (findingList)", (course,))
    rows = cur.fetchall()
    availableStudents = []
    for row in rows:
        availableStudent = {
            "id": row[0],
            "fullname": row[1]
        }
        availableStudents.append(availableStudent)
    cur.close()
    conn.close()
    return availableStudents

@app.get("/student/pair/{token}/{course}")
async def checkPairStudent(token: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM students WHERE authToken=%s", (token,))
        user = cur.fetchone()[0]
        cur.execute("SELECT receiver, requester, course FROM pair_students WHERE receiver = %s AND course = %s", (user, course))
        requesterRow = cur.fetchone()
        if not requesterRow: 
            cur.execute("SELECT receiver, requester, course FROM pair_students WHERE requester = %s AND course = %s", (user, course))
            receiverRow = cur.fetchone()
            if not receiverRow: return False
            cur.execute("SELECT fullname FROM students WHERE id = %s", (receiverRow[0],))
            fullname = cur.fetchone()[0]
            pair = [{
                'receiver': receiverRow[0],
                'requester': receiverRow[1],
                'pairName': fullname,
                'course': receiverRow[2],
            }]
        else:
            cur.execute("SELECT fullname FROM students WHERE id = %s", (requesterRow[1],))
            fullname = cur.fetchone()[0]
            pair = [{
                'receiver': requesterRow[0],
                'requester': requesterRow[1],
                'pairName': fullname,
                'course': requesterRow[2],
            }]
        return pair
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/student/pair/clear/{token}/{course}")
async def clearPairStudent(token: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM students WHERE authToken=%s", (token,))
        user = cur.fetchone()[0]
        cur.execute("DELETE FROM pair_students WHERE receiver=%s OR requester=%s AND course=%s", (user, user, course))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/receive/{studentID}/{course}")
async def getStudentReceives(studentID: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:       
        cur.execute("SELECT * FROM requests WHERE receiver=%s AND course=%s", (studentID, course))
        rows = cur.fetchall()
        if not rows: return False
        receives = []
        for row in rows:
            cur.execute("SELECT fullname FROM students WHERE id=%s", (row[2],))
            fullname = cur.fetchone()
            receive = {
                "id": row[0],
                "receiver": row[1],
                "requester": row[2],
                "requesterName": fullname[0],
                "course": row[3],
            }
            receives.append(receive)
        return receives
    finally:
        cur.close()
        conn.close()

@app.get("/request/{studentID}/{course}")
async def getStudentRequests(studentID: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:       
        cur.execute("SELECT * FROM requests WHERE requester=%s AND course=%s", (studentID, course))
        rows = cur.fetchall()
        if not rows: return False
        requests = []
        for row in rows:
            request = {
                "id": row[0],
                "receiver": row[1],
                "requester": row[2],
                "course": row[3],
            }
            requests.append(request)
        return requests
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/request/approve/{token}/{requester}/{course}")
async def approveRequest(token: str, requester: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM students WHERE authToken=%s", (token,))
        receiver = cur.fetchone()[0]
        cur.execute("UPDATE students SET findingList = array_remove(findingList, %s) WHERE authToken = %s ", (course, token,))
        cur.execute("UPDATE students SET findingList = array_remove(findingList, %s) WHERE id = %s ", (course, requester,))
        cur.execute("INSERT INTO pair_students VALUES (%s, %s, %s)", (receiver, requester, course))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/request/add/{receiver}/{token}/{course}")
async def addRequest(receiver: str, token: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:       
        cur.execute("SELECT id FROM students WHERE authToken=%s", (token,))
        requester = cur.fetchone()[0]
        cur.execute("INSERT INTO requests(receiver, requester, course) VALUES (%s, %s, %s)", (receiver, requester, course))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/request/del/{requestID}")
async def removeRequestByID(requestID: int):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:       
        cur.execute("DELETE FROM requests WHERE id=%s", (requestID,))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/request/del/{receiver}/{token}/{course}")
async def removeRequest(receiver: str, token: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM students WHERE authToken=%s", (token,))
        requester = cur.fetchone()[0]
        cur.execute("DELETE FROM requests WHERE receiver=%s AND requester=%s AND course=%s", (receiver, requester, course))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/request/clear/{token}/{course}")
async def clearRequest(token: str, course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM students WHERE authToken=%s", (token,))
        receiver = cur.fetchone()[0]
        cur.execute("DELETE FROM requests WHERE receiver=%s AND course=%s", (receiver, course))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()

@app.get("/forums/{course}")
async def getForums(course: str):
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM forums WHERE course = %s", (course,))
        rows = cur.fetchall()
        forums = []
        for row in rows:
            cur.execute("SELECT fullname from students WHERE id = %s", (row[4],))
            fullname = cur.fetchone()[0]
            forum = {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'imagePath': row[3],
                'ownerID': row[4],
                'ownerName': fullname,
                'anonymous': row[5],
                'posted_at': row[6]
            }
            forums.append(forum)
        return forums
    except (Exception, psycopg2.DatabaseError):
        return False
    finally:
        cur.close()
        conn.close()
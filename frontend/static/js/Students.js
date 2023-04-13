const STUDENT_API_BASE_URL = "http://localhost:8088/student/"
const STUDENTS_API_BASE_URL = "http://localhost:8088/students/"

function authLogin(studentInfo){
    return axios.post(STUDENT_API_BASE_URL+"auth/login", studentInfo);
}

function signUp(signUpInfo){
    return axios.post(STUDENT_API_BASE_URL+"signup", signUpInfo);
}

function checkToken(token){
    return axios.post(STUDENT_API_BASE_URL+"auth/token", token);
}

function checkPair(token, course){
    return axios.get(STUDENT_API_BASE_URL+"pair/"+token+"/"+course);
}

function clearPair(token, course){
    return axios.get(STUDENT_API_BASE_URL+"pair/clear/"+token+"/"+course);
}

function getStudent(id){
    return axios.get(STUDENT_API_BASE_URL+id);
}

function getFindingCount(course){
    return axios.get(STUDENTS_API_BASE_URL+"finding/"+course+"/count");
}

function getFindingStudents(course){
    return axios.get(STUDENTS_API_BASE_URL+"finding/"+course);
}

function lookingForGroup(token, course, setTo){
    return axios.get(STUDENT_API_BASE_URL+token+"/findGroup/"+course+"/"+setTo);
}
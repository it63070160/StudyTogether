const FORUM_API_BASE_URL = "http://localhost:8088/forum/"
const FORUMS_API_BASE_URL = "http://localhost:8088/forums/"

function getForums(course){
    return axios.get(FORUMS_API_BASE_URL+course);
}
const FORUM_API_BASE_URL = "http://localhost:8088/forum/"
const FORUMS_API_BASE_URL = "http://localhost:8088/forums/"

function getForum(forumID){
    return axios.get(FORUM_API_BASE_URL+forumID);
}

function getForums(course){
    return axios.get(FORUMS_API_BASE_URL+course);
}

function getForumComments(forumID){
    return axios.get(FORUM_API_BASE_URL+"comments/"+forumID);
}

function addComment(commentInfo){
    return axios.post(FORUM_API_BASE_URL+"comment/add", commentInfo);
}

function editComment(editCommentInfo){
    return axios.post(FORUM_API_BASE_URL+"comment/edit", editCommentInfo);
}

function removeComment(commentID){
    return axios.get(FORUM_API_BASE_URL+"comment/remove/"+commentID);
}
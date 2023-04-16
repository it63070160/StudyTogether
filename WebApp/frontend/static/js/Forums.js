// import urls from './Config.js';
const FORUM_API_BASE_URL = "http://localhost:8088/forum/"
const FORUMS_API_BASE_URL = "http://localhost:8088/forums/"

function createForum(forumInfo){
    return axios.post(FORUM_API_BASE_URL+"create", forumInfo);
}

function getForum(forumID){
    return axios.get(FORUM_API_BASE_URL+forumID);
}

function getForums(course){
    return axios.get(FORUMS_API_BASE_URL+course);
}

function getMyForums(course, token){
    return axios.get(FORUMS_API_BASE_URL+course+"/"+token);
}

function getForumComments(forumID){
    return axios.get(FORUM_API_BASE_URL+"comments/"+forumID);
}

function handleSaveForum(forumID, token){
    return axios.get(FORUM_API_BASE_URL+"save/"+forumID+"/"+token);
}

function getSave(course, token){
    return axios.get(FORUM_API_BASE_URL+"saves/"+course+"/"+token);
}

function handleLike(forumID, token){
    return axios.get(FORUM_API_BASE_URL+"like/"+forumID+"/"+token);
}

function getLike(token){
    return axios.get(FORUM_API_BASE_URL+"like/"+token);
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
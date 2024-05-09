document.addEventListener("DOMContentLoaded", function() {
    fetchUserProfile();
    fetchFriends();
    fetchNeighbors();
});

function fetchUserProfile() {
    fetch('/api/profile')
        .then(response => response.json())
        .then(data => {
            const userProfileElement = document.getElementById('user-profile');
            userProfileElement.innerHTML = `
            <div class="friend-item">
                <img src="${data.profile_picture}" alt="Profile Picture" class ="friend-pic">
                <p>${data.username}</p><p> #${data.user_id}</p>
            </div>
            `;
            userProfileElement.onclick = function(){
                window.location.href = `/user/${data.user_id}/`; 
            }
        });
}

// function fetchFriends() {
//     fetch('/api/friends')
//         .then(response => response.json())
//         .then(data => {
//             const friendsElement = document.getElementById('friends-list');
//             friendsElement.innerHTML = '';  // Clear previous entries
//             data.friends.forEach(friend => {
//                 friendsElement.innerHTML += `
//                     <div class = "friend-item">
//                      <img src="${friend.profile_picture}" alt="Friend Picture" class = "friend-pic">
//                         <p>${friend.username}</p>
//                     </div>
//                 `;
//             });
//         });
// }

// function fetchNeighbors() {
//     fetch('/api/friends')
//         .then(response => response.json())
//         .then(data => {
//             const neighborElement = document.getElementById('neighbors-list');
//             neighborElement.innerHTML = '';  // Clear previous entries
//             data.neighbors.forEach(neighbor => {
//                 neighborElement.innerHTML += `
//                     <div class = "neighbor-item">
//                         <img src="${neighbor.profile_picture}" alt="Neighbor Picture" class = "neighbor-pic">
//                         <p>${neighbor.username}</p>
//                     </div>
//                 `;
//             });
//         });
// }
function fetchFriends() {
    fetch('/api/friends')
        .then(response => response.json())
        .then(data => {
            const friendsElement = document.getElementById('friends-list');
            friendsElement.innerHTML = '';  // Clear previous entries
            data.friends.forEach(friend => {
                const friendItem = document.createElement('div');
                friendItem.className = 'friend-item';
                friendItem.innerHTML = `
                    <img src="${friend.profile_picture}" alt="Friend Picture" class="friend-pic">
                    <p>${friend.username}</p><p> #${friend.user_id}</p>
                `;
                // 添加点击事件
                friendItem.onclick = function() {
                    window.location.href = `/user/${friend.user_id}/`;  // 确保这个路径与Django的url配置一致

                };
                friendsElement.appendChild(friendItem);
            });
        });
}

function fetchNeighbors() {
    fetch('/api/friends')
        .then(response => response.json())
        .then(data => {
            const neighborElement = document.getElementById('neighbors-list');
            neighborElement.innerHTML = '';  // Clear previous entries
            data.neighbors.forEach(neighbor => {
                const neighborItem = document.createElement('div');
                neighborItem.className = 'neighbor-item';
                neighborItem.innerHTML = `
                    <img src="${neighbor.profile_picture}" alt="Neighbor Picture" class="neighbor-pic">
                    <p>${neighbor.username}</p> <p> #${neighbor.user_id}</p> 
                `;
                // 添加点击事件
                neighborItem.onclick = function() {
                    window.location.href = `/user/${neighbor.user_id}/`;  // 确保这个路径与Django的url配置一致

                };
                neighborElement.appendChild(neighborItem);
            });
        });
}

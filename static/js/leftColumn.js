document.addEventListener("DOMContentLoaded", function() {
    fetchHoods();
    fetchBlocks();
});
let globalThreadId;

function fetchHoods() {
    fetch('/api/hoods')
    .then(response => response.json())
    .then(hoods => {
        const hoodsList = document.getElementById('hoods-list');
        if (hoods.length === 0) {
            // console.log("No threads received for block ID:", blockId);  // 如果没有数据，打印提示
            hoodsList.innerHTML = '<p>No threads available for this block.</p>'; // 显示没有数据的提示
            return;
        }
        hoods.forEach(hood => {
            const hoodElement = document.createElement('button');
            hoodElement.className = 'btn btn-success hood-item';
            hoodElement.innerText =  hood.name;
            hoodElement.onclick = function() {
                // 添加点击事件处理逻辑，例如显示该社区的详细信息或跳转至相关页面
                fetchThreadsForHood(hood.hood_id);
            };
            hoodsList.appendChild(hoodElement);
        });
    })
    .catch(error => console.error('Error loading hoods:', error));
}

function fetchBlocks() {
    fetch('/api/blocks')
    .then(response => response.json())
    .then(blocks => {
        const blocksList = document.getElementById('blocks-list');
        blocksList.innerHTML = ''; // Clear the list first
        blocks.forEach(block => {
            const blockElement = document.createElement('button');
            blockElement.className = block.is_followed ? 'btn btn-success block-item' : 'btn btn-primary block-item';
            blockElement.innerText = block.name;
            blockElement.onclick = function() {
                fetchThreadsForBlock(block.block_id,block.is_followed);
            };
            blocksList.appendChild(blockElement);
        });
    })
    .catch(error => console.error('Error loading blocks:', error));
}
// function fetchBlocks() {
//     fetch('/api/blocks')
//     .then(response => response.json())
//     .then(blocks => {
//         const blocksList = document.getElementById('blocks-list');
//         blocks.forEach(block => {
//             const blockElement = document.createElement('button');
//             blockElement.className = 'btn btn-primary block-item';
//             blockElement.innerText = block.name;
//             blockElement.onclick = function() {
//                 fetchThreadsForBlock(block.block_id);
//             };
//             blocksList.appendChild(blockElement);
//         });
//     })
//     .catch(error => console.error('Error loading blocks:', error));
// }

function fetchThreadsForHood(hoodId) {
    fetch(`/api/threads/hood/${hoodId}`)
    .then(response => response.json())
    .then(threads => {
        const threadsList = document.getElementById('threads-list');
            if (threads.length === 0) {
            // console.log("No threads received for block ID:", blockId);  // 如果没有数据，打印提示
            threadsList.innerHTML = '<p>No threads available for this block.</p>'; // 显示没有数据的提示
            return;
        }
        threadsList.innerHTML = ''; // Clear previous threads
        threads.forEach(thread => {
            const threadElement = document.createElement('button');
            threadElement.className = 'btn btn-outline-secondary thread-item';
            threadElement.innerText = thread.topic;
            threadElement.onclick = function() {
                fetchMessages(thread.thread_id,true); // Assume fetchMessages is defined to fetch messages of this thread
            };
            threadsList.appendChild(threadElement);
        });
    })
    .catch(error => console.error('Error loading threads:', error));
}
// function fetchThreadsForBlock(blockId) {
//     console.log("Fetching threads for block ID:", blockId);  // 确认函数被调用

//     fetch(`/api/threads/block/${blockId}`)
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(threads => {
//         const threadsList = document.getElementById('threads-list');
//         console.log("Fetching threads for  22:", blockId);  // 确认函数被调用

//         threadsList.innerHTML = ''; // Clear previous threads
//         threads.forEach(thread => {
//             console.log("Received threads data:", threads);  // 打印接收到的数据，检查是否如预期
//             if (threads.length === 0) {
//                 console.log("No threads received for block ID:", blockId);  // 如果没有数据，打印提示
//                 threadsList.innerHTML = '<p>No threads available for this block.</p>'; // 显示没有数据的提示
//                 return;
//             }
//             const threadElement = document.createElement('button');
//             threadElement.className = 'btn btn-outline-secondary thread-item';
//             threadElement.innerText = thread.topic;
//             console.log("Fetching threads for block ID23:", blockId); 
//             threadElement.onclick = function() {
//                 // fetchMessages(thread.thread_id); // Assume fetchMessages is defined to fetch messages of this thread
//             };
//             threadsList.appendChild(threadElement);
//         });
//     })
//     .catch(error => console.error('Error loading threads:', error));
// }
function fetchThreadsForBlock(blockId, canReply) {
    // console.log("Fetching threads for block ID:", blockId);  // 确认函数被调用

    fetch(`/api/threads/block/${blockId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(threads => {
        // console.log("Received threads data:", threads);  // 打印接收到的数据，检查是否如预期
        const threadsList = document.getElementById('threads-list');
        if (threads.length === 0) {
            // console.log("No threads received for block ID:", blockId);  // 如果没有数据，打印提示
            threadsList.innerHTML = '<p>No threads available for this block.</p>'; // 显示没有数据的提示
            return;
        }

        threadsList.innerHTML = ''; // Clear previous threads
        threads.forEach(thread => {
            // console.log("Processing thread:", thread);  // 打印每个线程的数据，检查结构是否正确

            const threadElement = document.createElement('button');
            threadElement.className = 'btn btn-outline-secondary thread-item';
            threadElement.innerText = thread.topic;
            threadElement.onclick = function() {
                // const temp = iffollowed? fetchMessages(thread.thread_id):fetchMessages(); // 激活消息获取功能，这里假设 fetchMessages 已定义
                fetchMessages(thread.thread_id,canReply)
            };
            threadsList.appendChild(threadElement);
        });
    })
    .catch(error => {
        console.error('Error loading threads:', error);
        alert("Failed to load threads. Please try again.");  // 给用户错误反馈
    });
}

function fetchMessages(threadId,canReply) {
    fetch(`/api/messages/thread/${threadId}`)
    .then(response => response.json())
    .then(messages => {
        const messagesList = document.getElementById('messages-list');
        messagesList.innerHTML = ''; // Clear previous messages
        messages.forEach(message => {
            // globalThreadId = threadId;
            const messageElement = document.createElement('div');
            messageElement.className = 'message-item';
            const timestamp = new Date(message.timestamp).toLocaleString(); // Convert timestamp to local date format
            messageElement.innerHTML = `<p><strong>${message.username}</strong>: ${message.body} <i>${timestamp}</i></p>`;
            messagesList.appendChild(messageElement);
        });
        if (canReply) {
            displayReplyBox(threadId);
        } else {
            clearReplyBox();
        }
    })
    .catch(error => console.error('Error loading messages:', error));
}

function displayReplyBox(threadId) {
    const replyBoxContainer = document.getElementById('message-reply-container');
    replyBoxContainer.innerHTML = `
        <textarea id="message-reply" placeholder="Type your message..."></textarea>
        <button onclick="sendReply(${threadId})">Send</button>
    `;
}

function clearReplyBox() {
    const replyBoxContainer = document.getElementById('message-reply-container');
    replyBoxContainer.innerHTML = '';
}

function sendReply(threadId) {
    const messageBody = document.getElementById('message-reply').value.trim(); // Ensure no extra whitespace
    if (!messageBody) {
        alert("Please enter a message before sending.");
        return;
    }
    // const threadId = globalThreadId; // Ensure this variable is correctly initialized and available
    const csrftoken = document.cookie.split(';').find(row => row.startsWith('csrftoken=')).split('=')[1];
    // 发送 AJAX 请求来发送用户回复的消息
    fetch(`/api/messages/thread/${threadId}/reply`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ body: messageBody })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('message-reply').value = '';
        fetchMessages(threadId,true);
    })
    .catch(error => {
        console.error('Error sending reply:', error);
        alert("Failed to send message. Please try again.");
    });
}






function fetchFriends(){
    fetch('/api/friendsNeighbor')
    .then(response => response.json())
    .then(blocks => {
        const blocksList = document.getElementById('friendNeighbor-list');
        blocks.forEach(block => {
            const blockElement = document.createElement('button');
            blockElement.className = 'btn btn-primary friendsNeighbor-item';
            blockElement.innerText = 'Friends';
            blockElement.onclick = function() {
                // 添加点击事件处理逻辑，例如显示该社区的详细信息或跳转至相关页面
            };
            blocksList.appendChild(blockElement);
        });
    })
    .catch(error => console.error('Error loading hoods:', error));
}
document.addEventListener("DOMContentLoaded", function() {
    fetchHoods();
});

function fetchHoods() {
    fetch('/api/hoods')
    .then(response => response.json())
    .then(hoods => {
        const hoodsList = document.getElementById('hoods-list');
        hoods.forEach(hood => {
            const hoodElement = document.createElement('div');
            hoodElement.className = 'hood-item';
            hoodElement.innerHTML = `<h2>${hood.name}</h2>`;
            hoodElement.onclick = function() {
                // 添加点击事件处理逻辑，例如显示该社区的详细信息或跳转至相关页面
            };
            hoodsList.appendChild(hoodElement);
        });
    })
    .catch(error => console.error('Error loading hoods:', error));
}
// 공감 버튼 클릭 시 새로고침 없이 좋아요 수를 올리는 기능
document.addEventListener("DOMContentLoaded", () => {
    const likeBtn = document.getElementById("like-btn");

    if (likeBtn) {
        likeBtn.addEventListener("click", () => {
            const opinionId = likeBtn.dataset.id;

            fetch(`/like/${opinionId}`, { method: "POST" })
                .then((response) => response.json())
                .then((data) => {
                    // 서버가 응답한 새 좋아요 수로 화면 갱신
                    document.getElementById("like-count").textContent = data.likes;
                });
        });
    }
});

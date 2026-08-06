// 공감 버튼 클릭 시 새로고침 없이 좋아요 수를 올리는 기능
document.addEventListener("DOMContentLoaded", () => {
    const likeBtn = document.getElementById("like-btn");

    if (likeBtn) {
        likeBtn.addEventListener("click", () => {
            const opinionId = likeBtn.dataset.id;

            fetch(`/like/${opinionId}`, { method: "POST" })
                .then((response) => response.json())
                .then((data) => {
                    document.getElementById("like-count").textContent = data.likes;
                    // 중복 클릭 방지: 누르고 나면 버튼 비활성화
                    likeBtn.disabled = true;
                    likeBtn.textContent = "👍 공감 완료";
                });
        });
    }
});

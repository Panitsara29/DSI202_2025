document.addEventListener("DOMContentLoaded", function () {
    const pendingCount = parseInt(document.body.getAttribute("data-pending-count"));
    if (pendingCount > 0) {
        alert(`📢 มีสลิปใหม่รอตรวจสอบจำนวน ${pendingCount} รายการ`);
    }
});

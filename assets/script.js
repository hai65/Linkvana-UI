function setupSidebarSelection() {
  const sidebarItems = document.querySelectorAll(".sidebar-item-container");

  if (sidebarItems.length === 0) {
    // Thử lại sau nếu chưa có phần tử
    setTimeout(setupSidebarSelection, 100);
    return;
  }

  sidebarItems.forEach(item => {
    item.addEventListener("click", () => {
      sidebarItems.forEach(i => i.classList.remove("selected"));
      item.classList.add("selected");
    });
  });
}

// Kích hoạt khi trang đã sẵn sàng
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupSidebarSelection);
} else {
  setupSidebarSelection();
}

const carousel = document.querySelector(".carousel");

let isDragging = false,startX,startScrollLeft;

const dragStart = () =>{
    isDragging = true;
    carousel.classList.add('dragging')
    startX = e.pageX
    startScrollLeft = carousel.scrollLeft;
}

const dragging = (e) => {
    if (!isDragging) return;
    carousel.scrollLeft = e.pageX;
}
carousel.addEventListener('mousedown',dragStart)
carousel.addEventListener("mousemove",dragging)
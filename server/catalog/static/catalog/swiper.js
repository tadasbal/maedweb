var swiper = new Swiper('.mySwiper', {
    slidesPerView: "auto",
    loop:true,
    spaceBetween: 0,
    centeredSlides: true,
    freeMode: true,
    // If window size is bigger than 640px, then you will slide through 5 slides, if not, than through 1 slide
    breakpoints:{
        640:{
            slidesPerGroup:3,
            rewind:true,
            loop:false,
            centeredSlides: false,
        },
        1100:{
            slidesPerGroup:4,
            rewind:true,
            loop:false,
            centeredSlides: false,
        }

    },  
    pagination: {
        el: '.swiper-pagination',
        type: 'fraction',
    },
    navigation: {
        nextEl: '.button-for-images-right',
        prevEl: '.button-for-images-left',
    },
});

console.log("Hello")


// koncept zasad DRY tutaj leży

$(window).on("load",function() {
    let current_slide = 1;
    let slide_count = 3;
    $(".arrow-right").on("click", () => {
        $(`.slider-nav a:nth-child(${current_slide})`).css("opacity", "0.75");
        ++current_slide;
        if(current_slide > slide_count) {
            current_slide = 1;
        }

        window.location.hash = `#slide-${current_slide}`;
        $(`.slider-nav a:nth-child(${current_slide})`).css("opacity", "1");
    })

    $(".arrow-left").on("click", () => {
        $(`.slider-nav a:nth-child(${current_slide})`).css("opacity", "0.75");
        --current_slide;
        if(current_slide < 1) {
            current_slide = slide_count;
        }
        
        window.location.hash = `#slide-${current_slide}`;
        $(`.slider-nav a:nth-child(${current_slide})`).css("opacity", "1");
    })

    $("#menu-btns ul li a").on("click", () => {
        $("#burger").prop("checked", false);
    })
});
window.onload = function () {
    changeCheckCode(this);
}

function changeCheckCode(ths) {
    <!--改变URL，刷新图片。-->
    ths.src = "/captcha_img/?r=" + Math.random();
}
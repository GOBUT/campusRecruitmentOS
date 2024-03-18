window.onload = function () {
    changeCheckCode(this);
}

function changeCheckCode(ths) {
    <!--改变URL，刷新图片。-->
    ths.src = "/captcha_img/?r=" + Math.random();
}

// function education_btn() {
//     var education_need = document.getElementById("education_need").value;
//     window.location.href = '/user/education_equirements/' + education_need;
//   }
//
// function city_btn() {
//     var work_city = document.getElementById("work_city").value;
//     window.location.href = '/user/city_filter/' + work_city;
//   }

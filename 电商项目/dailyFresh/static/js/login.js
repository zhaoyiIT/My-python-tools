$(function () {

    /* 判断用户名、密码框是否填写内容  */
    $('.name_input').blur(function () {
        check_username();
    });

    $('.pass_input').blur(function () {
        check_pwd();
    });

    /*检验用户名 */
    function check_username() {
        var len = $('.name_input').val().length
        if (len == 0) {
            $('.user_error').html('用户名不能为空！').show()
        }else{
            $('.user_error').hide()
        }
    }

    /* 检验密码*/
    function check_pwd() {
        var len = $('.pass_input').val().length
        if (len==0){
            $('.pwd_error').html('密码不能为空！').show()
        }else{
            $('.pwd_error').hide()
        }
    }

})
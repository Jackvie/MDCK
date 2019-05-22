var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host: host,
        username: '',
        sina_user_name: '',
        sina_img_url: '',
        profile_url: '',
        sina_before: 'http://www.weibo.com/',
        // 订单1,2的未来时间戳
        order_time1:order_time1,
        order_time2:order_time2,
        //　订单1,2的剩余时间
        create_time1: "",
        create_time2: "",
        d1:"",
        h1:"",
        m1:"",
        s1:"",
        d2:"",
        h2:"",
        m2:"",
        s2:"",
        errmsg:"取消订单失败",
        errmsg11:true,
        errmsg12:false,
        errmsg21:true,
        errmsg22:false,
        time_over1: "start",
        time_over2: "start",
        cancel1: "取消订单",
        cancel2: "取消订单",
        order_id1: order_id1,
        order_id2: order_id2,
    },
    mounted(){
        this.username = getCookie('username');
    },
    created: function(){
        ask_sina_msg(this);
        this.myfun1();
        this.myfun2();
    },
    methods: {
        // 控制1号订单渲染
        myfun1: function() {
            if (this.time_over1 == ""){
                return
            }

            var date = new Date();
            var now = date.getTime();
            //设置截止时间
            var endDate = new Date(this.order_time1);
            var end = endDate.getTime();
            //时间差
            var leftTime = end - now;

            //定义变量 d,h,m,s保存倒计时的时间
            if (leftTime >= 0) {
                this.d1 = Math.floor(leftTime / 1000 / 60 / 60 / 24);
                this.h1 = Math.floor(leftTime / 1000 / 60 / 69 % 24);
                this.m1 = Math.floor(leftTime / 1000 / 60 % 60);
                this.s1 = Math.floor(leftTime / 1000 % 60);
            }
            this.create_time1 = "订单有效期："+this.d1 + ":" + this.h1 + ":" + this.m1 + ":" + this.s1;
            // 如果有效期时间归零
            if (this.d1 == 0 && this.h1 == 0 && this.m1 == 0 && this.s1 <= 2){
                this.cancel_order(this.order_id1, 1);
            }
            setTimeout(this.myfun1, 1000);
        },
        // 控制2号订单渲染
        myfun2: function() {
            if (this.time_over2 == ""){
                return
            }
            var date = new Date();
            var now = date.getTime();
            //设置截止时间
            var endDate = new Date(this.order_time2);
            var end = endDate.getTime();
            //时间差
            var leftTime = end - now;

            //定义变量 d,h,m,s保存倒计时的时间
            if (leftTime >= 0) {
                this.d2 = Math.floor(leftTime / 1000 / 60 / 60 / 24);
                this.h2 = Math.floor(leftTime / 1000 / 60 / 69 % 24);
                this.m2 = Math.floor(leftTime / 1000 / 60 % 60);
                this.s2 = Math.floor(leftTime / 1000 % 60);
            }
            this.create_time2 = "订单有效期："+this.d2 + ":" + this.h2 + ":" + this.m2 + ":" + this.s2;

            if (this.d2 == 0 && this.h2 == 0 && this.m2 == 0 && this.s2 <= 2){
                this.cancel_order(this.order_id2, 2);
            }

            setTimeout(this.myfun2, 1000);
        },

        oper_btn_click(order_id, status){
            if (status == '1') {
                // 待支付
                var url = this.host + '/payment/' + order_id + '/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            location.href = response.data.alipay_url;
                        } else {
                            console.log(response.data);
                            alert(response.data.errmsg);
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    });
            } else if (status == '4') {
                // 待评价
                location.href = '/orders/comment/?order_id=' + order_id;
            } else {
                // 其他：待收货。。。
                location.href = '/';
            }
        },
        cancel_order(order_id, index){

            var url = this.host+"/orders/cancel/"+order_id+"/";
            axios.get(url, {
                responseType: 'json'
            })
                .then(
                    response => {
                        if (response.data.code == '0') {
                            if (index == 1){

                                this.create_time1 = "";
                                this.time_over1 = "";  // 清理定时器
                                this.cancel1 = "";
                                this.errmsg11 = false;
                                this.errmsg12 = true;
                            }
                            else if (index == 2){
                                this.create_time2 = "";
                                this.time_over2 = "";  // 清理定时器
                                this.cancel2 = "";
                                this.errmsg21 = false;
                                this.errmsg22 = true;
                            }
                            // 取消页面订单显示

                        } else {
                            alert(this.errmsg);
                        }
                    }
                )
                .catch(error => {
                        alert(this.errmsg);
                    })
        },
    }
});








// $(function () {
//
// });
//
//
// $('.oper_btn').click(function () {
//     var order_id = $(this).attr('order_id');
//     var status = $(this).attr('order_status');
//
//     if (status == '1') {
//         // 待支付
//         var url = '/payment/' + order_id + '/';
//         $.get(url, function (response) {
//             if (response.code == '0') {
//                 location.href = response.alipay_url;
//             } else {
//                 console.log(response);
//                 alert(response.errmsg);
//             }
//         });
//     } else if (status == '4') {
//         // 待评价
//         location.href = '/orders/comment/?order_id=' + order_id;
//     } else {
//         // 其他：待收货。。。
//         location.href = '/index/'
//     }
// });
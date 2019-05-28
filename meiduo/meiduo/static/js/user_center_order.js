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

        page_num: page_num, //当前页码
        page_orders: [],  //页码中的订单对象集

        errmsg: "取消订单失败",


    },
    created(){

        this.for_orders();

    },
    mounted(){
        this.username = getCookie('username');

    },
    updated(){
        setInterval(this.orders_time, 1000);
    },


    methods: {
        for_orders(){

            axios.post(this.host+"/orders/info/"+this.page_num+"/")
                .then(response => {
                    this.page_orders = response.data.page_orders;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },

        orders_time(){
            if(this.page_orders.length == 0){return};

            for (let i = 0; i < this.page_orders.length; i++) {
                // 只要不是待支付状态,直接跳过本次循环
                if (this.page_orders[i].status != 1){continue}

                // 待支付状态设置有效期
                var date = new Date();
                var now = date.getTime();
                //设置截止时间
                var endDate = new Date(this.page_orders[i].order_expire_time);
                var end = endDate.getTime();
                //时间差
                var leftTime = end - now;

                //定义变量 d,h,m,s保存倒计时的时间
                if (leftTime > 0) {
                    var d = Math.floor(leftTime / 1000 / 60 / 60 / 24);
                    var h = Math.floor(leftTime / 1000 / 60 / 69 % 24);
                    var m = Math.floor(leftTime / 1000 / 60 % 60);
                    var s = Math.floor(leftTime / 1000 % 60);
                    Vue.set(this.page_orders[i], "realtime", "订单有效期: "+d + "天" + h + "时" + m + "分" + s + "秒");
                } else {
                    // 有效期自动归零发送请求取消订单
                    this.cancel_order(this.page_orders[i].status, this.page_orders[i].order_id);
                }




            }
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

        // 取消订单
        cancel_order(status, order_id){
            if (status != 1){return}

            var url = this.host+"/orders/cancel/"+order_id+"/";
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        // 取消页面订单显示
                        order_id = response.data.order_id;
                        this.page_orders.forEach((value, index, att)=>{
                            if (value.order_id == order_id){
                                Vue.set(value, 'status', 6);
                                Vue.set(value, 'status_name', "已取消");
                                // 将有效期一次性置空
                                Vue.set(value, 'realtime', "")
                            }
                        });
                    } else {
                        alert(this.errmsg+"a");
                    }
                })
                .catch(error => {
                    alert(this.errmsg+"b");
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
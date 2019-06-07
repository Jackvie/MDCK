var vm = new Vue({
    el: '#app',
	// 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        username: '',
        spike_end: spike_end,
        spike_time: "",
        sina_user_name: '',
        sina_img_url: '',
        profile_url: '',
        sina_before: 'http://www.weibo.com/',

    },
    mounted(){
        setInterval(this.spiketime, 1000);
    },
    methods: {
        spiketime(){
            if (this.spike_end == null){return}
            //设置截止时间
            parseInt(this.spike_end);
            this.spike_end = this.spike_end - 1;
            //定义变量 h,m,s保存倒计时的时间
            if (this.spike_end > 0) {
                var h = Math.floor(this.spike_end  / 3600);
                var m = Math.floor(this.spike_end % 3600 / 60 );
                var s = Math.floor(this.spike_end % 3600 % 60);
                this.spike_time = h+":"+m+":"+s;
            }
        },
        add_cart(sku_id){
            var url = this.host + '/carts/';
            axios.post(url, {
                sku_id: parseInt(sku_id),
                count: 1
            }, {
                headers: {
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials:  true
            })
            .then(response => {
                if (response.data.code == '0') {
                    alert('添加购物车成功');
                } else { // 参数错误
                    alert(response.data.errmsg);
                }
            })
            .catch(error => {
                console.log(error.response);
            })
        },
    },
});

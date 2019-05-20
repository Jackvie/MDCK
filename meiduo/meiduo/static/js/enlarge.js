window.onload = function() {
    var oDiv = document.getElementById('small_img');
    var oSpan = oDiv.getElementsByTagName('span')[0];

    var oDiv2 = document.getElementById('middle_img');
    var img2 = oDiv2.getElementsByTagName('img')[0];

    /*
        mouseenter和mouseleave事件子级不会影响到父级，
        所以也可以用此方法消除子级对父级的影响
    */


    oDiv.onmouseenter = function(){
        oSpan.style.display = 'block';
        oDiv2.style.display = 'block';
    };

    oDiv.onmouseleave = function(){
        oSpan.style.display = 'none';
        oDiv2.style.display = 'none';
    };

    // 要想元素跟着鼠标移动要绑定mousemove事件
    oDiv.onmousemove = function(ev){
        var ev = ev || window.event;
        /*
            ev.clientX、ev.clientY获取鼠标坐标
            oDiv.offsetLeft: oDiv距离屏幕左侧的距离
            oDiv.offsetTop: oDiv距离屏幕顶部的距离
            oSpan.offsetWidth: offsetWidth返回对象的padding+border+width属性值之和
        */
        var L = ev.clientX - oDiv.offsetLeft - oSpan.offsetWidth/2; // 将黄色遮罩中部移到鼠标位置
        var T = ev.clientY - oDiv.offsetTop - oSpan.offsetHeight/2; // 将黄色遮罩中部移到鼠标位置

        /* 限制黄色遮罩层的移动范围START */
        if(L<0){
            L = 0;
        }
        else if(L>oDiv.offsetWidth - oSpan.offsetWidth){
            L = oDiv.offsetWidth - oSpan.offsetWidth;
        }

        if(T<0){
            T = 0;
        }
        else if(T>oDiv.offsetHeight - oSpan.offsetHeight){
            T = oDiv.offsetHeight - oSpan.offsetHeight;
        }

        oSpan.style.left = L + 'px';
        oSpan.style.top = T + 'px';
        /* 限制黄色遮罩层的移动范围END */

        var scaleX = L/(oDiv.offsetWidth - oSpan.offsetWidth); // 移动的比例 0 ~ 1
        var scaleY = T/(oDiv.offsetHeight - oSpan.offsetHeight); // 移动的比例 0 ~ 1

        /*
            大图的移动方向要和黄色遮罩(鼠标)移动方向相反
            img2.offsetWidth - oDiv2.offsetWidth 大图能够移动的最大宽度
            img2.offsetHeight - oDiv2.offsetHeight 大图能够移动的最大高度
        */
        img2.style.left = - scaleX * (img2.offsetWidth - oDiv2.offsetWidth) + 'px';
        img2.style.top = - scaleY * (img2.offsetHeight - oDiv2.offsetHeight) + 'px';        

    };

};

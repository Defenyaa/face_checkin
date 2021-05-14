

let appGetData = new Vue({
  //获取到数据之后需要绑定在 下边两个vue对象上
    data:{

      imageData:"",
      state:'class_checkin',
      ip:'http://127.0.0.1:8000/'
      
      
    },
    methods:{

      imageToBase64(file){
        if (file.size > 25 * 1024 * 1024) {
            alert("上传文件大小不能超过25M");
            return;
        }

        appGetData.setBase64(file,appGetData.toSend);	
      },
      setBase64(file,fn){//图片文件转换为base64编码
        if(!window.FileReader){
            alert('浏览器对FileReader方法不兼容');
            return;
        }
        var reader = new FileReader();
        reader.readAsDataURL(file);//读出 base64
        reader.onloadend = function (){
            appGetData.imgCompress(reader,function(base64){
                typeof fn=="function" && fn(base64 || reader.result )//base64
            });
        };
      },
      imgCompress(reader,callback){//图片超过尺寸压缩
        var img=new Image();
        img.src=reader.result;
        img.onload=function(){
            var w = this.naturalWidth, h = this.naturalHeight, resizeW = 0, resizeH = 0;  
            var maxSize = {
                width: 10000,
                height: 10000,
                level: 0.92
            };
              if(w > maxSize.width || h > maxSize.height){
                var multiple = Math.max(w / maxSize.width, h / maxSize.height);
                resizeW = w / multiple;
                resizeH = h / multiple;
              }else{// 如果图片尺寸小于最大限制，则不压缩直接上传
                return callback()
              }
              var canvas = document.createElement('canvas'),
              ctx = canvas.getContext('2d');
            canvas.width = resizeW;
            canvas.height = resizeH;
            ctx.drawImage(img, 0, 0, resizeW, resizeH);
              var base64 = canvas.toDataURL('image/jpeg', maxSize.level); 
              callback(base64);
        }
      },
      toSend(result){//传给后端result为处理好后的base64的字符串。
        appGetData.imageData = result
        // console.log(result)
        this.sendImage(appGetData.imageData)
      },


      sendImage(){
        if($("#checkbox1").is(":checked")==true)
        {
          bodyData = {"state":"class_checkin","imageData":this.imageData,"continueValidate":true}
        }else{
          bodyData = {"state":"class_checkin","imageData":this.imageData,"continueValidate":false}
        }

        axios.defaults.timeout = 15000;
        axios.post(this.ip+"class_clockin/",bodyData)
        .then(function(res){
            let jsonDate=res.data;
            if (jsonDate.state=='-1'){
              alert(jsonDate.log)
            }else{
              appText.res = res.data
            }
            
          },function(err){
            alert('出现错误：'+err);
        })
        document.getElementById("checkbox1").style="display:inline-block"
        appImageAndName.name = "连续查询"
        


      },


    }//methods结束

  })


let appImageAndName = new Vue({
    el:'#appImageAndName',
    data: {
        imageData:"./images/people.png",
        name:"待查询"
      },
    methods:{
      clickImage(){
        document.getElementById("uploader").click()
      },
      changeImage(event){
        let files = event.target.files
        if(files.length < 1)
        {
          return -1;
        }

        let file = files[0]
        if(file.size > 9956096)
        {
          alert("图片太大,请更换图片!")
          return -1;
        }
        appGetData.imageToBase64(file)
      
      },






    }//methods结束
    


})

let appText = new Vue({
  el:"#appText",
  data: {
      res:[1,2,3,4],
  }


})


let add = new Vue({
    el:'#add',
    data:{
        text:"你的人脸",
        text1:"注册 ",
        studentid:"",
        imageData:"./images/people.jpg", 
        ip:'http://127.0.0.1:8000/'
    },
    methods:{

        clicksubmit(){
            this.studentid = document.getElementById("studentid").value
            this.sendImage()
        },
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
            //console.log(file.size)
    
            if(file.size > 9956096)
            {
              alert("图片太大,请更换图片!")
              return -1;
            }
            // console.log(file)
            this.imageToBase64(file)
          
        },
        imageToBase64(file){
            if (file.size > 25 * 1024 * 1024) {
                alert("上传文件大小不能超过25M");
                return;
            }
    
            add.setBase64(file,add.toSend);	
        },
        setBase64(file,fn){//图片文件转换为base64编码
            if(!window.FileReader){
                alert('浏览器对FileReader方法不兼容');
                return;
            }
            var reader = new FileReader();
            reader.readAsDataURL(file);//读出 base64
            reader.onloadend = function (){
                add.imgCompress(reader,function(base64){
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
                    level: 0.95
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
            add.imageData = result
        },
       
       
        sendImage(){
            //处理bodyDate数据
    
    
            // 处理结束  2为上传人脸  1为验证人脸
            
            axios.defaults.timeout = 25000;
            bodyData = {"state":"register_face","imageData":this.imageData,"studentId":this.studentid}
            axios.post(this.ip+"class_clockin/",bodyData)
            .then(function(res){
                let jsonDate=res.data;

                if(jsonDate.state == '-1')
                {
                    add.text1 = jsonDate.log
                }

                else if(jsonDate.state == '1')
                {
                    add.text1 = "成功"
                }
                else
                {
                    add.text1 = "人脸注册失败"
                }
                add.text = ""


                console.log(jsonDate)


              },function(err){
                alert('出现错误：'+err);
            })
    
            
    
    
        },
        
    }



})
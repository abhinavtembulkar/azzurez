var video = document.querySelector('video')
const photo = document.querySelector('button')
const canvas = document.createElement('canvas')
const ss = document.getElementById('ss')
const checker = document.querySelector('#checkbutton')

function imager()
{
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
    {
        navigator.mediaDevices.getUserMedia({video:true}).then((stream)=>{
            video.srcObject = stream
            video.play()
        })
    }   
    
    photo.addEventListener('click',(event)=>{
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        canvas.getContext('2d').drawImage(video,0,0)
        ss.src = canvas.toDataURL('image/png')

        console.log(ss)
        document.querySelector('button').innerHTML = '<h2>LOADING....</h2>'
        document.querySelector('#result').innerHTML = `<div class='loader'></div>`

        ss.height = 320
        sender()
    })
}

function sender()
{ 
    var dataURL = canvas.toDataURL('image/png')
    dataurl = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
    
    $.ajax({ 
        type: "POST", 
        url: "/webcam", 
        data: { 
            imgBase64: dataurl 
        } 
    }).done(function(o) { 
        console.log('sent'); 
    }); 
}

imager()

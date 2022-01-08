$(document).ready(function () {
  const fileInput = document.getElementById("input");
  setInterval(function () {
    $("#statImg").attr(
      "src",
      $("#statImg").attr("src") + "?timestamp=" + new Date().getTime()
    );
  }, 500);
  fileInput.onchange = () => {
    // var _Profile_PIC = document.getElementById("input").value;
    // console.log(_Profile_PIC);
    const selectedFile = fileInput.files[0];
    fileInput.disabled = true;
    document.getElementById("inputBox").style.left = "-1em";
    document.getElementById("inputBox").style.right = "-1em";
    console.log(selectedFile);
    $("#outputContainer").hide();
    $("#upload").hide();
    $(".loadState").show();
    $("#statImg").show();
    console.log("Hello");
    predict_score(selectedFile);
    // for (var i = 0; i < 120; i++) {
    //   jQuery(document).ready(function () {
    //     // $("#statImg").show();
    //     console.log("Hello");
    //     $("#statImg").attr(
    //       "src",
    //       $("#statImg").attr("src") + "?timestamp=" + new Date().getTime()
    //     );
    //     // document.getElementById("#statImg").innerHTML.reload();
    //     // $("#statImg").attr("src", "example.png");
    //     // setTimeout("jQuery('#statImg').hide();", 500);
    //   });
    // }
  };

  function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });
  }

  function predict_score(video) {
    // var blob = new Blob(video, {
    //   type: "video/mp4",
    // });
    // console.log(video);
    // var url = getBase64(video);
    // console.log(url);
    getBase64(video).then((data) => {
      // console.log(data);
      // var blob = new Blob(video);
      // var blob = new Blob([url], { "type": "video/mp4" });
      var formdata = new FormData();
      formdata.append("video", data); //Correct: sending the Blob itself
      $.ajax({
        type: "POST",
        //   enctype: "multipart/form-data",
        //   dataType: "json",
        url: "/skynet/features/classify",
        data: formdata,
        processData: false,
        contentType: false,
        //   cache: false,
        //   timeout: 600000,
        success: function (data) {
          console.log("Data" + JSON.stringify(data));
          if (data.success) {
            if (!data.isLong) {
              document.getElementById("scored").value = data.scored;
              document.getElementById("probab").value = data.prob;
              $("#upload").show();
              $(".loadState").hide();
              $("#outputContainer").show();
            } else {
            }
            fileInput.disabled = false;
          }
        },
        error: function (e) {
          console.log("ERROR : ", e);
        },
      });
    });
    // $.post("/skynet/features/classify", { video: data } ,processData: false,
    //   contentType: false,);
    // $.ajax({
    //   url: "/skynet/features/classify",
    //   type: "POST",
    //   dataType: "json",
    //   contentType: "application/json; charset=utf-8",
    //   data: {
    //     video: video,
    //     csrfmiddlewaretoken: "{{ csrf_token }}",
    //   },

    //   success: function (data) {
    //     //console.log(data);
    //     if (data.success) {
    //       console.log("Hurray", data.msg);
    //     }
    //     // do nothing
    //     //show_response_message(data.msg, data.success);
    //   },
    //   error: function (data) {
    //     // do nothing
    //     //show_response_message(errors.http_error, false);
    //   },
    // });
  }
});

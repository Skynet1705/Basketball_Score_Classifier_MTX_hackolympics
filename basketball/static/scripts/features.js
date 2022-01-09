$(document).ready(function () {
  const fileInput = document.getElementById("input");
  setInterval(function () {
    $("#statImg").attr(
      "src",
      $("#statImg").attr("src") + "?timestamp=" + new Date().getTime()
    );
  }, 500);
  fileInput.onchange = () => {
    const selectedFile = fileInput.files[0];
    var allowedExtensions = /(\.mp4)$/i;
    if (!allowedExtensions.exec(fileInput.value)) {
      alert("Please upload file having extension .mp4 only.");
      fileInput.value = "";
    } else {
      if (fileInput.files && fileInput.files[0]) {
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
      }
    }
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
    getBase64(video).then((data) => {
      var formdata = new FormData();
      formdata.append("video", data);
      $.ajax({
        type: "POST",
        url: "/skynet/features/classify",
        data: formdata,
        processData: false,
        contentType: false,
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
              $(".loadState").hide();
            }
            fileInput.disabled = false;
          }
        },
        error: function (e) {
          console.log("ERROR : ", e);
        },
      });
    });
  }
});

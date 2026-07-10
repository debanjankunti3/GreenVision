const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

const uploadedImage =
document.getElementById("uploadedImage");

const fileInput =
document.getElementById("fileInput");

async function openCamera() {

    try {

        const stream =
        await navigator.mediaDevices.getUserMedia({

            video: {
                facingMode: "environment"
            }

        });

        video.srcObject = stream;

    }

    catch {

        alert("Camera permission denied");

    }
}

// async function openCamera() {

//     try {

//         const stream = await navigator.mediaDevices.getUserMedia({

//             video: {
//                 facingMode: "environment",
//                 width: { ideal: 1920 },
//                 height: { ideal: 1080 }
//             }

//         });

//         video.srcObject = stream;

//     } catch {

//         alert("Camera permission denied");

//     }
// }
function captureImage() {

    const context = canvas.getContext("2d");

    canvas.width = 800;
    canvas.height = 800;

    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    const imageData = canvas.toDataURL("image/jpeg", 0.9);

    uploadedImage.src = imageData;
    uploadedImage.style.display = "block";

    document.getElementById("capturedImage").value = imageData;
}

function chooseImage() {

    fileInput.click();

}

fileInput.addEventListener("change", function(e){

    const file = e.target.files[0];

    if(file){

        uploadedImage.src =
        URL.createObjectURL(file);

        uploadedImage.style.display =
        "block";
    }
});
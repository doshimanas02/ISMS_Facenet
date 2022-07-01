document.addEventListener("DOMContentLoaded",
    () => {
        var clickPhotos = getElementById('click5Photos');
        var submitData = getElementById('submit');
        var nm = document.querySelector('name').value;
        var rank = document.querySelector('rank').value;
        var number = document.querySelector('number').value;
        var gender = document.querySelector('input[name="gender"]:checked').value;
        var snumber = document.querySelector('snumber').value;
        var category = document.querySelector('category').value;
        var blacklist = document.querySelector('input[name="blacklist"]:checked').value;
        let canvas = document.querySelector("#canvas");
        var video = document.getElementById("vid");
        var mediaDevices = navigator.mediaDevices;
        photos = []
        clickPhotos.addEventListener("click", () => {
            photos.length = 0;
            mediaDevices
                .getUserMedia({
                    video: true,
                    audio: false,
                })
                .then((stream) => {
                    // Changing the source of video to current stream.
                    video.srcObject = stream;
                    video.addEventListener("loadedmetadata", () => {
                        video.play();
                    });

                    function sleep(ms) {
                        return new Promise(resolve => setTimeout(resolve, ms));
                    }

                    async function send_data() {
                        var photos = [];
                        for (i = 0; i < 5; i++) {
                            await sleep(1000);
                            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                            let image_data_url = canvas.toDataURL('image/jpeg');
                            photos[i] = image_data_url;
                        }
                        console.log(photos);
                    }
                });
            })
            submitData.addEventListener("click", () => {
            var form = new FormData();
            form.append("name", nm);
            form.append("rank", rank);
            form.append("number", number);
            form.append("blacklist", blacklist);
            form.append("category", category);
            form.append("gender", gender);
            form.append("snumber", snumber);
            form.append('photo0', photos[0]);
            form.append('photo1', photos[1]);
            form.append('photo2', photos[2]);
            form.append('photo3', photos[3]);
            form.append('photo4', photos[4]);

            $.ajax({
                type: "POST",
                url: "/saveDetails/",
                data: form,
                // {'photo0': photos[0], 'photo1': photos[1], 'photo2': photos[2], 'photo3': photos[3], 'photo4': photos[4]},
                success: function(data){
                    print_data(data);
                }
            });
        });
    }
);
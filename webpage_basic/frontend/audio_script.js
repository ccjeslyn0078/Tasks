const audio = document.getElementById("player");
const transcriptDiv = document.getElementById("transcriptDiv");

// get stored upload result
const storedData = localStorage.getItem("audioData");

if(storedData){

    const data = JSON.parse(storedData);

    if(data.type === "mp3"){

        // load audio file
        audio.src = data.audio_url;

        transcriptDiv.innerHTML = "";

        data.content.forEach(segment => {

            const p = document.createElement("p");

            p.innerHTML =
            "<b>" + segment.speaker + "</b> (" +
            segment.start.toFixed(1) + "s): " +
            segment.text;

            transcriptDiv.appendChild(p);

        });

    }

}

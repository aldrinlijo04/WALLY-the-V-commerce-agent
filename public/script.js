const canvas = document.getElementById('frequencyCanvas');
const ctx = canvas.getContext('2d');
const flash = document.getElementById('flash');
const clickSound = document.getElementById('clickSound');

canvas.width = window.innerWidth;
canvas.height = 200; // Set the height of the canvas to 200 pixels

let isRecording = false;
let audioContext;
let analyser;
let microphone;
let dataArray;
let animationId;
// Existing code...
let mediaRecorder;
let audioChunks = [];

const startRecording = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.start();
        mediaRecorder.ondataavailable = (e) => {
            audioChunks.push(e.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];

            const formData = new FormData();
            formData.append('audio', audioBlob, 'recorded_audio.wav');

            await fetch('/upload', {
                method: 'POST',
                body: formData,
            });
        };

        clickSound.play();
        flash.style.opacity = 1;
        setTimeout(() => {
            flash.style.opacity = 0;
        }, 50);

        isRecording = true;
        visualizeFrequency();
    } catch (err) {
        console.error('Error accessing microphone:', err);
    }
};

const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
    isRecording = false;
    cancelAnimationFrame(animationId);
    if (audioContext) {
        audioContext.close();
    }
};



const visualizeFrequency = () => {
    analyser.getByteFrequencyData(dataArray);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';

    const barWidth = canvas.width / dataArray.length;

    for (let i = 0; i < dataArray.length; i++) {
        const value = dataArray[i];
        const percent = value / 256;
        const height = canvas.height * percent;
        const offset = canvas.height - height - 1;

        ctx.fillRect(i * barWidth, offset, barWidth, height);
    }

    animationId = requestAnimationFrame(visualizeFrequency);
};

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !isRecording) {
        startRecording();
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space' && isRecording) {
        stopRecording();
    }
});
